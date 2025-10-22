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

"""Contains classes creating a workflow from template."""
from __future__ import annotations

from abc import abstractmethod
import os
from pathlib import Path
import shutil
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional, Tuple, Union
import warnings

from ansys.optislang.core import Optislang
from ansys.optislang.core.io import AbsolutePath, OptislangPath
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import (
    DesignFlow,
    ExecutionOption,
    IntegrationNode,
    Node,
    OutputSlot,
    ParametricSystem,
    ProxySolverNode,
)
from ansys.optislang.core.slot_types import SlotTypeHint
from ansys.optislang.parametric.design_study import (
    ExecutableBlock,
    ManagedInstance,
    ManagedParametricSystem,
    OMDBFilesProvider,
    ParametricDesignStudyManager,
    ProxySolverManagedParametricSystem,
)

if TYPE_CHECKING:
    from ansys.optislang.core.project_parametric import Criterion, Design, Parameter, Response


# region node settings
class GeneralNodeSettings:
    """Settings specific to all nodes."""

    @property
    def additional_settings(self) -> dict:
        """Additional settings for the solver node.

        Returns
        -------
        dict
            Additional settings for the solver node.
        """
        return self.__additional_settings

    @additional_settings.setter
    def additional_settings(self, value: dict):
        """Set additional settings for the solver node.

        Parameters
        ----------
        value : dict
            Additional settings for the solver node.
        """
        self.__additional_settings = value

    def __init__(self, additional_settings: Optional[dict] = None):
        """Initialize the GeneralNodeSettings.

        Parameters
        ----------
        additional_settings : Optional[dict], optional
            Additional settings for the solver node.
        """
        self.additional_settings = additional_settings if additional_settings else {}

    def convert_properties_to_dict(self) -> dict:
        """Convert the named tuple to a dictionary of properties.

        Returns
        -------
        dict
            Dictionary of properties.
        """
        properties = self.additional_settings
        return properties


class MopSolverNodeSettings(GeneralNodeSettings):
    """Settings specific to MOP solver nodes."""

    @property
    def multi_design_launch_num(self) -> int:
        """Number of designs to be sent/received in one batch.

        Returns
        -------
        Optional[int]
            Number of designs to be sent/received in one batch.
        """
        return self.__multi_design_launch_num

    @multi_design_launch_num.setter
    def multi_design_launch_num(self, value: int):
        """Set number of designs to be sent/received in one batch.

        Parameters
        ----------
        value : int
            Number of designs to be sent/received in one batch.
        """
        self.__multi_design_launch_num = value

    @property
    def input_file(self) -> Union[OptislangPath, None]:
        """Path to the MOP file.

        Returns
        -------
        Union[OptislangPath, None]
            Path to the MOP file or ``None``, if input file is specified by the connection.
        """
        return self.__input_file

    @input_file.setter
    def input_file(self, value: Union[str, Path, OptislangPath, None]) -> None:
        """Set path to the MOP file.

        Parameters
        ----------
        value : Union[str, Path, OptislangPath, None]
            Path to the MOP file.
            If ``None``, input file is expected to be specified by the connection.
        """
        if value is None:
            self.__input_file = value
        elif isinstance(value, OptislangPath):
            self.__input_file = value
        else:
            self.__input_file = AbsolutePath(value)

    def __init__(
        self,
        input_file: Optional[Union[str, Path, OptislangPath]] = None,
        multi_design_launch_num: Optional[int] = None,
        additional_settings: Optional[dict] = {},
    ):
        """Initialize the MopSolverNode.

        Parameters
        ----------
        input_file : Union[str, Path, OptislangPath]
            Path to the MOP file.
        multi_design_launch_num : Optional[int], optional
            Number of designs to be sent/received in one batch, by default 1.
        additional_settings : Optional[dict], optional
            Additional settings for the solver node.
        """
        super().__init__(additional_settings=additional_settings)
        self.input_file = input_file
        self.multi_design_launch_num = (
            multi_design_launch_num if multi_design_launch_num is not None else 1
        )

    def convert_properties_to_dict(self):
        """Get properties dictionary.

        Returns
        -------
        dict
            Dictionary with properties.
        """
        properties = {}
        properties["MultiDesignNum"] = self.multi_design_launch_num
        if self.input_file:
            if isinstance(self.input_file, OptislangPath):
                properties["MDBPath"] = self.input_file.to_dict()
        properties.update(super().convert_properties_to_dict())
        return properties


