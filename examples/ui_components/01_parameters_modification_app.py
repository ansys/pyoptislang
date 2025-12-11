# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""
.. _ref_parameters_modification:

Parameters modification app
===========================

This example demonstrates how to utilize parametric ui components in a simple dash based app
allowing to modify parameters in projects parametric systems.

Multiple optimization systems are created using `parametric_design_study` functionality.
"""

#########################################################
# Perform required imports
# ------------------------
# Perform the required imports.


from enum import Enum
from math import sin
from pathlib import Path
from threading import Event, Thread

from IPython import get_ipython
from dash import Dash, Input, Output, State, callback, dcc, html, no_update
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import parametric_dash_ui  # TODO: agree on location of this

from ansys.optislang.core import Optislang
from ansys.optislang.core.errors import OslDisposedError
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import ParametricSystem, RootSystem, System
from ansys.optislang.core.project_parametric import (
    Design,
    DesignVariable,
    ObjectiveCriterion,
    OptimizationParameter,
    Response,
)
from ansys.optislang.parametric.design_study import ParametricDesignStudyManager
from ansys.optislang.parametric.design_study_templates import (
    GeneralAlgorithmTemplate,
    ProxySolverNodeSettings,
)

# TODO: add dependencies to the [examples]


#########################################################
# Create dash based app
# ---------------------
# Perform the required imports.


class ExecutionMode(Enum):
    """Enumeration of possible execution modes."""

    STANDARD = 0
    JUPYTER = 1


class ParametricModificationApp:
    """Dash based app for modification of the project parametric interactively.

    Parameters
    ----------
    optislang : Optislang
        Instance of an ``Optislang`` class with loaded project.
    host : str, optional
        IPv4/v6 address or domain name on which app is running as a
        server, by default ``"127.0.0.1"``.
    port : int, optional
        Port on which app is running as a server, by default ``8050``.
    """

    def __init__(self, optislang: Optislang, host="127.0.0.1", port=8050) -> None:
        """Initialize a new instance of the ``ParametricModificationApp``."""
        self.host = host
        self.port = port

        self.optislang_server = optislang

        # Store uid - object for quick access
        self.uid_object_mapping: dict[str, System] = {}

        # Display system name for the uid
        self.uid_name_mapping: dict[str, str] = {}

        # Execution option
        if self.__class__._running_in_jupyter_mode():
            self.execution_mode = ExecutionMode.JUPYTER
            self.jupyter_cell_registered = False
            self.next_cell_executed = Event()
        else:
            self.execution_mode = ExecutionMode.STANDARD
            self.app_thread = None

        self.app = Dash("ParametericModification")
        self.server = self.app.server

        self.stop_app = Event()
        self.optislang_server.log.info(f"App execution mode is: {self.execution_mode.name}")

    def build_parametrization_app(self) -> None:
        """Build the parametric app.

        Create the app layout and register callbacks.
        """
        if not self.optislang_server.osl_server:
            raise OslDisposedError("Optislang server is not running.")
        self._build_app_layout()
        self._register_callbacks()
        self._register_deactivation_callbacks()

    def start(self) -> None:
        """Start the app server.

        Standard execution => blocking run in a separate daemon thread.
        Jupyter notebook execution => blocking run in the main thread.
        """
        kwargs = {
            "host": self.host,
            "port": self.port,
        }

        if self.execution_mode == ExecutionMode.JUPYTER:
            self._register_jupyter_cleanup_hook()
            kwargs["jupyter_mode"] = "inline"
            kwargs["jupyter_width"] = "95%"
            self.app.run(**kwargs)
            self.stop_app.wait()
            # TODO: connect the next_cell_executed with dash app
            # TODO: make jupyter run in a non-blocking mode
        else:
            self.app_thread = Thread(
                target=self.app.run,
                kwargs=kwargs,
                daemon=True,
            )
            self.app_thread.start()
            self.stop_app.wait()

    def _append_tree_node(self, system: System, children: list[dict], parent_tree: list) -> None:
        """Append tree node to the list.

        Recursive helper function transforming pyosl objects into data format for
        the dash navigation tree.

        Parameters
        ----------
        system : System
           Optislang system.
        children : list[dict]
            Child nodes of the current system.
        parent_tree : list
            List where current system should be appended.
        """
        name = system.get_name()
        disable_parameters = not isinstance(system, ParametricSystem)
        disable_criteria = True  # TODO: criteria control not available
        tree_node = {
            "value": system.uid,  # unique key
            "label": name,
            "children": [],
        }

        self.uid_object_mapping[system.uid] = system
        self.uid_name_mapping[system.uid] = name
        parent_tree.append(tree_node)

        for child_dict in children:
            for child_obj, nodes_dict in child_dict.items():
                self._append_tree_node(child_obj, nodes_dict, tree_node["children"])

    def _build_app_layout(self) -> None:
        """Build app layout."""
        tree_data = self._build_tree()

        self.app.layout = dmc.MantineProvider(
            theme={
                "colorScheme": "light",
            },
            children=[
                html.Div(
                    children=[
                        dcc.Store(id="overlay-store", data=False, storage_type="session"),
                        dmc.Grid(
                            id="app-root",
                            align="stretch",
                            children=[
                                dmc.GridCol(
                                    span=3,
                                    children=[
                                        dmc.Paper(
                                            shadow="md",
                                            radius="md",
                                            p="md",
                                            children=[
                                                dmc.Title("Project tree", order=4),
                                                html.Hr(),
                                                html.Br(),
                                                dmc.Tree(
                                                    id="main-tree",
                                                    data=tree_data,
                                                    expandOnClick=True,
                                                    allowRangeSelection=False,
                                                    expanded="*",
                                                    expandedIcon=DashIconify(
                                                        icon="fluent:folder-16-regular"
                                                    ),
                                                    selectOnClick=True,
                                                    levelOffset=16,
                                                ),
                                            ],
                                        ),
                                        dmc.Center(
                                            mt=40,
                                            children=[
                                                dmc.Tooltip(
                                                    label="Press this button to finish editing and continue with design study.",
                                                    multiline=True,
                                                    w=300,
                                                    children=[
                                                        dmc.ActionIcon(
                                                            id="editing-finished-button",
                                                            children=DashIconify(
                                                                icon="codicon:debug-continue",
                                                                height=30,
                                                                color="white",
                                                            ),
                                                            variant="filled",
                                                            color="#ff922b",
                                                            size=80,
                                                            radius=30,
                                                        ),
                                                    ],
                                                )
                                            ],
                                        ),
                                        dmc.Center(
                                            children=[
                                                DashIconify(
                                                    icon="devicon:ansys-wordmark",
                                                    width=150,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.GridCol(
                                    span=9,
                                    children=dmc.Paper(
                                        shadow="md",
                                        radius="md",
                                        p="lg",
                                        children=[
                                            dmc.Title("Content Panel", order=4),
                                            html.Hr(),
                                            html.Div(
                                                id="content-area",
                                                style={"marginTop": "16px"},
                                                children=[
                                                    dmc.Badge(
                                                        id="displaySelected",
                                                        children="No Selection",
                                                        variant="dot",
                                                        color="red",
                                                        size="xl",
                                                        radius="xl",
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    dmc.Tabs(
                                                        id="parametrization-tabs",
                                                        children=[
                                                            dmc.TabsList(
                                                                id="tabs-list",
                                                                children=[
                                                                    dmc.TabsTab(
                                                                        id="parameters-tab",
                                                                        children="Parameters",
                                                                        value="parameters",
                                                                    ),
                                                                    dmc.TabsTab(
                                                                        id="criteria-tab",
                                                                        children="Criteria",
                                                                        value="criteria",
                                                                    ),
                                                                ],
                                                            ),
                                                            dmc.TabsPanel(
                                                                children=[
                                                                    html.Div(
                                                                        id="parameters-placeholder",
                                                                        children=[],
                                                                    )
                                                                ],
                                                                value="parameters",
                                                            ),
                                                            dmc.TabsPanel(
                                                                children=[
                                                                    html.Div(
                                                                        id="criteria-placeholder",
                                                                        children=[],
                                                                    )
                                                                ],
                                                                value="criteria",
                                                            ),
                                                        ],
                                                    ),
                                                    dmc.Button(
                                                        id="apply-changes",
                                                        variant="default",
                                                        size="md",
                                                        radius="lg",
                                                        mt=20,
                                                        children="Apply changes",
                                                        disabled=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                        dmc.LoadingOverlay(
                            id="grid-overlay",
                            visible=False,
                            loaderProps={
                                "variant": "custom",
                                "children": dmc.Center(
                                    children=[
                                        DashIconify(
                                            icon="nrk:media-media-complete",
                                            width=200,
                                            color="green",
                                        ),
                                    ]
                                ),
                            },
                        ),
                    ],
                    style={
                        "position": "relative",
                        "height": "100vh",
                        "width": "100%",
                        "overflow": "hidden",
                    },
                ),
            ],
        )

        if self.execution_mode == ExecutionMode.JUPYTER:
            self.app.layout.children.extend(
                [
                    dcc.Interval(
                        id="jupyter-listener",
                        interval=5000,
                        n_intervals=0,
                        disabled=False,
                    ),
                ]
            )

    def _build_tree(self) -> dict:
        """Build tree.

        Find all parametric systems in loaded project and create
        their dictionary representation in format for the dash
        navigation tree.

        Returns
        -------
        dict
            Dictionary containing optiSLang systems in dash navigation tree format.
        """
        self.uid_name_mapping.clear()
        self.uid_object_mapping.clear()

        name = self.optislang_server.application.project.get_name()
        root_system = self.optislang_server.application.project.root_system

        systems = self.__class__._get_parametric_systems(root_system)
        root_system, rs_children = next(iter(systems.items()))

        project_parametric_tree = {
            "value": root_system.uid,  # unique key
            "label": "Project - " + name,
            "children": [],
        }
        self.uid_object_mapping[root_system.uid] = root_system
        self.uid_name_mapping[root_system.uid] = "Project"

        for item in rs_children:
            for system, children in item.items():
                self._append_tree_node(system, children, project_parametric_tree["children"])

        return [project_parametric_tree]

    def _register_callbacks(self) -> None:
        @self.app.callback(
            Output("displaySelected", "color"),
            Output("displaySelected", "children"),
            Output("parameters-placeholder", "children"),
            # TODO: Output("criteria-placeholder", "children"),
            Output("apply-changes", "disabled"),
            Output("parametrization-tabs", "value"),
            Output("parameters-tab", "disabled"),
            Output("criteria-tab", "disabled"),
            Input("main-tree", "selected"),
            running=[
                (Output("displaySelected", "color"), "orange", "orange"),
                (Output("displaySelected", "children"), "...", "..."),
                (Output("apply-changes", "disabled"), True, True),
                (Output("main-tree", "selectOnClick"), False, True),
            ],
        )
        def update_content_panel(selected_item):
            """Update content panel.

            Lock navigation tree and apply changes button while running.

            Parameters
            ----------
            selected_item : list[str]
                Value (uid) of the selected item in navigation tree.

            Returns
            -------
            (str, str, object, bool, int, bool, bool)

            str:        color of dot next to the system name
                        (red - no selection, orange-processing, green-active, gray-not applicable)
            str:        Name of the selected system
            object:     Parameters table component
            bool:       Disable "apply-changes button
            int:        Index of tabs component
            bool:       Disable parameters tab
            bool:       Disable criteria tab
            """
            self.optislang_server.log.info("Updating content panel.")
            if not selected_item:
                return "red", "No selection", [html.Div()], True, 0, True, True
            else:
                uid = selected_item[0]
                is_parametric = isinstance(self.uid_object_mapping[uid], ParametricSystem)
                if is_parametric:
                    manager_dict = self.uid_object_mapping[uid].get_property("ParameterManager")
                    parameter_manager = parametric_dash_ui.ParametersTable(
                        id=uid + "_ParameterManager",
                        parameterManager=manager_dict,
                        theme="light",
                    )
                    color = "green"
                    apply_changes_disabled = False
                    parameters_tab_disabled = False
                    criteria_tab_disabled = True
                else:
                    color = "grey"
                    parameter_manager = html.Div()
                    apply_changes_disabled = True
                    parameters_tab_disabled = True
                    criteria_tab_disabled = True

                display_name = self.uid_name_mapping[selected_item[0]]
                parametrization_tabs_idx = 0

                self.optislang_server.log.debug(f"Selected node: {display_name}")
                self.optislang_server.log.debug(f"parameter manager: {parameter_manager}")
                # time.sleep(2)
                return (
                    color,
                    display_name,
                    [parameter_manager],
                    # TODO: criteria manager,
                    apply_changes_disabled,
                    parametrization_tabs_idx,
                    parameters_tab_disabled,
                    criteria_tab_disabled,
                )

        @self.app.callback(
            Input("apply-changes", "n_clicks"),
            State("main-tree", "selected"),
            State("parametrization-tabs", "value"),
            State("parameters-placeholder", "children"),
            # TODO: state from criteria-table
            running=[
                (Output("editing-finished-button", "disabled"), True, False),
                (Output("apply-changes", "disabled"), True, False),
            ],
        )
        def apply_changes(n_clicks, selected_item, selected_tab, param_placeholder_children):
            """Apply changes from active component to the optiSLang system."""
            uid = selected_item[0]
            self.optislang_server.log.info(
                f"Applying changes from node {self.uid_name_mapping[uid]} - {selected_tab}"
            )

            parametric_system = self.uid_object_mapping[uid]

            if selected_tab == "parameters" and param_placeholder_children:
                manager: parametric_dash_ui.ParametersTable = param_placeholder_children[0]
                value = manager["props"]["parameterManager"]
                property_name = "ParameterManager"
            else:
                # TODO: implement for criteria
                raise NotImplementedError()
            # time.sleep(2)
            parametric_system.set_property(property_name, value)

        @self.app.callback(Output("grid-overlay", "visible"), Input("overlay-store", "data"))
        def update_overlay(visible):
            """Update overlay visibility when page reloads."""
            self.optislang_server.log.info(f"Reload was triggered.")
            return self.stop_app.is_set()

    def _register_jupyter_cleanup_hook(self) -> None:
        """Register event setting value, when next cell is executed."""

        if self.jupyter_cell_registered:
            return

        ip = get_ipython()

        def notify(*args, **kwargs):
            self.next_cell_executed.set()

        ip.events.register("pre_run_cell", notify)
        self.jupyter_cell_registered = True

    def _register_deactivation_callbacks(self) -> None:
        """Register callbacks deactivating the app."""

        @self.app.callback(
            Output("overlay-store", "data"),
            Input("editing-finished-button", "n_clicks"),
            running=[
                (Output("apply-changes", "disabled"), True, False),
            ],
            prevent_initial_call=True,
        )
        def disable_app(n):
            if n and n > 0:
                self.optislang_server.log.info("Shutting down the app.")
                self.stop_app.set()
                return True
            else:
                return no_update

    @classmethod
    def _create_branches(cls, parent: System) -> tuple[list[dict], bool]:
        """Find all parametric systems.

        Recursive function looping over the parent nodes and returning
        only parametric systems (or systems containing parametric system(s)).

        Parameters
        ----------
        parent : System
            Optislang system.

        Returns
        -------
        tuple[list[dict], bool]
            Tuple of branches and info whether there is a parametric system.
        """
        children = parent.get_nodes()

        branch_children = []
        contains_parametric = isinstance(parent, ParametricSystem)

        for c in children:
            if isinstance(c, System):
                child_branch, child_contains = cls._create_branches(c)
                if child_contains:
                    branch_children.extend(child_branch)
                if child_contains:
                    contains_parametric = True

        # If no parametric system in this subtree, discard entirely
        if not contains_parametric:
            return [], False

        # For ParametricSystem: if no deeper parametrics, make it a leaf
        if isinstance(parent, ParametricSystem) and not branch_children:
            return [{parent: []}], True

        return [{parent: branch_children}], True

    @classmethod
    def _get_parametric_systems(cls, root_system: RootSystem) -> dict[System, list[dict]]:
        """Get parametric systems."""
        parametric_systems, _ = cls._create_branches(root_system)
        return next(iter(parametric_systems))

    @staticmethod
    def _running_in_jupyter_mode() -> bool:
        """Determine if app is running in jupyter mode."""
        try:
            from IPython import get_ipython

            return get_ipython().__class__.__name__ == "ZMQInteractiveShell"
        except:
            return False


#########################################################
# Create template inputs
# ----------------------
# Define template inputs, that are used by the parametric design study manager
# to create and execute the design study.


project_path = Path().cwd() / "parametric_app_demonstrator.opf"
parameters = [
    OptimizationParameter(name=f"X{i}", reference_value=0.0, range=(-3.14, 3.14))
    for i in range(1, 6)
]
responses = [Response(name="Y", reference_value=0.0)]
criteria = [ObjectiveCriterion("minY", expression="Y")]


def callback(designs: list[Design]) -> list[Design]:
    """Calculate coupled function for provided designs."""
    results_designs = []
    for design in designs:
        X1 = design.parameters[design.parameters_names.index("X1")].value
        X2 = design.parameters[design.parameters_names.index("X2")].value
        X3 = design.parameters[design.parameters_names.index("X3")].value
        X4 = design.parameters[design.parameters_names.index("X4")].value
        X5 = design.parameters[design.parameters_names.index("X5")].value

        Y = 0.5 * X1 + X2 + 0.5 * X1 * X2 + 5 * sin(X3) + 0.2 * X4 + 0.1 * X5
        id = design.id

        # create instance of design with new values
        output_design = Design(
            responses=[DesignVariable("Y", Y)],
            design_id=id,
        )
        results_designs.append(output_design)
    return results_designs


solver_settings = ProxySolverNodeSettings(callback=callback, multi_design_launch_num=-1)

#########################################################
# Create NLPQLP template
# ----------------------
# Define template that will be transformed into a NLPQLP system with proxy solver.

nlpqlp_template = GeneralAlgorithmTemplate(
    parameters=parameters,
    criteria=criteria,
    responses=responses,
    algorithm_type=nt.NLPQLP,
    solver_type=nt.ProxySolver,
    solver_settings=solver_settings,
)


#########################################################
# Create multiple NLPQLP systems
# ------------------------------
# Instantiate parametric design study manager, create multiple nlpql systems.

design_study_manager = ParametricDesignStudyManager(project_path=project_path)
for i in range(1, 4):
    nlpqlp_template.algorithm_name = f"NLPQL-{i}"
    study = design_study_manager.create_design_study(template=nlpqlp_template)
design_study_manager.save()

#########################################################
# Start the app
# -------------
# Instantiate and start the `ParameterModificationApp`.
# You can modify parameter properties. When your are finished with the modification,
# you must press the orange button deactivating the app.
#
# .. note::
#
#   App is started at local host, port 8050 by default. For terminal run,
#   you can open the app in the browser on address http://127.0.0.1:8050/.
#   When executed from jupyter notebook, app is show below the execution block.
#
# .. note::
#
#   Deleting and/or creation of new parameters is not treated in this example
#   and either will raise an error, or the parameters will be ignored.

parametrization_app = ParametricModificationApp(design_study_manager.optislang)
parametrization_app.build_parametrization_app()
parametrization_app.start()

#########################################################
# View generated app
# ------------------
# This image shows the generated app ui.
#
# .. image:: ../../_static/01_parameter_modification_app_gui.png
#  :width: 1000
#  :alt: App gui.


#########################################################
# Execute design studies
# ----------------------
# Execute all created design studies and save project.

for study in design_study_manager.design_studies:
    study.execute()

design_study_manager.save()

#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.

design_study_manager.optislang.dispose()


#########################################################
# View generated workflow
# -----------------------
# This image shows the generated workflow.
#
# .. image:: ../../_static/01_parameter_modification_app_workflow.png
#  :width: 800
#  :alt: Result of script.
