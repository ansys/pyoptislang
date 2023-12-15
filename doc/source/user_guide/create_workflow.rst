.. _ref_create_workflow:

===============
Create workflow
===============
You use the :py:class:`RootSystem <ansys.optislang.core.nodes.RootSystem>` class ..
:py:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance,
Describe creation and connection of nodes, add code to create some workflow
use DesignFlow enum when creating nodes

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core import examples
    from pathlib import Path