class ProxySolverNodeSettings(GeneralNodeSettings):
    """Settings specific to Proxy solver nodes.

    Attributes
    ----------
    additional_settings : Optional[dict]
        Additional settings for the solver node.
    callback : callable
        A callback function to handle design evaluation results.
    """

    @property
    def multi_design_launch_num(self) -> int:
        """Number of designs to be sent/received in one batch.

        Returns
        -------
        Optional[int]
            Number of designs to be sent/received in one batch.
        """
        return self.__multi_design_launch_num

    @multi_design_launch_num.setter
    def multi_design_launch_num(self, value: int):
        """Set number of designs to be sent/received in one batch.

        Parameters
        ----------
        value : int
            Number of designs to be sent/received in one batch.
        """
        self.__multi_design_launch_num = value

    @property
    def callback(self) -> Callable:
        """A callback function to handle design evaluation results.

        Returns
        -------
        Callable
            A callback function to handle design evaluation results.
        """
        return self.__callback

    @callback.setter
    def callback(self, value: Callable):
        """Set a callback function to handle design evaluation results.

        Parameters
        ----------
        value : Callable
            A callback function to handle design evaluation results.
        """
        self.__callback = value

    def __init__(
        self,
        callback: Callable,
        multi_design_launch_num: Optional[int] = None,
        additional_settings: Optional[dict] = {},
    ):
        """Initialize the MopSolverNode.

        Parameters
        ----------
        callback: Callable
            A callback function to handle design evaluation results.
        multi_design_launch_num : Optional[int], optional
            Number of designs to be sent/received in one batch, by default 1.
        additional_settings : Optional[dict], optional
            Additional settings for the solver node.
        """
        super().__init__(additional_settings=additional_settings)
        self.callback = callback
        self.multi_design_launch_num = (
            multi_design_launch_num if multi_design_launch_num is not None else 1
        )

    def convert_properties_to_dict(self) -> dict:
        """Get properties dictionary.

        Returns
        -------
        dict
            Dictionary with properties.
        """
        properties = {}
        properties["MultiDesignLaunchNum"] = self.multi_design_launch_num
        properties.update(super().convert_properties_to_dict())
        return properties


class PythonSolverNodeSettings(GeneralNodeSettings):
    """Settings specific to Python solver nodes."""

    @property
    def input_code(self) -> Union[str, None]:
        """Python script code.

        Returns
        -------
        Union[str, None]
            Python script code or ``None``, if input file is meant to be specified
            by the connection or `input_file`.
        """
        return self.__input_code

    @input_code.setter
    def input_code(self, value: Union[str, None]) -> None:
        """Set Python script.

        Parameters
        ----------
        value : Union[str, None]
            Python script.
            If ``None``, input file is expected to be specified either
            by the connection or `input_file`.
        """
        self.__input_code = value

    @property
    def input_file(self) -> Union[OptislangPath, None]:
        """Path to the Python file.

        Returns
        -------
        Union[OptislangPath, None]
            Path to the Python file or ``None``, if input file is meant to be specified
            by the connection or `input_code`.
        """
        return self.__input_file

    @input_file.setter
    def input_file(self, value: Union[str, Path, OptislangPath, None]) -> None:
        """Set path to the Python file.

        Parameters
        ----------
        value : Union[str, Path, OptislangPath, None]
            Path to the Python file.
            If ``None``, input file is expected to be specified either
            by the connection or `input_code`.
        """
        if value is None:
            self.__input_file = value
        elif isinstance(value, OptislangPath):
            self.__input_file = value
        else:
            self.__input_file = AbsolutePath(value)

    def __init__(
        self,
        input_file: Optional[Union[str, Path]] = None,
        input_code: Optional[str] = None,
        additional_settings: Optional[dict] = {},
    ):
        """Initialize the PythonSolverNode.

        Parameters
        ----------
        input_file : Optional[Union[str, Path]], optional
            Path to the Python script file.
            Cannot be specified together with `input_code`.
        input_code: Optional[str], optional
            Python source code as a string.
            Cannot be specified together with `input_file`
        additional_settings : Optional[dict], optional
            Additional settings for the solver node.
        """
        super().__init__(additional_settings=additional_settings)
        if input_file and input_code:
            raise AttributeError(
                "Arguments `input_file` and `input_code` cannot be specified simultaneously."
            )
        elif input_file:
            self.input_file = input_file
            self.input_code = None
        elif input_code:
            self.input_code = input_code
            self.input_file = None
        else:
            self.input_file = None
            self.input_code = None

    def convert_properties_to_dict(self):
        """Get properties dictionary.

        Returns
        -------
        dict
            Dictionary with properties.
        """
        properties = {}
        if self.input_file and self.input_code:
            raise AttributeError(
                "Arguments `input_file` and `input_code` cannot be specified simultaneously."
            )
        elif self.input_file:
            properties["Path"] = self.input_file.to_dict()
            # content mode
        elif self.input_code:
            properties["Source"] = self.input_code
        properties.update(super().convert_properties_to_dict())
        return properties


# endregion


# region parametric system settings
class GeneralParametricSystemSettings:
    """Settings common to all parametric systems."""

    @property
    def additional_settings(self) -> dict:
        """Additional settings for the parametric system.

        Returns
        -------
        dict
            Additional settings for the parametric system.
        """
        return self.__additional_settings

    @additional_settings.setter
    def additional_settings(self, value: dict):
        """Set additional settings for the parametric system.

        Parameters
        ----------
        value : dict
            Additional settings for the parametric system.
        """
        self.__additional_settings = value

    def __init__(self, additional_settings: Optional[dict] = None):
        """Initialize the GeneralParametricSystemSettings.

        Parameters
        ----------
        additional_settings : Optional[dict], optional
            Additional settings for the parametric system.
        """
        self.additional_settings = additional_settings if additional_settings is not None else {}

    def convert_properties_to_dict(self) -> dict:
        """Convert the named tuple to a dictionary of properties.

        Returns
        -------
        dict
            Dictionary of properties.
        """
        properties = self.additional_settings
        return properties


