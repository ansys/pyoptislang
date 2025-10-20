Design Study
============
Main classes responsible for workflow creation and execution.
.. currentmodule:: ansys.optislang.parametric.design_study

.. autosummary::
   :toctree: _autosummary

   ParametricDesignStudyManager
   ParametricDesignStudy


An executable unit used by :py:class:`ParametricDesignStudy <ansys.optislang.parametric.design_study.ParametricDesignStudy>` defining execution order.

.. autosummary::
   :toctree: _autosummary

   ExecutableBlock


Elementary objects containing necessary data for automatic execution.
.. autosummary::
   :toctree: _autosummary

   ManagedInstance
   ManagedParametricSystem
   ProxySolverManagedParametricSystem


Helper classes used for migration of omdb files into a new optiSLang project.
.. autosummary::
   :toctree: _autosummary

   OMDBFilesProvider
   OMDBFilesSpecificationEnum
   