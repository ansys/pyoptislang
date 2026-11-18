# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT

"""Typed request and response models for Decision Tree recommendations."""

from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

AlgorithmWorkflow = Literal["optimization", "sensitivity"]
AlgorithmCategory = Literal[
    "gradient_and_downhill",
    "surrogate_assisted",
    "nature_inspired",
    "adaptive_sampling",
    "sampling_method",
    "plugins",
]
"""Wizard group of an algorithm, mirroring the optiSLang Opt/Sensi wizard group boxes.

Built-in algorithms use the native wizard assignment. Custom algorithms use ``AlgoCategory``
from their configuration if it matches their ``AlgoType``; otherwise they are ``"plugins"``.
"""
PriorKnowledge = Literal["not_set", "unaware", "fragmental", "preoptimized"]
ViolationKnowledge = Literal["not_set", "none", "seldom", "frequently"]
SolverNoise = Literal["not_set", "none", "some", "strong"]


class AlgorithmRecommendationParameters(TypedDict):
    """Complete parameter summary required for explicit-context requests."""

    deterministic_count: int
    random_count: int
    has_discrete_deterministic: bool
    has_discrete_random: bool
    has_nominal_discrete_deterministic: bool


class AlgorithmRecommendationCriteria(TypedDict):
    """Complete criterion summary required for explicit-context requests."""

    objective_count: int
    constraint_count: int


class AlgorithmRecommendationParameterOverrides(TypedDict, total=False):
    """Parameter fields that may override a system-derived context."""

    deterministic_count: int
    random_count: int
    has_discrete_deterministic: bool
    has_discrete_random: bool
    has_nominal_discrete_deterministic: bool


class AlgorithmRecommendationCriteriaOverrides(TypedDict, total=False):
    """Criterion fields that may override a system-derived context."""

    objective_count: int
    constraint_count: int


class AlgorithmRecommendationKnowledge(TypedDict, total=False):
    """Solver knowledge accepted by the recommendation query."""

    prior_knowledge: PriorKnowledge
    constraint_violations: ViolationKnowledge
    failed_designs: ViolationKnowledge
    solver_noise: SolverNoise


class AlgorithmRecommendationEvaluation(TypedDict, total=False):
    """Evaluation options accepted by the recommendation query.

    ``operate_on_mop`` is used by optimization. ``enable_amop`` is used by
    sensitivity and defaults to ``True``, which prefers AMOP. The option the
    selected workflow does not use is reported with provenance
    ``"not_applicable"``.
    """

    operate_on_mop: bool
    enable_amop: bool


class AlgorithmRecommendationContext(TypedDict):
    """Complete problem summary used for explicit-context requests."""

    parameters: AlgorithmRecommendationParameters
    criteria: AlgorithmRecommendationCriteria
    knowledge: NotRequired[AlgorithmRecommendationKnowledge]
    evaluation: NotRequired[AlgorithmRecommendationEvaluation]


class AlgorithmRecommendationOverrides(TypedDict, total=False):
    """Partial context fields that override a system-derived baseline."""

    parameters: AlgorithmRecommendationParameterOverrides
    criteria: AlgorithmRecommendationCriteriaOverrides
    knowledge: AlgorithmRecommendationKnowledge
    evaluation: AlgorithmRecommendationEvaluation


AlgorithmFamily = Literal["optimization", "sensitivity", "unclassified"]
"""Decision-tree family of an algorithm.

``"unclassified"`` custom algorithms stay in the result without an assessment.
"""
AlgorithmLicenseStatus = Literal[
    "not_evaluated",
    "included_by_unknown_custom_policy",
    "unknown_requirements",
    "eligible",
    "ineligible",
]
"""Advisory license eligibility of one algorithm."""
LicenseRequirementStatus = Literal["known", "partially_unknown", "unknown"]
"""Certainty of an algorithm's declared license requirements."""
LicensePolicyMode = Literal["unknown", "user_interactive", "non_interactive", "automation_server"]
"""Application mode of the license-steering policy captured with the response."""
LicensePolicyScenario = Literal[
    "default",
    "parent_child",
    "inside",
    "inside_parametric_0",
    "raptor_ai",
    "unknown",
]
"""Scenario of the license-steering policy captured with the response."""
AlgorithmRecommendationProvenance = Literal[
    "explicit",
    "system_derived",
    "overridden",
    "defaulted",
    "structure_defaulted",
    "not_applicable",
]
"""How one resolved-context field was obtained.

``"not_applicable"`` marks a field the selected workflow does not use.
"""