class GeneralAlgorithmSettings(GeneralParametricSystemSettings):
    """Settings common to all algorithms."""

    def __init__(self, additional_settings: Optional[dict] = {}):
        """Initialize the GeneralAlgorithmSettings.

        Parameters
        ----------
        additional_settings : Optional[dict], optional
            Additional settings for the algorithm.
        """
        super().__init__(additional_settings=additional_settings)

    def convert_properties_to_dict(self) -> dict:
        """Convert the named tuple to a dictionary of properties.

        Returns
        -------
        dict
            Dictionary of properties.
        """
        properties = self.additional_settings
        return properties


# endregion


# region Workflow templates
class WorkFlowTemplate:
    """Base class for workflow templates."""

    @abstractmethod
    def create_workflow(
        self, parent: ParametricSystem
    ) -> Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]:  # pragma: no cover
        """Abstract method implemented in derived classes.

        Parameters
        ----------
        parent : ParametricSystem
            Parent system to create the workflow in.

        Returns
        -------
        Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]
            Tuple of managed instances and executable blocks.

        """
        pass

    def create_algorithm(
        self,
        parent_system: ParametricSystem,
        parameters: Iterable[Parameter],
        criteria: Iterable[Criterion],
        responses: Iterable[Response],
        algorithm_type: nt.NodeType,
        solver_type: nt.NodeType,
        algorithm_name: Optional[str] = None,
        algorithm_settings: Optional[GeneralAlgorithmSettings] = None,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        start_designs: Optional[Iterable[Design]] = None,
        connections_algorithm: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
        connections_solver: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
    ) -> Tuple[ParametricSystem, IntegrationNode]:
        """Create an algorithm system with solver node and append to managed algorithms.

        Parameters
        ----------
        parent_system : ParametricSystem
            Parent system to create the algorithm in.
        parameters : Iterable[Parameter]
            Parameters to be included in the algorithm.
        criteria : Iterable[Criterion]
            Criteria to be included in the algorithm.
        responses : Iterable[Response]
            Responses to be included in the algorithm.
        algorithm_type : NodeType
            The type of algorithm to generate.
        solver_type : NodeType
            The type of solver node to generate.
        algorithm_name : Optional[str], optional
            Optional name or ID for the algorithm.
        algorithm_settings : Optional[GeneralAlgorithmSettings] , optional
            Additional settings for the algorithm. Settings must be compatible with
            the selected algorithm type.
        solver_name : Optional[str], optional
            Name for the solver node.
        solver_settings : Optional[GeneralNodeSettings], optional
            Additional settings for the solver node.
        start_designs : Optional[Iterable[Design]], optional
            Designs to be used as start designs for the algorithm.
        connections_algorithm: Optional[Iterable[Tuple[OutputSlot, str]]]
            Iterable of tuples specifying the connection from each predecessor node to the
            new algorithm.
        connections_solver: Optional[Iterable[Tuple[OutputSlot, str]]]
            Iterable of tuples specifying the connection from each predecessor node to the
            new solver node.

        Returns
        -------
        ParametricSystem, IntegrationNode
            The created algorithm system and the created solver node.
        """
        algorithm = parent_system.create_node(type_=algorithm_type, name=algorithm_name)
        assert isinstance(algorithm, ParametricSystem)

        # Connect each predecessor if both lists are provided and lengths match
        if connections_algorithm:
            for output_slot, input_slot_str in connections_algorithm:
                output_slot.connect_to(algorithm.get_input_slots(name=input_slot_str)[0])

        settings_dict = (
            algorithm_settings.convert_properties_to_dict()
            if isinstance(algorithm_settings, GeneralAlgorithmSettings)
            else {}
        )
        for name, value in settings_dict.items():
            algorithm.set_property(name, value)

        for parameter in parameters:
            algorithm.parameter_manager.add_parameter(parameter)

        solver_node = self.create_solver_node(
            parent_system=algorithm,
            parameters=parameters,
            responses=responses,
            solver_type=solver_type,
            solver_name=solver_name,
            solver_settings=solver_settings,
            solver_connections=connections_solver,
        )

        for criterion in criteria:
            algorithm.criteria_manager.add_criterion(criterion)

        # TODO: implement `set_start_designs` command
        # for start_design in start_designs:
        #     algorithm.design_manager.set_start_design()
        return algorithm, solver_node

    def create_solver_node(
        self,
        parent_system: ParametricSystem,
        parameters: Iterable[Parameter],
        responses: Iterable[Response],
        solver_type: nt.NodeType,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        solver_connections: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
    ) -> IntegrationNode:  # pragma: no cover
        """Create solver node inside the provided parent parametric system.

        Parameters
        ----------
        parent_system : ParametricSystem
            Parent system to create solver node.
        parameters: Iterable[Parameter]
            Registered parameters of the solver node.
        responses : Iterable[Response]
            Registered responses of the solver node.
        solver_type: nt.NodeType
            The type of solver to create. Supported types are ``nt.Mopsolver``.
        solver_name : Optional[str], optional
            Solver node name.
        solver_settings : Optional[GeneralSolverNodeSettings], optional
            Solver node settings.
        solver_connections: Optional[Iterable[Tuple[OutputSlot, str]]]
            Iterable of tuples specifying the connection from each predecessor node to the
            new solver node.

        Returns
        -------
        IntegrationNode
            The created solver node.
        """
        solver_node = parent_system.create_node(
            type_=solver_type, name=solver_name, design_flow=DesignFlow.RECEIVE_SEND
        )
        assert isinstance(solver_node, IntegrationNode)

        # Connect each predecessor if both lists are provided and lengths match
        if solver_connections:
            for output_slot, input_slot_str in solver_connections:
                output_slot.connect_to(solver_node.get_input_slots(name=input_slot_str)[0])

        settings_dict = (
            solver_settings.convert_properties_to_dict()
            if isinstance(solver_settings, GeneralNodeSettings)
            else {}
        )
        for name, value in settings_dict.items():
            solver_node.set_property(name, value)

        # use custom method to register parameters and responses
        # TODO: Reimplement registration of locations, when convenience module for registration
        # of locations is introduced. For now, only ProxySolver and Mopsolver is implemented.
        if solver_node.type == nt.ProxySolver:
            assert isinstance(solver_node, ProxySolverNode)
            self.__register_proxy_solver_locations(solver_node, parameters, responses)
        elif solver_node.type == nt.Mopsolver:
            self.__register_mop_solver_locations(solver_node, parameters, responses)
        elif solver_node.type == nt.CalculatorSet:
            # TODO: implement
            pass
        elif solver_node.type == nt.Python2:
            # TODO: implement
            pass
        elif solver_node.type == nt.PythonScript:
            # TODO: implement
            pass
        elif solver_node.type == nt.Process:
            # TODO: implement
            pass
        else:
            self.__register_integration_node_locations(solver_node)
        return solver_node

    def __register_proxy_solver_locations(
        self,
        solver_node: ProxySolverNode,
        parameters: Iterable[Parameter],
        responses: Iterable[Response],
    ) -> None:
        """Register proxy solver node locations.

        Parameters
        ----------
        solver_node : ProxySolverNode
            Instance of the proxy solver node.
        parameters : Iterable[Parameter]
            Parameter to be registered.
        responses: Iterable[Response]
            Responses to be registered.
        """
        load_json: dict[str, Any] = {}
        load_json["parameters"] = []
        load_json["responses"] = []
        for parameter in parameters:
            load_json["parameters"].append(
                {
                    "dir": {"value": "input"},
                    "name": parameter.name,
                    "value": parameter.reference_value,
                }
            )
        for response in responses:
            load_json["responses"].append(
                {
                    "dir": {"value": "output"},
                    "name": response.name,
                    "value": response.reference_value,
                }
            )

        solver_node.load(args=load_json)
        solver_node.register_locations_as_parameter()
        solver_node.register_locations_as_response()

    def __register_mop_solver_locations(
        self,
        solver_node: IntegrationNode,
        parameters: Iterable[Parameter],
        responses: Iterable[Response],
    ) -> None:
        """Register mop solver node locations.

        Parameters
        ----------
        solver_node : IntegrationNode
            Instance of the mop solver node.
        parameters : Iterable[Parameter]
            Parameter to be registered.
        responses: Iterable[Response]
            Responses to be registered.
        """
        base = next(iter(parameters))
        for parameter in parameters:
            location = {
                "base": base.name,
                "dir": {"enum": ["input", "output"], "value": "input"},
                "id": parameter.name,
                "suffix": "",
                "value_type": {
                    "enum": ["value", "cop", "rmse", "error", "abs_error", "density"],
                    "value": "value",
                },
            }
            solver_node.register_location_as_parameter(
                location, parameter.name, parameter.reference_value
            )
        for response in responses:
            location = {
                "base": response.name,
                "dir": {"value": "output"},
                "id": response.name,
                "suffix": "",
                "value_type": {"value": "value"},
            }
            solver_node.register_location_as_response(
                location, reference_value=response.reference_value
            )

    def __register_integration_node_locations(self, solver_node: IntegrationNode) -> None:
        """Register integration node locations using `load` method.

        Parameters
        ----------
        solver_node : IntegrationNode
            Instance of the integration_node.
        """
        solver_node.load()


