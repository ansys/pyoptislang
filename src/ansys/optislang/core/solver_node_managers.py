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

"""Contains classes managing algorithms with solver nodes and helper functions."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
import shutil
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import (
    DesignFlow,
    ExecutionOption,
    IntegrationNode,
    Node,
    ParametricSystem,
    ProxySolverNode,
    RootSystem,
)

if TYPE_CHECKING:
    from ansys.optislang.core.io import File
    from ansys.optislang.core.project_parametric import (
        Criterion,
        Design,
        Parameter,
        Response,
        VariableCriterion,
    )


class OMDBFilesSpecificationEnum(Enum):
    """Enumeration of possible specifications of the OMDB files."""

    OMDB_FILES = 0
    OMDB_FOLDER = 1
    SOLVER_MANAGER = 3
    UNDEFINED = 4


class OMDBFilesProvider:
    """Provides OMDB to be included in the project."""

    @property
    def omdb_files_specification(self) -> OMDBFilesSpecificationEnum:
        """Specification of the OMDB files.

        Returns
        -------
        OMDBFilesSpecificationEnum
            The specification of the OMDB files.
        """
        return self.__omdb_files_specification

    @property
    def input(self) -> Union[Union[Path, str], Union[List[str], List[Path]], BaseSolverManager]:
        """Input specifying the OMDB files.

        Returns
        -------
        Union[Union[Path,str], Union[List[str], List[Path]], BaseSolverManager]
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of BaseSolverManager.
        """
        return self.__input

    @input.setter
    def input(
        self, value: Union[Union[Path, str], Union[List[str], List[Path]], BaseSolverManager]
    ):
        self.__input = value
        self.__omdb_files_specification = self.__class__.get_ombd_files_specification_from_input(
            value
        )

    def __init__(
        self,
        input: Optional[
            Union[Union[Path, str], Union[List[str], List[Path]], BaseSolverManager]
        ] = None,
    ):
        """Initialize the OMDBFilesProvider.

        Parameters
        ----------
        input : Optional[
                    Union[Union[Path,str],
                    Union[List[str], List[Path]],
                    BaseSolverManager]
            ], optional
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of BaseSolverManager.
        """
        self.input = input

    def get_omdb_files(self) -> Tuple[Path]:
        """Get the a tuple of OMDB files to be included in the project.

        Returns
        -------
        Tuple[Path]
            Tuple of paths to the OMDB files.
        """
        if self.omdb_files_specification == OMDBFilesSpecificationEnum.SOLVER_MANAGER:
            paths = []
            for algorithm in self.input.algorithms:
                paths.extend([file.path for file in algorithm.get_omdb_files()])
            return paths
        elif self.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FOLDER:
            folder_path = Path(self.input)
            return tuple([file for file in folder_path.rglob("*.omdb") if file.is_file()])
        elif self.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FILES:
            return tuple([Path(file) for file in self.input])
        else:
            return tuple([])

    @staticmethod
    def get_ombd_files_specification_from_input(
        input: Optional[Union[Union[Path, str], Union[List[str], List[Path]], BaseSolverManager]],
    ):
        """Determine the specification of the OMDB files based on the input.

        Parameters
        ----------
        input : Optional[Union[Union[Path, str], Union[List[str], List[Path]], BaseSolverManager]]
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of BaseSolverManager.

        Returns
        -------
        OMDBFilesSpecificationEnum
            The specification of the OMDB files.
        """
        if isinstance(input, BaseSolverManager):
            return OMDBFilesSpecificationEnum.SOLVER_MANAGER
        elif isinstance(input, (str, Path)) and Path(input).is_dir():
            return OMDBFilesSpecificationEnum.OMDB_FOLDER
        elif isinstance(input, list) and all(
            isinstance(item, (str, Path)) and Path(item).suffix == ".omdb" for item in input
        ):
            return OMDBFilesSpecificationEnum.OMDB_FILES
        else:
            return OMDBFilesSpecificationEnum.UNDEFINED


class ManagedAlgorithm(NamedTuple):
    """A named tuple representing a managed algorithm.

    Attributes
    ----------
    instance : ParametricSystem
        Instance of the managed algoritgm.
    predecessor : Dict[str, Node], optional
        Dictionary of predecessors of the managed algorithm.
    """

    instance: ParametricSystem
    predecessors: Dict[str, Node] = {}


class WorkFlowTemplate(NamedTuple):
    """Base class for optimization workflow templates.

    Attributes
    ----------
    TODO
    """

    pass


class OptimizationOnMOP(WorkFlowTemplate):
    """Optimization workflow template using MOP solver node."""

    pass


class GeneralSolverNodeSettings(NamedTuple):
    """Properties common to all solver nodes."""

    additional_settings: Optional[dict]


class PythonSolverNode(GeneralSolverNodeSettings):
    """Properties specific to Python solver nodes."""

    input: Union[File, str]


class BaseSolverManager:
    """Base class for solver managers."""

    @property
    def optislang(self) -> Optislang:
        """The optiSLang instance the manager operates on.

        Returns
        -------
        Optislang
            The optiSLang instance.
        """
        return self.__optislang

    @property
    def algorithms(self) -> Tuple[ParametricSystem, ...]:
        """Algorithms managed by the instance of SolverManager."""
        return tuple([managed_algo.instance for managed_algo in self._managed_algorithms.values()])

    @property
    def managed_algorithms(self) -> Tuple[ManagedAlgorithm]:
        """Managed algorithms with their predecessors."""
        return tuple(self._managed_algorithms.values())

    def __init__(
        self, optislang_instance: Optional[Optislang] = None, **kwargs
    ):  # pragma: no cover
        """Initialize the BaseSolverManager.

        Parameters
        ----------
        optislang_instance : Optional[Optislang]
            An existing optiSLang instance to operate on. If not provided,
            a new instance will be created.
        **kwargs
            Additional keyword arguments, used to initialize the optislang instance.
            Not used if an existing instance is provided.
        """
        if optislang_instance is None:
            self.__optislang = Optislang(**kwargs)
        else:
            self.__optislang = optislang_instance

        self._managed_algorithms: Dict[str, ManagedAlgorithm] = {}

    def add_algorithm_predecessor(
        self, algorithm: ParametricSystem, predecessor: ParametricSystem
    ) -> None:
        """Set predecessors for the specified managed algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.
        predecessors : ParametricSystem
            Instance of the predecessor algorithms.
        """
        managed_algorithm = self._managed_algorithms.get(algorithm.uid, None)
        if managed_algorithm:
            if predecessor.uid not in managed_algorithm.predecessors.keys():
                self._managed_algorithms[algorithm.uid].predecessors[predecessor.uid] = predecessor
            else:
                self.optislang.log.warning("The specified predecessor is already set.")
        else:
            self.optislang.log.warning("The specified algorithm is not managed by this instance.")

    def clear_managed_algorithms(self, delete: Optional[bool] = False) -> None:
        """Remove all algorithms managed by the instance of SolverManager.

        Parameters
        ----------
        delete: Optional[bool], optional
            If ``True``, the algorithm nodes will be deleted from the project. By default ``False``.
        """
        if delete:
            [
                managed_algorithm.instance.delete()
                for managed_algorithm in self._managed_algorithms.values()
            ]
        self._managed_algorithms.clear()

    def clear_algorithm_predecessors(self, algorithm: ParametricSystem) -> None:
        """Clear predecessors of the specified managed algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.
        """
        managed_algorithm = self._managed_algorithms.get(algorithm.uid, None)
        if managed_algorithm:
            self._managed_algorithms[algorithm.uid].predecessors.clear()
        else:
            self.optislang.log.warning("The specified algorithm is not managed by this instance.")

    def dispose(self):
        """Dispose the instance of SolverManager and close the associated optiSLang instance."""
        self._managed_algorithms.clear()
        if self.optislang:
            self.optislang.dispose()

    def is_managed_algorithm(self, algorithm: ParametricSystem) -> bool:
        """Check if the specified algorithm is managed by the instance of SolverManager.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.

        Returns
        -------
        bool
            ``True`` if the algorithm is managed, ``False`` otherwise.
        """
        return algorithm.uid in self._managed_algorithms.keys()

    def get_algorithm_designs(self, algorithm: ParametricSystem) -> Tuple[Design]:
        """Get the designs associated with the specified algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.

        Returns
        -------
        Tuple[Design]
            Tuple of designs associated with the algorithm.
        """
        designs = []
        hids = algorithm.get_states_ids()
        for hid in hids:
            designs.extend(algorithm.design_manager.get_designs(hid))
        return tuple(designs)

    def get_algorithm_predecessors(self, algorithm: ParametricSystem) -> Tuple[ParametricSystem]:
        """Get predecessors of the specified algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.

        Returns
        -------
        Tuple[ParametricSystem]
            Predecessors of the specified algorithm
        """
        managed_algorithm = self._managed_algorithms.get(algorithm.uid, None)
        if managed_algorithm and managed_algorithm.predecessors:
            return tuple(managed_algorithm.predecessors.values())

    def get_managed_algorithm_by_name(self, name: str) -> Optional[ManagedAlgorithm]:
        """Get a managed algorithm by its name.

        Parameters
        ----------
        name : str
            The name of the algorithm.

        Returns
        -------
        Optional[ManagedAlgorithm]
            The managed algorithm or None if not found.
        """
        for managed_algorithm in self._managed_algorithms.values():
            if managed_algorithm.instance.get_name() == name:
                return managed_algorithm()
        self.optislang.log.warning("The specified algorithm is not managed by this instance.")
        return None

    def get_solved_algorithms(self) -> Tuple[ParametricSystem]:
        """Get all managed algorithms that have been solved.

        Returns
        -------
        Tuple[ParametricSystem]
            Tuple of managed algorithms that have been solved.
        """
        solved_algorithms = [
            managed_algorithm.instance
            for managed_algorithm in self._managed_algorithms.values()
            if managed_algorithm.instance.get_status() == "Finished"
        ]
        return tuple(solved_algorithms)

    def get_unsolved_algorithms(self) -> Tuple[ParametricSystem]:
        """Get all managed algorithms that have not been solved.

        Returns
        -------
        Tuple[ParametricSystem]
            Tuple of managed algorithms that have not been solved.
        """
        unsolved_algorithms = [
            managed_algorithm.instance
            for managed_algorithm in self._managed_algorithms.values()
            if managed_algorithm.instance.get_status() != "Finished"
        ]
        return tuple(unsolved_algorithms)

    def remove_managed_algorithm(
        self, algorithm: ParametricSystem, delete: Optional[bool] = False
    ) -> None:
        """Remove the specified algorithm from managed algorithms.

        Parameters
        ----------
        algorithm_name: str
            Name of algorithm to be removed.
        delete: Optional[bool], optional
            If ``True``, the algorithm node will be deleted from the project. By default ``False``.
        """
        if algorithm.uid not in self._managed_algorithms.keys():
            self.optislang.log.warning("The specified algorithm is not managed by this instance.")
        else:
            self._managed_algorithms.pop(algorithm.uid)

        if delete:
            algorithm.delete()

    def remove_algorithm_predecessor(self, algorithm: ParametricSystem, predecessor: Node):
        """Remove the specified predecessor from the managed algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.
        predecessor : Node
            Instance of the predecessor node to be removed.
        """
        managed_algorithm = self._managed_algorithms.get(algorithm.uid, None)
        if managed_algorithm:
            predecessor_uids = set(
                [predecessor.uid for predecessor in managed_algorithm.predecessors]
            )
            if predecessor.uid in predecessor_uids:
                self._managed_algorithms[algorithm.uid].predecessors.remove(predecessor)
            else:
                self.optislang.log.warning("The specified predecessor is not set.")
        else:
            self.optislang.log.warning("The specified algorithm is not managed by this instance.")

    @staticmethod
    def get_algorithm_execution_order(
        managed_algorithms: Iterable[ManagedAlgorithm],
    ) -> Tuple[ParametricSystem, ...]:
        """Sort algorithms with predecessor before its dependent algorithm.

        Parameters
        ----------
        managed_algorithms : Iterable[ManagedAlgorithm]
            Iterable of managed algorithms.

        Returns
        -------
        Tuple[ParametricSystem, ...]
            Ordered tuple of managed algorithms for execution.
        """
        # Build dependency graph: key is uid, value is set of predecessor uids
        algo_dict = {algo.instance.uid: algo for algo in managed_algorithms}
        dependencies = {
            uid: set(algo.predecessors.keys()) if algo.predecessors is not None else set()
            for uid, algo in algo_dict.items()
        }

        # Kahn's algorithm for topological sort
        ordered_uids = []
        no_deps = [uid for uid, preds in dependencies.items() if not preds]
        visited = set()
        while no_deps:
            uid = no_deps.pop(0)
            if uid in visited:
                continue
            ordered_uids.append(uid)
            visited.add(uid)
            for other_uid, preds in dependencies.items():
                if uid in preds:
                    preds.remove(uid)
                    if not preds and other_uid not in visited and other_uid not in no_deps:
                        no_deps.append(other_uid)
        # If there are cycles, append remaining in original order
        for uid in algo_dict.keys():
            if uid not in ordered_uids:
                ordered_uids.append(uid)
        return tuple([algo_dict[uid].instance for uid in ordered_uids])


class MopSolverNodeManager(BaseSolverManager):
    """Class which operates with mop solver nodes."""

    def __init__(self, optislang_instance: Optional[Optislang] = None):  # pragma: no cover
        """Initialize the MopSolverManager.

        Parameters
        ----------
        optislang_instance : Optional[Optislang]
            An existing optiSLang instance to operate on. If not provided,
            a new instance will be created.
        """
        super().__init__(optislang_instance)

    def execute_algorithm(
        self,
        algorithm_name: str,
    ) -> None:
        """Execute the specified algorithm.

        Parameters
        ----------
        algorithm_name : str
            The name or ID of the algorithm to execute.
        """
        pass

    def execute_all_algorithms(self) -> None:
        """Execute all managed algorithms."""
        pass

    def _create_solver_node(
        self,
        parent_system: ParametricSystem,
        variables: VariableCriterion,
        responses: Response,
        solver_name: str,
        solver_settings: dict,
    ) -> IntegrationNode:
        """Create solver node inside the provided parent parametric system.

        Parameters
        ----------
        parent_system : ParametricSystem
            Parent system to create solver node.
        variables : VariableCriterion
            Internal variables of the solver node.
        responses : Response
            Registered responses of the solver node.
        solver_name : str
            Solver node name.
        solver_settings : dict
            Solver node settings.
        """
        pass


class ProxySolverNodeManager(BaseSolverManager):
    """Class which operate with ``ProxySolver`` nodes."""

    def __init__(self, optislang_instance=None, **kwargs):
        """Initialize the ProxySolverNodeManager.

        Parameters
        ----------
        optislang_instance : Optional[Optislang]
            An existing optiSLang instance to operate on. If not provided,
            a new instance will be created.
        **kwargs
            Additional keyword arguments, used to initialize the optislang instance.
            Not used if an existing instance is provided.
        """
        super().__init__(optislang_instance, **kwargs)

    def append_algorithm(self, algorithm: ParametricSystem) -> None:
        """Append an existing algorithm to managed algorithms.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the algorithm to be managed. Algorithm must contain a single
            ``ProxySolver`` node and manages execution of this ProxySolver node exclusively.
            If multiple nodes are present, these must be preset and executable automatically.
        """
        if algorithm.uid in self._managed_algorithms.keys():
            self.optislang.log.warning("The specified algorithm is already managed.")

        # check that algorithm contains a single ProxySolver node
        solver_nodes = [node for node in algorithm.get_nodes() if node.type == nt.ProxySolver]
        if len(solver_nodes) != 1:
            self.optislang.log.error(
                "The specified algorithm must contain a single 'ProxySolver' node."
            )
            return

        managed_algorithm = ManagedAlgorithm(algorithm, {})

        # check for managed predecessors
        predecessor_dict = {}
        for input_slot in algorithm.get_input_slots():
            for connection in input_slot.get_connections():
                predecessor_instance: Node = connection.from_slot.node
                if predecessor_instance.uid in self._managed_algorithms.keys():
                    managed_algorithm.predecessors[predecessor_instance.uid] = predecessor_instance

        self._managed_algorithms[algorithm.uid] = managed_algorithm

    def create_algorithm(
        self,
        parameters: Iterable[Parameter],
        criteria: Iterable[Criterion],
        responses: Iterable[Response],
        algorithm_type: nt.NodeType,
        algorithm_name: Optional[str] = None,
        algorithm_settings: Optional[Dict[str, Any]] = {},
        solver_name: Optional[str] = None,
        solver_settings: Optional[dict] = {},
        start_designs: Iterable[Design] = [],
        predecessors: Optional[Iterable[ParametricSystem]] = None,
        predecessor_connections: Optional[Iterable[Tuple[str, str]]] = None,
    ) -> ParametricSystem:
        """Create an algorithm system with solver node and append to managed algorithms.

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
        algorithm_name : Optional[str], optional
            Optional name or ID for the algorithm.
        algorithm_settings : Optional[Dict[str, Any]], optional
            Additional settings for the algorithm. Settings must be compatible with
            the selected algorithm type. Dictionary of properties reflecting
            the properties of the node are expected.
        solver_name : Optional[str], optional
            Name for the solver node.
        solver_settings : Optional[dict], optional
            Additional settings for the solver node.
        start_designs : Iterable[Design], optional
            Designs to be used as start designs for the algorithm.
        predecessors : Optional[Iterable[ParametricSystem]], optional
            Iterable of predecessor algorithm instances, if any.
            Must be provided in combination with predecessor_connections, ignored otherwise.
        predecessor_connections: Optional[Iterable[Tuple[str, str]]], optional
            Iterable of tuples specifying the connection from each predecessor node to the
            new algorithm. Must be provided in combination with predecessors, ignored otherwise.
            E.g. ("OBestDesigns", "IStartDesigns").

        Returns
        -------
        ParametricSystem
            The created algorithm system.
        """
        algorithm: ParametricSystem = self.optislang.application.project.root_system.create_node(
            type_=algorithm_type, name=algorithm_name
        )
        # Store predecessors as a dict {uid: instance}
        predecessor_dict = {}
        if predecessors:
            for pred in predecessors:
                predecessor_dict[pred.uid] = pred
        self._managed_algorithms[algorithm.uid] = ManagedAlgorithm(algorithm, predecessor_dict)

        # Connect each predecessor if both lists are provided and lengths match
        if (
            predecessors
            and predecessor_connections
            and len(predecessors) == len(predecessor_connections)
        ):
            for pred, conn in zip(predecessors, predecessor_connections):
                predecessor_instance: Node = (
                    self.optislang.application.project.root_system.find_node_by_uid(pred.uid)
                )
                predecessor_instance.get_output_slots(name=conn[0])[0].connect_to(
                    algorithm.get_input_slots(name=conn[1])[0]
                )

        for name, value in algorithm_settings.items():
            algorithm.set_property(name, value)

        for parameter in parameters:
            algorithm.parameter_manager.add_parameter(parameter)

        self._create_solver_node(algorithm, parameters, responses, solver_name, solver_settings)

        for criterion in criteria:
            algorithm.criteria_manager.add_criterion(criterion)

        # TODO: implement `set_start_designs` command
        # for start_design in start_designs:
        #     algorithm.design_manager.set_start_design()
        algorithm.set_execution_options(ExecutionOption.INACTIVE)
        return algorithm

    def execute_algorithm(
        self,
        algorithm: ParametricSystem,
        callback: callable,
    ) -> None:
        """Execute the specified algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm to execute.
        callback : callable
            A callback function to handle design evaluation results.
        """
        # Check if predecessor exists and was solved before executing this algorithm
        managed_algo = self._managed_algorithms[algorithm.uid]
        if managed_algo and managed_algo.predecessors:
            for predecessor_algo in managed_algo.predecessors.values():
                status = predecessor_algo.get_status()
                if status != "Processing done":
                    self.optislang.log.warning(
                        f"Predecessor algorithm '{predecessor_algo.get_name()}' is not solved yet, "
                        + f"status: '{status}'."
                    )
                    return
        algorithm.set_execution_options(
            ExecutionOption.ACTIVE | ExecutionOption.STARTING_POINT | ExecutionOption.END_POINT
        )

        # Find the solver node in the algorithm, it must contain a single proxy solver node
        for node in algorithm.get_nodes():
            if node.type == nt.ProxySolver:
                solver: ProxySolverNode = node
                break
        if not solver:
            self.optislang.log.error("No ``ProxySolver`` node found in the specified algorithm.")
            return
        self.optislang.application.project.start(wait_for_finished=False)
        while True:
            status = self.optislang.application.project.get_status()
            if status == "FINISHED":
                self.optislang.log.info(f"Project status: {status}")
                break
            elif status == "STOPPED":
                self.optislang.log.info(f"Project status: {status}")
                break
            design_list = solver.get_designs()
            if len(design_list):
                responses_dict = callback(design_list)
                solver.set_designs(responses_dict)
            time.sleep(0.5)
        algorithm.set_execution_options(ExecutionOption.INACTIVE)

    def execute_all_algorithms(self, callback: callable) -> None:
        """Execute all managed algorithms.

        Parameters
        ----------
        callback : Optional[callable]
            A callback function to handle design evaluation results.
        """
        order = self.get_algorithm_execution_order()
        for algorithm in order:
            self.execute_algorithm(algorithm, callback)

    def _create_solver_node(
        self,
        parent_system: ParametricSystem,
        parameters: Iterable[Parameter],
        responses: Iterable[Response],
        solver_name: Optional[str] = None,
        solver_settings: Optional[dict] = {},
    ) -> ProxySolverNode:  # pragma: no cover
        """Create solver node inside the provided parent parametric system.

        Parameters
        ----------
        parent_system : ParametricSystem
            Parent system to create solver node.
        parameters: Iterable[Parameter]
            Registered parameters of the solver node.
        responses : Iterable[Response]
            Registered responses of the solver node.
        solver_name : Optional[str], optional
            Solver node name.
        solver_settings : Optional[dict], optional
            Solver node settings.
        """
        solver_node: IntegrationNode = parent_system.create_node(
            type_=nt.ProxySolver, name=solver_name, design_flow=DesignFlow.RECEIVE_SEND
        )
        for name, value in solver_settings.items():
            solver_node.set_property(name, value)

        for parameter in parameters:
            location = {
                "dir": {"value": "input"},
                "name": parameter.name,
                "value": parameter.reference_value,
            }
            solver_node.register_location_as_parameter(location=location)

        for response in responses:
            location = {
                "dir": {"value": "input"},
                "name": response.name,
                "value": response.reference_value,
            }
            solver_node.register_location_as_response(location=location)


def go_to_optislang(
    project_path: Union[str, Path],
    connector_type: nt.NodeType,
    connector_settings: dict,
    omdb_files: Union[Union[str, Path], List[Union[str, Path]], BaseSolverManager],
    parameters: Iterable[Parameter],
) -> Optislang:
    """Generate a new optiSLang project with a parametric system and launch in GUI mode.

    Parameters
    ----------
    project_path: Union[str,Path]
        Path to save the generated optiSLang project file.
    connector_type : str
        The type of connector actor.
    connector_settings : dict
        Settings for the connector actor.
    omdb_files : Union[Union[str, Path], List[Union[str, Path]], BaseSolverManager]
        OMDB files to include in the project. Can be a path to a folder,
        a list of paths, or an instance of ``BaseSolverManager``.
    parameters: Iterable[Parameter]
        Parameters to be included in the parametric system.

    Returns
    -------
    Path
        The path to the generated optiSLang project file.
    """
    create_optislang_project_with_solver_node(
        project_path, connector_type, connector_settings, omdb_files, parameters
    )
    osl = Optislang(project_path=project_path, batch=False)
    return osl


def create_optislang_project_with_solver_node(
    project_path: Union[str, Path],
    connector_type: nt.NodeType,
    connector_settings: GeneralSolverNodeSettings,
    omdb_files: Union[Union[str, Path], List[Union[str, Path]], BaseSolverManager],
    parameters: Iterable[Parameter],
) -> None:
    """Generate a new optiSLang project with a parametric system and specified connector.

    Parameters
    ----------
    project_path: Union[str,Path]
        Path to save the generated optiSLang project file.
    connector_type : NodeType
        The type of connector actor.
    connector_settings : GeneralSolverNodeSettings
        Settings for the connector actor.
    omdb_files : Union[Union[str, Path], List[Union[str, Path]], BaseSolverManager]
        OMDB files to include in the project. Can be a path to a folder,
        a list of paths, or an instance of ``BaseSolverManager``.
    parameters: Iterable[Parameter]
        Parameters to be included in the parametric system.
    """
    with Optislang(project_path=project_path) as osl:
        omdb_files_provider = OMDBFilesProvider(omdb_files)
        omdb_files = omdb_files_provider.get_omdb_files()
        # TODO: implement `get_reference_dir` in project class
        ref_dir = str(osl.application.project.get_working_dir()).replace(".opd", ".opr")
        # TODO: copy to ref dir as a relative path to the original working directory
        for file in omdb_files:
            shutil.copy(file, ref_dir)
        root_system: RootSystem = osl.application.project.root_system
        parametric_system: ParametricSystem = root_system.create_node(type_=nt.ParametricSystem)
        for parameter in parameters:
            parametric_system.parameter_manager.add_parameter(parameter)

        connector: IntegrationNode = parametric_system.create_node(
            type_=connector_type, design_flow=DesignFlow.RECEIVE_SEND
        )
        for name, value in connector_settings._asdict().items():
            if name != "additional_settings":
                connector.set_property(name, value)
            else:
                for setting_name, setting_value in value.items():
                    connector.set_property(setting_name, setting_value)
        connector.load()
        osl.application.save()


def create_workflow_from_template(
    template: WorkFlowTemplate,
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
    pass