class AlgorithmCapabilityRequirement(TypedDict):
    """License requirement associated with a server capability."""

    capability: str
    no_license_required: bool
    mapping_status: Literal["known", "unknown"]
    any_of: list[str]


class AlgorithmLicenseRequirements(TypedDict):
    """Algorithm-only license requirements; not a workflow entitlement check."""

    status: LicenseRequirementStatus
    scope: Literal["algorithm_only"]
    custom_specific_status: Literal["known", "unknown"]
    configuration_dependent_status: Literal["known", "unknown"]
    capability_requirements: list[AlgorithmCapabilityRequirement]


class AlgorithmLicenseFilter(TypedDict):
    """Advisory license filter metadata returned with recommendations."""

    applied: bool
    policy_mode: LicensePolicyMode
    policy_scenario: LicensePolicyScenario
    declared_features: list[str]
    basis: Literal["current_server_steering_policy"]


class AlgorithmRecommendationResolvedKnowledge(TypedDict):
    """Knowledge values present on every resolved context."""

    prior_knowledge: PriorKnowledge
    constraint_violations: ViolationKnowledge
    failed_designs: ViolationKnowledge
    solver_noise: SolverNoise


class AlgorithmRecommendationResolvedEvaluation(TypedDict):
    """Evaluation values present on every resolved context."""

    operate_on_mop: bool
    enable_amop: bool


class AlgorithmRecommendationResolvedContext(TypedDict):
    """Problem summary returned after defaults and workflow rules are applied."""

    parameters: AlgorithmRecommendationParameters
    criteria: AlgorithmRecommendationCriteria
    knowledge: AlgorithmRecommendationResolvedKnowledge
    evaluation: AlgorithmRecommendationResolvedEvaluation


class AlgorithmRecommendation(TypedDict):
    """One assessed, installed algorithm.

    Retained recommendations are ordered by assessment, strongest first
    (``recommended``, ``possible``, ``not_applicable``, ``impossible``,
    ``no_assessment``), then by ``algorithm_id``.
    """

    algorithm_id: str
    display_name: str
    family: AlgorithmFamily
    category: AlgorithmCategory
    origin: Literal["builtin", "custom"]
    assessment: Literal["no_assessment", "impossible", "not_applicable", "possible", "recommended"]
    license_status: AlgorithmLicenseStatus
    license_eligibility_verified: bool
    license_requirements: AlgorithmLicenseRequirements


class AlgorithmRecommendationResult(TypedDict):
    """Response returned by the design-study ``recommend_algorithms`` conveniences.

    ``recommendations`` contains the retained algorithms.
    ``filtered_recommendations`` contains algorithms removed by the advisory
    license filter. Built-in algorithms with unknown configuration-dependent
    requirements stay in ``recommendations`` when their known requirements are
    covered; ``license_status`` is then ``"unknown_requirements"`` and
    ``license_eligibility_verified`` is false.
    """

    schema_version: int
    server_version: str
    rule_implementation_version: str
    resolved_context: AlgorithmRecommendationResolvedContext
    context_provenance: dict[str, AlgorithmRecommendationProvenance]
    recommendations: list[AlgorithmRecommendation]
    filtered_recommendations: list[AlgorithmRecommendation]
    license_filter: AlgorithmLicenseFilter
    warnings: list[str]