class ParametricSystemIntegrationTemplate(WorkFlowTemplate):
    """Template for parametric system with integration node solver."""

    def __init__(
        self,
        parameters: Iterable[Parameter],
        solver_type: nt.NodeType,
        parametric_system_name: Optional[str] = None,
        parametric_system_settings: Optional[GeneralAlgorithmSettings] = None,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        start_designs: Iterable[Design] = [],
        algorithm_connections: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
        solver_connections: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
        criteria: Optional[Iterable[Criterion]] = None,
    ):
        """Initialize the ParametricSystemTemplate.

        Parameters
        ----------
        parameters : Iterable[Parameter]
            Parameters to be included in the parametric system.
        solver_type : nt.NodeType
            The type of solver node to generate. Must be integration node.
        parametric_system_name : Optional[str], optional
            Optional name or ID for the parametric system.
        parametric_system_settings : Optional[GeneralAlgorithmSettings], optional
            Settings for the parametric system.
        solver_name : Optional[str], optional
            Name for the solver node.
        solver_settings : Optional[GeneralSolverNodeSettings], optional
            Settings for the solver node.
        start_designs : Iterable[Design], optional
            Designs to be used as start designs for the parametric system.
        algorithm_connections : Optional[Iterable[Tuple[OutputSlot, str]]], optional
            Iterable of tuples specifying the connections to the new parametric system.
        solver_connections : Optional[Iterable[Tuple[OutputSlot, str]]], optional
            Iterable of tuples specifying the connections to the new solver node.
        criteria: Optional[Iterable[Criterion]], optional
            Iterable of criteria.
        """
        self.parameters = parameters
        self.responses: Iterable[Response] = []
        self.solver_type = solver_type
        self.criteria: Iterable[Criterion] = criteria if criteria is not None else []
        self.parametric_system_name = parametric_system_name
        self.parametric_system_settings = parametric_system_settings
        self.solver_name = solver_name
        self.solver_settings = solver_settings
        self.start_designs = start_designs
        self.algorithm_connections = algorithm_connections
        self.solver_connections = solver_connections

    def create_workflow(
        self, parent: ParametricSystem
    ) -> Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]:
        """Create the workflow template.

        Parameters
        ----------
        parent : ParametricSystem
            Parent system to create the workflow in.
        Returns
        -------
        Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]
            Tuple of managed instances and executable blocks.
        """
        parametric_system, solver_node = self.create_algorithm(
            parent_system=parent,
            parameters=self.parameters,
            criteria=self.criteria,
            responses=self.responses,
            algorithm_type=nt.ParametricSystem,
            solver_type=self.solver_type,
            algorithm_name=self.parametric_system_name,
            algorithm_settings=self.parametric_system_settings,
            solver_name=self.solver_name,
            solver_settings=self.solver_settings,
            start_designs=self.start_designs,
            connections_algorithm=self.algorithm_connections,
            connections_solver=self.solver_connections,
        )
        instance = ManagedParametricSystem(
            parametric_system=parametric_system, solver_node=solver_node
        )
        executable_block = ExecutableBlock(
            (
                (
                    instance,
                    ExecutionOption.ACTIVE
                    | ExecutionOption.STARTING_POINT
                    | ExecutionOption.END_POINT,
                ),
            )
        )
        return ((instance,), (executable_block,))


