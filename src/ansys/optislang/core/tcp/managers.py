# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Contains classes to obtain operate with project parametric."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from ansys.optislang.core.managers import CriteriaManager, ParameterManager, ResponseManager
from ansys.optislang.core.project_parametric import (
    ConstraintCriterion,
    Criterion,
    LimitStateCriterion,
    Parameter,
    Response,
)

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpCriteriaManagerProxy(CriteriaManager):
    """Contains methods for obtaining criteria."""

    __PROPERTY_MAPPING = {"limit_expression": "limit"}

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpCriteriaManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the criteria manager."""
        return f"CriteriaManager uid: {self.__uid}"

    def add_criterion(self, criterion: Criterion) -> None:
        """Add criterion to the system.

        Parameters
        ----------
        criterion: Criterion
            Criterion to be created in the system.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for Ansys optiSLang version >= 23.2.")
        else:
            self.__osl_server.add_criterion(
                uid=self.__uid,
                criterion_type=criterion.criterion.name,
                expression=criterion.expression,
                name=criterion.name,
                limit=criterion.limit_expression
                if isinstance(criterion, (ConstraintCriterion, LimitStateCriterion))
                else None,
            )

    def get_criteria(self) -> Tuple[Criterion, ...]:
        """Get the criteria of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the criterion for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        container = (
            self.__osl_server.get_actor_properties(uid=self.__uid)
            .get("Criteria", {})
            .get("sequence", [{}])
        )
        return tuple([Criterion.from_dict(criterion_dict) for criterion_dict in container])

    def get_criteria_names(self) -> Tuple[str, ...]:
        """Get all criteria names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all criteria names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        container = (
            self.__osl_server.get_actor_properties(uid=self.__uid)
            .get("Criteria", {})
            .get("sequence", [{}])
        )
        return tuple([criterion_dict["First"] for criterion_dict in container])

    def modify_criterion(self, criterion: Criterion) -> None:
        """Modify criterion in the system.

        Parameters
        ----------
        criterion : Criterion
            Criterion to be modified. Criterion name is used as idefentifier.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.modify_criterion_property(
                criterion_name=criterion.name,
                property_name="type",
                property_value=criterion.criterion.name,
            )
            self.modify_criterion_property(
                criterion_name=criterion.name,
                property_name="expression",
                property_value=criterion.expression,
            )
            if isinstance(criterion, (ConstraintCriterion, LimitStateCriterion)):
                self.modify_criterion_property(
                    criterion_name=criterion.name,
                    property_name="limit",
                    property_value=criterion.limit_expression,
                )

    def modify_criterion_property(
        self, criterion_name: str, property_name: str, property_value: Any
    ) -> None:
        """Modify property of criterion in the system.

        Parameters
        ----------
        criterion_name : str
            Name of criterion to be modified.
        property_name: str
            Name of property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.set_criterion_property(
                uid=self.__uid,
                criterion_name=criterion_name,
                name=self.__class__.__PROPERTY_MAPPING.get(property_name, property_name),
                value=property_value,
            )

    def remove_all_criteria(self) -> None:
        """Remove all criteria from the system.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.remove_criteria(uid=self.__uid)

    def remove_criterion(self, criterion_name: str) -> None:
        """Remove criterion from the system.

        Parameters
        ----------
        criterion_name : str
            Name of the criterion to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.remove_criterion(uid=self.__uid, name=criterion_name)


class TcpParameterManagerProxy(ParameterManager):
    """Contains methods for obtaining parameters."""

    __PROPERTY_MAPPING = {
        "operation": "dependency_expression",
    }

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpParameterManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the parameter manager."""
        return f"ParameterManager uid: {self.__uid}"

    def add_parameter(self, parameter: Parameter) -> None:
        """Add parameter to the system.

        Parameters
        ----------
        parameter: Parameter
            Parameter to be created in the system.

        Raises
        ------
        NameError
            Raised when the parameter with the given name already exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        if (
            self.__class__.__get_parameter_idx(container=container, parameter_name=parameter.name)
            is not None
        ):
            raise NameError(
                f"Parameter `{parameter.name}` already exists, choose another name"
                " or modify this parameter instead."
            )
        else:
            container.append(parameter.to_dict())
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )

    def get_parameters(self) -> Tuple[Parameter, ...]:
        """Get the parameters of the system.

        Returns
        -------
        Tuple[Parameter, ...]
            Tuple of the parameters for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        return tuple([Parameter.from_dict(parameter_dict) for parameter_dict in container])

    def get_parameters_names(self) -> Tuple[str, ...]:
        """Get all parameter names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all parameter names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        return tuple([parameter["name"] for parameter in container])

    def modify_parameter(self, parameter: Parameter):
        """Modify parameter in the system.

        Parameters
        ----------
        parameter: Parameter
            Parameter to be modified. Parameter name is used as identifier.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter.name)
        if idx is not None:
            parameter.id = container[idx]["id"]
            container[idx] = parameter.to_dict()
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )
        else:
            raise NameError(
                f"Parameter `{parameter.name}` doesn't exist in current parametric system."
            )

    def modify_parameter_property(
        self, parameter_name: str, property_name: str, property_value: Any
    ) -> None:
        """Modify property of parameter in the system.

        Parameters
        ----------
        parameter_name: str
            Name of the parameter to be modified.
        property_name: str
            Name of the property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter_name)
        if idx is not None:
            container[idx][
                self.__class__.__PROPERTY_MAPPING.get(property_name, property_name)
            ] = property_value
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )
        else:
            raise NameError(
                f"Parameter `{parameter_name}` doesn't exist in current parametric system."
            )

    def remove_all_parameters(self) -> None:
        """Remove all parameters from the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        parameter_manager["parameter_container"] = []
        self.__osl_server.set_actor_property(
            actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
        )

    def remove_parameter(self, parameter_name: str) -> None:
        """Remove parameter from the system.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter_name)
        if idx is not None:
            container.pop(idx)
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )

        else:
            raise NameError(
                f"Parameter `{parameter_name}` doesn't exist in current parametric system."
            )

    def __get_parameter_container(self) -> Tuple[Dict[str, list], List[dict]]:
        parameter_manager = self.__osl_server.get_actor_properties(uid=self.__uid)[
            "ParameterManager"
        ]
        container = parameter_manager["parameter_container"]
        return parameter_manager, container

    @staticmethod
    def __get_parameter_idx(container: list, parameter_name: str) -> Optional[int]:
        for idx, parameter in enumerate(container):
            if parameter["name"] == parameter_name:
                return idx
        return None


class TcpResponseManagerProxy(ResponseManager):
    """Contains methods for obtaining responses."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpResponseManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the response manager."""
        return f"ResponseManager uid: {self.__uid}"

    def get_responses(self) -> Tuple[Response, ...]:
        """Get the responses of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the responses for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        responses = []
        for key, res_dict in container.items():
            responses.append(Response.from_dict(key, res_dict))
        return tuple(responses)

    def get_responses_names(self) -> Tuple[str, ...]:
        """Get all responses names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all responses names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        return tuple(container.keys())
