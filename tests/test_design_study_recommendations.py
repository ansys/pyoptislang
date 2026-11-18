# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mocked tests for design-study Decision Tree recommendation conveniences."""

from typing import Any, Dict, Tuple
from unittest.mock import Mock, patch

import pytest

from ansys.optislang.core.algorithm_recommendations import (
    AlgorithmRecommendationContext,
    AlgorithmWorkflow,
)
from ansys.optislang.core.osl_server import OslServer
from ansys.optislang.core.tcp.osl_server import TcpOslServer
from ansys.optislang.parametric.design_study import (
    ParametricDesignStudy,
    ParametricDesignStudyManager,
)


def _context() -> AlgorithmRecommendationContext:
    return {
        "parameters": {
            "deterministic_count": 2,
            "random_count": 0,
            "has_discrete_deterministic": False,
            "has_discrete_random": False,
            "has_nominal_discrete_deterministic": False,
        },
        "criteria": {"objective_count": 1, "constraint_count": 0},
    }


def _manager(response: Dict[str, Any]) -> Tuple[ParametricDesignStudyManager, Mock]:
    server = Mock(spec=TcpOslServer)
    server.get_algorithm_recommendations.return_value = response
    osl = Mock()
    osl.osl_server = server
    return ParametricDesignStudyManager(osl), server


def _study(server: Mock, system_uid: Any = "system-uuid") -> ParametricDesignStudy:
    osl = Mock()
    osl.osl_server = server
    study = ParametricDesignStudy.__new__(ParametricDesignStudy)
    study._ParametricDesignStudyBase__osl_instance = osl
    parametric_system = None if system_uid is None else Mock(uid=system_uid)
    patcher = patch.object(study, "get_last_parametric_system", return_value=parametric_system)
    patcher.start()
    return study


@pytest.fixture(autouse=True)
def _stop_patches():
    yield
    patch.stopall()


@pytest.mark.parametrize("workflow", ["optimization", "sensitivity"])
def test_manager_recommend_algorithms_explicit_context(workflow: AlgorithmWorkflow):
    """Explicit recommendations send one workflow and strip the transport envelope."""
    manager, server = _manager(
        {"status": "success", "message": "done", "schema_version": 1, "recommendations": []}
    )

    response = manager.recommend_algorithms(
        workflow=workflow,
        context=_context(),
        declared_license_features=("optimization_level2",),
    )

    assert response == {"schema_version": 1, "recommendations": []}
    server.get_algorithm_recommendations.assert_called_once_with(
        {
            "schema_version": 1,
            "source": "explicit",
            "workflow": workflow,
            "context": _context(),
            "declared_license_features": ["optimization_level2"],
        },
        uid=None,
    )


def test_manager_recommend_algorithms_forwards_enable_amop():
    """Sensitivity requests can disable the default AMOP preference."""
    manager, server = _manager({"schema_version": 1, "filtered_recommendations": []})
    context = _context()
    context["evaluation"] = {"enable_amop": False}

    response = manager.recommend_algorithms(workflow="sensitivity", context=context)

    assert response["filtered_recommendations"] == []
    server.get_algorithm_recommendations.assert_called_once_with(
        {
            "schema_version": 1,
            "source": "explicit",
            "workflow": "sensitivity",
            "context": context,
        },
        uid=None,
    )


def test_manager_recommend_algorithms_system_overrides():
    """System requests forward a uid and field-wise overrides."""
    manager, server = _manager({"schema_version": 1})

    manager.recommend_algorithms(
        workflow="sensitivity",
        system_uid="system-uuid",
        overrides={"criteria": {"objective_count": 2}},
    )

    server.get_algorithm_recommendations.assert_called_once_with(
        {
            "schema_version": 1,
            "source": "system",
            "workflow": "sensitivity",
            "overrides": {"criteria": {"objective_count": 2}},
        },
        uid="system-uuid",
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"workflow": "optimization"},
        {"workflow": "optimization", "context": _context(), "system_uid": "system-uuid"},
        {"workflow": "optimization", "context": _context(), "overrides": {}},
        {"workflow": "", "context": _context()},
        {"workflow": "robustness", "context": _context()},
        {"workflow": None, "context": _context()},
        {"workflow": 1, "context": _context()},
        {"workflow": ["optimization"], "context": _context()},
        {"workflow": ["optimization", "sensitivity"], "context": _context()},
    ],
)
def test_manager_recommend_algorithms_rejects_invalid_arguments(kwargs: Dict[str, Any]):
    """Invalid source combinations and non-scalar workflows are rejected locally."""
    manager, server = _manager({})
    with pytest.raises(ValueError):
        manager.recommend_algorithms(**kwargs)
    server.get_algorithm_recommendations.assert_not_called()


def test_manager_recommend_algorithms_rejects_string_license_features():
    """A single string is not silently split into characters."""
    manager, server = _manager({})
    with pytest.raises(TypeError):
        manager.recommend_algorithms(
            workflow="optimization",
            context=_context(),
            declared_license_features="optimization_level2",
        )
    server.get_algorithm_recommendations.assert_not_called()


def test_manager_recommend_algorithms_rejects_legacy_families_argument():
    """The unfinished multi-family selector is not part of the public API."""
    manager, server = _manager({})
    with pytest.raises(TypeError, match="families"):
        manager.recommend_algorithms(
            families=["optimization", "sensitivity"], context=_context()  # type: ignore[call-arg]
        )
    server.get_algorithm_recommendations.assert_not_called()


def test_manager_recommend_algorithms_requires_tcp_server():
    """Only the TCP server implements the recommendation query."""
    osl = Mock()
    osl.osl_server = Mock(spec=OslServer)
    with pytest.raises(NotImplementedError):
        ParametricDesignStudyManager(osl).recommend_algorithms(
            workflow="optimization", context=_context()
        )


def test_design_study_recommend_algorithms_uses_last_parametric_system():
    """A design study evaluates its own parametric system as the baseline."""
    server = Mock(spec=TcpOslServer)
    server.get_algorithm_recommendations.return_value = {"schema_version": 1}
    study = _study(server)

    response = study.recommend_algorithms(
        workflow="optimization",
        overrides={"criteria": {"objective_count": 2}},
        declared_license_features=[],
    )

    assert response == {"schema_version": 1}
    server.get_algorithm_recommendations.assert_called_once_with(
        {
            "schema_version": 1,
            "source": "system",
            "workflow": "optimization",
            "overrides": {"criteria": {"objective_count": 2}},
            "declared_license_features": [],
        },
        uid="system-uuid",
    )


def test_design_study_recommend_algorithms_requires_parametric_system():
    """A study without a parametric system cannot provide a baseline."""
    server = Mock(spec=TcpOslServer)
    study = _study(server, system_uid=None)
    with pytest.raises(RuntimeError, match="parametric system"):
        study.recommend_algorithms(workflow="sensitivity")
    server.get_algorithm_recommendations.assert_not_called()