class GeneralAlgorithmTemplate(WorkFlowTemplate):
    """Template for general algorithm."""

    def __init__(
        self,
        parameters: Iterable[Parameter],
        criteria: Iterable[Criterion],
        responses: Iterable[Response],
        algorithm_type: nt.NodeType,
        solver_type: nt.NodeType,
        algorithm_name: Optional[str] = None,
        algorithm_settings: Optional[GeneralAlgorithmSettings] = None,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        start_designs: Optional[Iterable[Design]] = None,
        algorithm_connections: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
        solver_connections: Optional[Iterable[Tuple[OutputSlot, str]]] = None,
    ):
        """Initialize the GeneralAlgorithmWorkflow.

        Parameters
        ----------
        parameters : Iterable[Parameter]
                Parameters to be included in the algorithm.
        criteria : Iterable[Criterion]
            Criteria to be included in the algorithm.
        responses : Iterable[Response]
            Responses to be included in the algorithm.
        algorithm_type : NodeType
            The type of algorithm to generate.
        solver_type : NodeType, optional
            The type of solver node to generate.
            Currently supported types are ``nt.Mopsolver`` and ``nt.ProxySolver``.
        algorithm_name : Optional[str], optional
            Optional name or ID for the algorithm.
        algorithm_settings : Optional[GeneralAlgorithmSettings], optional
            Settings for the algorithm. Settings must be compatible with
            the selected algorithm type.
        solver_name : Optional[str], optional
            Name for the solver node.
        solver_settings : Optional[GeneralSolverNodeSettings], optional
            Settings for the solver node. Settings must be compatible with
            the selected solver type.
        start_designs : Optional[Iterable[Design]], optional
            Designs to be used as start designs for the algorithm.
        algorithm_connections: Optional[Iterable[Tuple[OutputSlot, str]]], optional
            Iterable of tuples specifying the connections to the
            new algorithm.
        solver_connections: Optional[Iterable[Tuple[OutputSlot, str]]], optional
            Iterable of tuples specifying the connections to the
            new solver node.
        """
        self.parameters = parameters
        self.criteria = criteria
        self.responses = responses
        self.algorithm_type = algorithm_type
        self.algorithm_name = algorithm_name
        self.algorithm_settings = algorithm_settings
        self.solver_type = solver_type
        self.solver_name = solver_name
        self.solver_settings = solver_settings
        self.start_designs = start_designs
        self.algorithm_connections = algorithm_connections
        self.solver_connections = solver_connections

    def create_workflow(
        self, parent: ParametricSystem
    ) -> Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]:
        """Create the workflow template.

        Parameters
        ----------
        parent : ParametricSystem
            Parent system to create the workflow in.

        Returns
        -------
        Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]
            Tuple of managed instances and executable blocks.
        """
        algorithm, solver_node = self.create_algorithm(
            parent_system=parent,
            parameters=self.parameters,
            criteria=self.criteria,
            responses=self.responses,
            algorithm_type=self.algorithm_type,
            solver_type=self.solver_type,
            algorithm_name=self.algorithm_name,
            algorithm_settings=self.algorithm_settings,
            solver_name=self.solver_name,
            solver_settings=self.solver_settings,
            start_designs=self.start_designs,
            connections_algorithm=self.algorithm_connections,
            connections_solver=self.solver_connections,
        )
        instance: ManagedInstance
        if self.solver_type == nt.ProxySolver:
            if not isinstance(self.solver_settings, ProxySolverNodeSettings):
                raise TypeError(
                    "Incompatible settings. For ``ProxySolver`` node, "
                    "solver_settings must be of type ``ProxySolverNodeSettings``."
                )
            assert isinstance(solver_node, ProxySolverNode)
            instance = ProxySolverManagedParametricSystem(
                algorithm=algorithm,
                solver_node=solver_node,
                callback=self.solver_settings.callback,
            )
        else:
            instance = ManagedParametricSystem(parametric_system=algorithm, solver_node=solver_node)

        executable_block = ExecutableBlock(
            (
                (
                    instance,
                    ExecutionOption.ACTIVE
                    | ExecutionOption.STARTING_POINT
                    | ExecutionOption.END_POINT,
                ),
            )
        )
        return ((instance,), (executable_block,))


