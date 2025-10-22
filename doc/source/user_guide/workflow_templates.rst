.. _ref_workflow_templates:

Parametric design study templates
=================================

The :mod:`ansys.optislang.parametric.design_study_templates` module provides
ready-to-use **template classes** for constructing common types of
parametric workflows in optiSLang.

Templates encapsulate predefined study configurations such as optimization
on a metamodel (MOP), design exploration, or response-surface workflows.
Each template defines the data structure, parameter setup, and workflow logic
required for a particular analysis type.


Optimization on MOP
-------------------
Optimization on MOP using a MOP solver to optimize design and ProxySolver for validation.

Workflow:
  .. image:: ../_static/template_OptimizationOnMOP.png
     :width: 400
     :alt: Result of script.








