.. _ref_algorithm_recommendations:

=========================
Algorithm recommendations
=========================

The :mod:`ansys.optislang.parametric.design_study` module provides convenience
methods that evaluate optiSLang's Decision Tree without running an algorithm or
changing the project:

- :py:meth:`ParametricDesignStudyManager.recommend_algorithms
  <ansys.optislang.parametric.design_study.ParametricDesignStudyManager.recommend_algorithms>`
  accepts an explicit problem context or the UUID of any parametric system.
- :py:meth:`ParametricDesignStudy.recommend_algorithms
  <ansys.optislang.parametric.design_study.ParametricDesignStudy.recommend_algorithms>`
  derives the context from the last parametric system of a design study.

Requests are sent through the TCP optiSLang server.
Choose exactly one ``workflow``: ``"optimization"`` for the Opt wizard or
``"sensitivity"`` for the Sensi wizard. This selects the corresponding Decision
Tree branch, rather than combining algorithms for different workflows. To
compare workflows, make a separate request for each.
This prototype requires a matching server build accepting the scalar
``workflow`` field; the earlier ``families`` array is no longer accepted.

Explicit context
----------------

An explicit summary can be evaluated without an open project. Parameter counts
and discrete flags, plus objective and constraint counts, are required:

.. code:: python

    from ansys.optislang.parametric.design_study import ParametricDesignStudyManager

    manager = ParametricDesignStudyManager(osl)
    result = manager.recommend_algorithms(
        workflow="sensitivity",
        context={
            "parameters": {
                "deterministic_count": 3,
                "random_count": 0,
                "has_discrete_deterministic": False,
                "has_discrete_random": False,
                "has_nominal_discrete_deterministic": False,
            },
            "criteria": {"objective_count": 1, "constraint_count": 0},
        },
    )
    for algorithm in result["recommendations"]:
        print(algorithm["algorithm_id"], algorithm["assessment"])

Knowledge and evaluation fields can be added when known. Omitted values use
documented defaults and are identified in ``context_provenance``. Contradictory
effective values, such as a nominal discrete parameter without any discrete
deterministic parameter, are rejected.

Algorithm categories
--------------------

Each recommendation has a ``category`` that mirrors the group boxes of the
optiSLang wizards, so clients can present results the same way:

- Opt wizard: ``"gradient_and_downhill"``, ``"surrogate_assisted"``,
  ``"nature_inspired"``.
- Sensi wizard: ``"adaptive_sampling"`` (for example AMOP) and
  ``"sampling_method"``.
- ``"plugins"``: custom algorithms whose configuration does not declare a
  matching ``AlgoCategory``, including unclassified custom algorithms.

Built-in algorithms use the native wizard assignment. Custom algorithms use
the ``AlgoCategory`` entry of their configuration if it belongs to their
``AlgoType``.

System-derived context
----------------------

Call the method on a design study to derive the parameter and criterion summary
of its last parametric system from the open project. The ``overrides`` mapping
is applied field-by-field; omitted values retain the system-derived baseline.

.. code:: python

    study = manager.create_design_study(template)
    result = study.recommend_algorithms(
        workflow="optimization",
        overrides={"criteria": {"objective_count": 2}},
    )

For a parametric system that is not managed by a design study, pass its UUID to
the manager instead:

.. code:: python

    result = manager.recommend_algorithms(
        workflow="optimization",
        system_uid="<parametric-system-uuid>",
    )

License metadata
----------------

The optional ``declared_license_features`` argument accepts canonical
optiSLang feature names, for example ``["optimization_level2"]``. When omitted,
the server does not filter recommendations by license. When supplied, built-in
algorithms are filtered using their algorithm-level capability requirements and
the current server license steering policy. The response includes both retained
and filtered algorithms, the capability requirements, and whether eligibility
was verified. This is advisory only: it does not check out a license or verify
workflow-wide entitlements. Custom algorithms with unknown custom-specific
requirements are included but marked unverified.
Installed custom algorithms without a recognized workflow classification remain
visible as ``family="unclassified"`` with no assessment; their applicability to
the selected workflow is unknown.

See the :ref:`algorithm recommendation API reference
<ref_api_algorithm_recommendations>` for the request and response types.