class OptimizationOnMOPTemplate(WorkFlowTemplate):
    """Template creating optimization on MOP and validation with proxy solver.

    Workflow:
    - Optimizer:
        - Algorithm using MopSolver node as solver, OCO algorithm by default.
    - Validator:
        - Parametric system validating best designs using ProxySolver node.
    """

    def __init__(
        self,
        parameters: Iterable[Parameter],
        criteria: Iterable[Criterion],
        responses: Iterable[Response],
        mop_predecessor: Node,
        optimizer_name: Optional[str] = None,
        optimizer_type: nt.NodeType = nt.OCO,
        optimizer_start_designs: Optional[Iterable[Design]] = None,
        callback: Optional[Callable] = None,
        best_designs_num: int = 1,
    ):
        """Initialize the OptimizationOnMOPTemplate.

        Parameters
        ----------
        parameters : Iterable[Parameter]
            Parameters to be used by optimization algorithm and validator.
        criteria : Iterable[Criterion]
            Criteria to be used by optimization algorithm and validator.
        responses : Iterable[Response]
            Responses to be used by optimization algorithm and validator.
        mop_predecessor: Node
            Predecessor of the workflow. Must be either MOP node or AMOP system.
        optimizer_name: Optional[str]
            Name of the optimization algorithm.
        optimizer_type: nt.NodeType
            Type of the optimization algorithm, by default OCO.
        optimizer_start_designs: Iterable[Design]
            Start designs.
        callback: Optional[Callable]
            ProxySolver node callback processing designs.
            MUST be specified to allow automatic execution. If not specified,
            execution of the proxy solver must be performed by the user.
        best_designs_num: int, optional
            Number of best designs to be filtered. By default ``1``.
        """
        self.parameters = parameters
        self.criteria = criteria
        self.responses = responses
        self.mop_predecessor = mop_predecessor
        self.optimizer_name = optimizer_name
        self.optimizer_type = optimizer_type
        self.optimizer_start_designs = optimizer_start_designs
        if not callback:
            self.validator_solver_settings = ProxySolverNodeSettings(self.__class__._empty_callback)
            warnings.warn("Callback was not provided, automatic execution won't be possible.")
        else:
            self.validator_solver_settings = ProxySolverNodeSettings(callback=callback)
        self.best_designs_num = best_designs_num

    def create_workflow(
        self, parent: ParametricSystem
    ) -> Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]:
        """Create the workflow template.

        Parameters
        ----------
        parent : ParametricSystem
            Parent system to create the workflow in.

        Returns
        -------
        Tuple[Tuple[ManagedInstance, ...], Tuple[ExecutableBlock, ...]]
            Tuple of managed instances and executable blocks.
        """
        # optimizer
        optimizer_algorithm, optimizer_solver_node = self.create_algorithm(
            parent_system=parent,
            parameters=self.parameters,
            criteria=self.criteria,
            responses=self.responses,
            algorithm_type=self.optimizer_type,
            solver_type=nt.Mopsolver,
            algorithm_name=self.optimizer_name,
            start_designs=self.optimizer_start_designs,
            connections_algorithm=[
                (self.mop_predecessor.get_output_slots("OParameterManager")[0], "IParameterManager")
            ],
            connections_solver=[
                (self.mop_predecessor.get_output_slots("OMDBPath")[0], "IMDBPath"),
            ],
        )
        optimizer_managed_instance = ManagedParametricSystem(
            parametric_system=optimizer_algorithm, solver_node=optimizer_solver_node
        )

        # validator
        validator_settings = GeneralAlgorithmSettings()
        validator_settings.additional_settings["DynamicSamplingDesired"] = False
        validator_system, validator_solver_node = self.create_algorithm(
            parent_system=parent,
            parameters=self.parameters,
            criteria=self.criteria,
            responses=self.responses,
            algorithm_type=nt.Sensitivity,
            solver_type=nt.ProxySolver,
            algorithm_settings=validator_settings,
            solver_settings=self.validator_solver_settings,
            connections_algorithm=[
                (optimizer_algorithm.get_output_slots("OCriteria")[0], "ICriteria")
            ],
            connections_solver=[],
        )
        assert isinstance(validator_solver_node, ProxySolverNode)
        validator_managed_instance = ProxySolverManagedParametricSystem(
            algorithm=validator_system,
            solver_node=validator_solver_node,
            callback=self.validator_solver_settings.callback,
        )

        # filter
        filter_node = parent.create_node(type_=nt.DataMining, name="VALIDATOR_FILTER_NODE")
        assert isinstance(filter_node, IntegrationNode)
        filter_node.create_input_slot("IBestDesigns", SlotTypeHint.DESIGN_CONTAINER)
        filter_node_managed_instance = ManagedInstance(filter_node)
        optimizer_algorithm.get_output_slots("OBestDesigns")[0].connect_to(
            filter_node.get_input_slots("IBestDesigns")[0]
        )

        ofilter = {
            "OFilteredBestDesigns": [
                {
                    "First": {"name": "AddDesignsFromSlot"},
                    "Second": [
                        {"design_container": []},
                        {"string": "IBestDesigns"},
                        {"design_entry": False},
                    ],
                }
            ]
        }
        dmm = filter_node.get_property("DataMiningManager")
        dmm["id_filter_list_map"] = ofilter
        filter_node.set_property("DataMiningManager", dmm)

        getbestdesigns = {
            "First": {"name": "GetBestDesigns"},
            "Second": [{"design_container": []}, {"design_entry": self.best_designs_num}],
        }

        dmm = filter_node.get_property("DataMiningManager")
        dmm["id_filter_list_map"]["OFilteredBestDesigns"].append(getbestdesigns)
        filter_node.set_property("DataMiningManager", dmm)

        filter_node.load()
        filter_node.register_location_as_output_slot(
            location="OFilteredBestDesigns", name="OFilteredBestDesigns"
        )
        filter_node.get_output_slots("OFilteredBestDesigns")[0].connect_to(
            validator_system.get_input_slots("IStartDesigns")[0]
        )

        # design filter
        append_node = parent.create_node(type_=nt.DataMining, name="Append Designs")
        assert isinstance(append_node, IntegrationNode)
        append_node.create_input_slot("IDesigns", SlotTypeHint.DESIGN_CONTAINER)
        append_node.create_input_slot("IPath", SlotTypeHint.PATH)
        append_node_managed_instance = ManagedInstance(append_node)

        ofilter = {
            "OValidatedMDBPath": [
                {
                    "First": {"name": "AppendDesignsToFile"},
                    "Second": [
                        {"design_container": []},
                        {"string": "IDesigns"},
                        {"string": "IPath"},
                    ],
                }
            ]
        }
        dmm = append_node.get_property("DataMiningManager")
        dmm["id_filter_list_map"] = ofilter
        append_node.set_property("DataMiningManager", dmm)
        append_node.load()
        append_node.register_location_as_output_slot(
            location="OValidatedMDBPath", name="OValidatedMDBPath"
        )

        validator_system.get_output_slots("ODesigns")[0].connect_to(
            append_node.get_input_slots("IDesigns")[0]
        )
        optimizer_algorithm.get_output_slots("OMDBPath")[0].connect_to(
            append_node.get_input_slots("IPath")[0]
        )
        # postprocessing
        postprocessing_node: Node = parent.create_node(
            type_=nt.Postprocessing, name="PostProcessing"
        )
        postprocessing_managed_instance = ManagedInstance(postprocessing_node)

        append_node.get_output_slots("OValidatedMDBPath")[0].connect_to(
            postprocessing_node.get_input_slots("IMDBPath")[0]
        )

        # create executable blocks from the nodes
        managed_instances = (
            optimizer_managed_instance,
            filter_node_managed_instance,
            validator_managed_instance,
            append_node_managed_instance,
            postprocessing_managed_instance,
        )
        executable_blocks = (
            ExecutableBlock(
                (
                    (
                        optimizer_managed_instance,
                        ExecutionOption.ACTIVE
                        | ExecutionOption.STARTING_POINT
                        | ExecutionOption.END_POINT,
                    ),
                )
            ),
            ExecutableBlock(
                (
                    (
                        filter_node_managed_instance,
                        ExecutionOption.ACTIVE | ExecutionOption.STARTING_POINT,
                    ),
                    (
                        validator_managed_instance,
                        ExecutionOption.ACTIVE | ExecutionOption.END_POINT,
                    ),
                )
            ),
            ExecutableBlock(
                (
                    (
                        append_node_managed_instance,
                        ExecutionOption.ACTIVE | ExecutionOption.STARTING_POINT,
                    ),
                    (
                        postprocessing_managed_instance,
                        ExecutionOption.ACTIVE | ExecutionOption.END_POINT,
                    ),
                )
            ),
        )
        return (managed_instances, tuple(executable_blocks))

    @staticmethod
    def _empty_callback(designs: List[dict]) -> List[dict]:
        """Empty callback to be used, if not provided by the user."""
        results_designs = []
        for design in designs:
            results_designs.append(
                {
                    "hid": design["hid"],
                }
            )
        return results_designs


