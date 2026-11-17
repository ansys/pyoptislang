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
    """Evaluation options accepted by the recommendation query."""

    operate_on_mop: bool


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


class AlgorithmCapabilityRequirement(TypedDict):
    """License requirement associated with a server capability."""

    capability: str
    no_license_required: bool
    mapping_status: str
    any_of: list[str]


class AlgorithmLicenseRequirements(TypedDict):
    """Algorithm-only license requirements; not a workflow entitlement check."""

    status: str
    scope: Literal["algorithm_only"]
    custom_specific_status: str
    configuration_dependent_status: str
    capability_requirements: list[AlgorithmCapabilityRequirement]


class AlgorithmRecommendation(TypedDict):
    """One assessed, installed algorithm."""

    algorithm_id: str
    display_name: str
    family: str
    category: AlgorithmCategory
    origin: Literal["builtin", "custom"]
    assessment: Literal["no_assessment", "impossible", "not_applicable", "possible", "recommended"]
    license_status: str
    license_eligibility_verified: bool
    license_requirements: AlgorithmLicenseRequirements


class AlgorithmRecommendationResult(TypedDict):
    """Response returned by the design-study ``recommend_algorithms`` conveniences."""

    schema_version: int
    server_version: str
    rule_implementation_version: str
    resolved_context: AlgorithmRecommendationContext
    context_provenance: dict[str, str]
    recommendations: list[AlgorithmRecommendation]
    filtered_algorithms: list[AlgorithmRecommendation]
    license_filter: dict[str, object]
    warnings: list[str]
