.. _ref_design_study_templates:

Parametric design study templates
=================================

The :mod:`ansys.optislang.parametric.design_study_templates` module provides
ready-to-use **template classes** for constructing common types of
parametric design studies in optiSLang.

Templates encapsulate predefined study configurations such as optimization, design exploration, uncertainty quantification and metamodel generation.
Each template defines the data structure, parameter setup, and workflow logic
required for a particular design study type.


Optimization on MOP
-------------------
Optimization on MOP using a MOP solver to optimize design and ProxySolver for validation.

Workflow:
  .. image:: ../_static/template_OptimizationOnMOP.png
     :width: 800
     :alt: Result of script.