# endregion


# region helper functions
def go_to_optislang(
    project_path: Union[str, Path],
    connector_type: nt.NodeType,
    omdb_files: Union[Union[str, Path], List[Union[str, Path]], ParametricDesignStudyManager],
    parameters: Optional[Iterable[Parameter]] = None,
    connector_settings: Optional[GeneralNodeSettings] = None,
) -> Optislang:  # pragma: no cover
    """Generate a new optiSLang project with a parametric system and launch in GUI mode.

    Parameters
    ----------
    project_path: Union[str,Path]
        Path to save the generated optiSLang project file.
    connector_type : str
        The type of connector actor.
    omdb_files : Union[Union[str, Path], List[Union[str, Path]], BaseSolverManager]
        OMDB files to include in the project. Can be a path to a folder,
        a list of paths, or an instance of ``BaseSolverManager``.
    parameters: Optional[Iterable[Parameter]], optional
        Parameters to be included in the parametric system, by default `None`.
    connector_settings : Optional[GeneralNodeSettings], optional
        Settings for the connector actor, by default `None`.

    Returns
    -------
    Path
        The path to the generated optiSLang project file.
    """
    create_optislang_project_with_solver_node(
        project_path, connector_type, omdb_files, parameters, connector_settings
    )
    osl = Optislang(project_path=project_path, batch=False)
    return osl


