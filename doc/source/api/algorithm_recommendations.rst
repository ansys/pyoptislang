.. _ref_api_algorithm_recommendations:

=========================
Algorithm recommendation
=========================

Use :py:meth:`ParametricDesignStudyManager.recommend_algorithms
<ansys.optislang.parametric.design_study.ParametricDesignStudyManager.recommend_algorithms>`
or :py:meth:`ParametricDesignStudy.recommend_algorithms
<ansys.optislang.parametric.design_study.ParametricDesignStudy.recommend_algorithms>`
to request recommendations. The following typed request and response models are
available from ``ansys.optislang.core``:

.. currentmodule:: ansys.optislang.core.algorithm_recommendations

.. autosummary::
   :toctree: _autosummary

   AlgorithmWorkflow
   AlgorithmFamily
   AlgorithmCategory
   AlgorithmRecommendationContext
   AlgorithmRecommendationResolvedContext
   AlgorithmRecommendationOverrides
   AlgorithmRecommendation
   AlgorithmRecommendationResult
   AlgorithmRecommendationProvenance
   AlgorithmCapabilityRequirement
   AlgorithmLicenseRequirements
   AlgorithmLicenseStatus
   AlgorithmLicenseFilter
   LicenseRequirementStatus
   LicensePolicyMode
   LicensePolicyScenario