def create_optislang_project_with_solver_node(
    project_path: Union[str, Path],
    connector_type: nt.NodeType,
    omdb_files: Union[Union[Path, str], List[Union[Path, str]], ParametricDesignStudyManager],
    parameters: Optional[Iterable[Parameter]],
    connector_settings: Optional[GeneralNodeSettings],
) -> None:
    """Generate a new optiSLang project with a parametric system and specified connector.

    Parameters
    ----------
    project_path: Union[str,Path]
        Path to save the generated optiSLang project file.
    connector_type : NodeType
        The type of connector actor.
    omdb_files : Union[Union[str, Path], List[Union[str, Path]], ParametricDesignStudyManager]
        OMDB files to include in the project. Can be a path to a folder,
        a list of paths, or an instance of `ParametricDesignStudyManager`.
    parameters: Optional[Iterable[Parameter]], optional
        Parameters to be included in the parametric system, by default `None`.
    connector_settings : Optional[GeneralSolverNodeSettings], optional
        Settings for the connector actor, by default `None`.
    """
    with Optislang(project_path=project_path) as osl:
        omdb_files_provider = OMDBFilesProvider(omdb_files)
        omdb_paths = omdb_files_provider.get_omdb_files()
        ref_dir = osl.application.project.get_reference_dir()
        for path in omdb_paths:
            parts = path.parts
            for i, part in enumerate(parts):
                if part.endswith(".opd"):
                    relpath = Path(*parts[i + 1 :])  # everything after the .opd dir
                    break
            reldirs = relpath.parts[0:-1]
            if reldirs:
                reldirs_full = ref_dir / relpath.parent
                if not reldirs_full.exists():
                    os.makedirs(reldirs_full)
            target = ref_dir / relpath
            shutil.copy(path, target)

        template = ParametricSystemIntegrationTemplate(
            parameters=parameters if parameters is not None else [],
            solver_type=connector_type,
            solver_name="Connector",
            solver_settings=connector_settings,
        )

        template.create_workflow(osl.application.project.root_system)
        osl.application.save()


def create_workflow_from_template(
    template: WorkFlowTemplate,
    project_path: Optional[Union[str, Path]] = None,
) -> Optislang:
    """Generate a new optiSLang project with a workflow based on the provided template.

    Parameters
    ----------
    template : WorkFlowTemplate
        The workflow template to use.

    Returns
    -------
    Optislang
        The instance of ``Optislang`` with the generated workflow.
    """
    osl = Optislang(project_path=project_path)
    assert osl.application.project is not None
    template.create_workflow(osl.application.project.root_system)
    return osl


# endregion
