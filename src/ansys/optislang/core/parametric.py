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
import time
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

from ansys.optislang.core import Optislang
from ansys.optislang.core.nodes import (
    ExecutionOption,
    IntegrationNode,
    Node,
    ParametricSystem,
    ProxySolverNode,
    SlotType,
)

if TYPE_CHECKING:
    from ansys.optislang.core.project_parametric import (
        Design,
    )
    from ansys.optislang.core.workflow_templates import WorkFlowTemplate


# region OMDB files
class OMDBFilesSpecificationEnum(Enum):
    """Enumeration of possible specifications of the OMDB files."""

    OMDB_FILES = 0
    OMDB_FOLDER = 1
    STUDY_MANAGER = 3
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
    def input(
        self,
    ) -> Union[Union[Path, str], Union[List[str], List[Path]], ParametricDesignStudyManager]:
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
        self,
        value: Union[Union[Path, str], Union[List[str], List[Path]], ParametricDesignStudyManager],
    ):
        self.__input = value
        self.__omdb_files_specification = self.__class__.get_ombd_files_specification_from_input(
            value
        )

    def __init__(
        self,
        input: Optional[
            Union[Union[Path, str], Union[List[str], List[Path]], ParametricDesignStudyManager]
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
        if self.omdb_files_specification == OMDBFilesSpecificationEnum.STUDY_MANAGER:
            paths = []
            for design_study in self.input.design_studies:
                paths.extend(
                    [
                        file.path
                        for file in design_study.get_final_parametric_system().get_omdb_files()
                    ]
                )
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
        input: Optional[
            Union[Union[Path, str], Union[List[str], List[Path]], ParametricDesignStudyManager]
        ],
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
        if isinstance(input, ParametricDesignStudyManager):
            return OMDBFilesSpecificationEnum.STUDY_MANAGER
        elif isinstance(input, (str, Path)) and Path(input).is_dir():
            return OMDBFilesSpecificationEnum.OMDB_FOLDER
        elif isinstance(input, list) and all(
            isinstance(item, (str, Path)) and Path(item).suffix == ".omdb" for item in input
        ):
            return OMDBFilesSpecificationEnum.OMDB_FILES
        else:
            return OMDBFilesSpecificationEnum.UNDEFINED


# endregion


# region managed instance
class ManagedInstance:
    """Class storing a managed instance."""

    @property
    def instance(self) -> Node:
        """Get the managed instance.

        Returns
        -------
        Node
            The managed instance.
        """
        return self.__instance

    def __init__(
        self,
        instance: Node,
    ):
        """Initialize the ManagedInstance.

        Parameters
        ----------
        instance : Node
            Elementary component manageable by the ParametricDesignStudy class.
        """
        self.__instance = instance


class ManagedParametricSystem(ManagedInstance):
    """Class storing a managed algorithm."""

    @property
    def instance(self) -> ParametricSystem:
        """Instance of the managed algorithm.

        Returns
        -------
        ParametricSystem
            Instance of the managed algorithm.
        """
        return super().instance

    @property
    def solver_node(self) -> IntegrationNode:
        """Instance of the solver node inside the managed algorithm.

        Returns
        -------
        IntegrationNode
            Instance of the solver node inside the managed algorithm.
        """
        return self.__solver_node

    def __init__(
        self,
        parametric_system: ParametricSystem,
        solver_node: IntegrationNode,
    ):
        """Initialize the ManagedAlgorithm.

        Parameters
        ----------
        parametric_system : ParametricSystem
            Instance of the managed parametric system.
        solver_node : IntegrationNode
            Instance of the solver node inside the managed parametric system.
        """
        super().__init__(parametric_system)
        self.__solver_node = solver_node


class ProxySolverManagedParametricSystem(ManagedParametricSystem):
    """Class storing a managed algorithm with ProxySolver node."""

    @property
    def callback(self) -> callable:
        """A callback function to handle design evaluation results.

        Returns
        -------
        callable
            A callback function to handle design evaluation results.
        """
        return self.__callback

    @property
    def solver_node(self) -> ProxySolverNode:
        """Instance of the solver node inside the managed algorithm.

        Returns
        -------
        ProxySolverNode
            Instance of the solver node inside the managed algorithm.
        """
        return super().solver_node

    def __init__(
        self,
        algorithm: ParametricSystem,
        solver_node: ProxySolverNode,
        callback: callable,
    ):
        """Initialize the ManagedAlgorithm.

        Parameters
        ----------
        parametric_system : ParametricSystem
            Instance of the managed parametric system.
        solver_node : ProxySolverNode
            Instance of the proxy solver node inside the managed parametric system.
        callback: callable
            Callback to be executed by the proxy solver.
        """
        super().__init__(algorithm, solver_node)
        self.__callback = callback


# endregion


class ParametricDesignStudy:
    """A class to store data and perform operations on design study.

    Attributes
    ----------
    instance : ParametricSystem
        Instance of the managed algoritgm.
    predecessor : Dict[str, Node], optional
        Dictionary of predecessors of the managed algorithm.
    """

    @property
    def managed_instances(self) -> Tuple[ManagedInstance]:
        """Elementary components of this ParametricStudy.

        Returns
        -------
        Tuple[ManagedInstance]
            Elementary components of this ParametricStudy.
        """
        return self.__managed_instances

    @property
    def predecessors(self) -> Tuple[Node]:
        """Predecessors of the managed algorithm.

        Returns
        -------
        Tuple[Node]
            Tuple of predecessors of the managed algorithm.
        """
        return tuple(self.__predecessors.values())

    def __init__(
        self,
        osl_instance: Optislang,
        managed_instances: Tuple[ManagedInstance],
        predecessors: Optional[Iterable[Node]] = None,
    ):
        """Initialize the ParametricDesignStudy.

        Parameters
        ----------
        osl_instance: Optislang
            The optiSLang instance.
        managed_instances : Iterable[ManagedInstance]
            Elementary components of this ParametricStudy provided in execution order.
        predecessors : Optional[Iterable[Node]], optional
            Iterable of predecessors of the managed algorithm.
        """
        self.__osl_instance: Optislang = osl_instance
        self.__managed_instances: List[ManagedParametricSystem] = list(managed_instances)
        self.__predecessors: Dict[str, Node] = (
            {predecessor.uid: predecessor for predecessor in predecessors} if predecessors else {}
        )

    def add_predecessor(self, predecessor: Node, connection: Optional[Tuple[str, str]]) -> None:
        """Add a predecessor to the managed algorithm.

        Parameters
        ----------
        predecessor : Node
            Instance of the predecessor node to be added.
        connection : Optional[Tuple[str, str]]
            Tuple specifying the connection from the predecessor node to the managed algorithm.
            E.g. ("OBestDesigns", "IStartDesigns").
        """
        if predecessor.uid not in self.__predecessors.keys():
            self.__predecessors[predecessor.uid] = predecessor
        else:
            self.__osl_instance.log.warning("The specified predecessor is already set.")

        if connection:
            predecessor.get_output_slots(name=connection[0])[0].connect_to(
                self.__algorithm.get_input_slots(name=connection[1])[0]
            )

    def clear_predecessors(self, algorithm: ParametricSystem) -> None:
        """Clear predecessors of the specified managed algorithm.

        Parameters
        ----------
        algorithm : ParametricSystem
            Instance of the managed algorithm.
        """
        self.__predecessors.clear()

    def delete(self) -> None:
        """Delete the managed algorithm from the project."""
        for item in self.__managed_instances:
            item.instance.delete()

    # TODO: Execute whole block or instance by instance?
    def execute(self):
        """Execute the managed instances."""
        for item in self.__managed_instances:
            if isinstance(item, ProxySolverManagedParametricSystem):
                item.instance.set_execution_options(
                    ExecutionOption.ACTIVE
                    | ExecutionOption.STARTING_POINT
                    | ExecutionOption.END_POINT
                )
                self.__osl_instance.application.project.start(wait_for_finished=False)
                while True:
                    status = self.__osl_instance.application.project.get_status()
                    if status == "FINISHED":
                        self.__osl_instance.log.info(f"Project status: {status}")
                        break
                    elif status == "STOPPED":
                        self.__osl_instance.log.info(f"Project status: {status}")
                        break
                    design_list = item.solver_node.get_designs()
                    if len(design_list) and item.callback:
                        responses_dict = item.callback(design_list)
                        item.solver_node.set_designs(responses_dict)
                    time.sleep(0.5)
                item.instance.set_execution_options(ExecutionOption.INACTIVE)
            else:
                item.instance.set_execution_options(
                    ExecutionOption.ACTIVE
                    | ExecutionOption.STARTING_POINT
                    | ExecutionOption.END_POINT
                )
                self.__osl_instance.application.project.start(wait_for_finished=True)
                item.instance.set_execution_options(ExecutionOption.INACTIVE)

    def get_result_designs(self) -> Tuple[Design]:
        """Get the result designs of the final parametric system workflow component.

        Returns
        -------
        Tuple[Design]
            Tuple of result designs of the managed algorithm.
        """
        designs = []
        for item in reversed(self.__managed_instances):
            if isinstance(item, ManagedParametricSystem):
                designs.extend(item.instance.design_manager.get_designs("0"))
        return tuple(designs)

    def get_final_parametric_system(self) -> ParametricSystem:
        """Get the final parametric system workflow component.

        Returns
        -------
        ParametricSystem
            The final parametric system.
        """
        for item in reversed(self.__managed_instances):
            if isinstance(item, ManagedParametricSystem):
                return item.instance

    def is_complete(self) -> bool:
        """Check if the design study is finished.

        Returns
        -------
        bool
            ``True`` if all components has been solved, ``False`` otherwise.
        """
        return all(item.instance.get_status() == "Finished" for item in self.__managed_instances)

    def contains_proxy_solver(self) -> bool:
        """Get info whether workflow contains proxy solver.

        Returns
        -------
        bool
            Whether proxy solver is contained.
        """
        return any(
            [
                isinstance(item.instance, ProxySolverManagedParametricSystem)
                for item in self.managed_instances
            ]
        )

    def remove_predecessor(self, predecessor: Node) -> None:
        """Remove a predecessor from the managed algorithm.

        Parameters
        ----------
        predecessor : Node
            Instance of the predecessor node to be removed.
        """
        if predecessor.uid in self.__predecessors.keys():
            self.__predecessors.pop(predecessor.uid)
        else:
            self.__osl_instance.log.warning("The specified predecessor is not set.")


class ParametricDesignStudyManager:
    """Class creating and managing design studies."""

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
    def design_studies(self) -> Tuple[ParametricDesignStudy, ...]:
        """Managed design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Tuple of managed parametric studies.
        """
        return tuple(self.__design_studies)

    def __init__(self, optislang_instance: Optional[Optislang] = None, **kwargs):
        """Initialize the ParametricDesignStudyManager.

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

        self.__design_studies: List[ParametricDesignStudy] = []

    def append_algorithm_design_study(
        self,
        managed_instances: Iterable[ManagedInstance],
    ) -> None:
        """Add an existing design study to the managed studies.

        Predecessors are determined automatically based on the connections
        of the first managed instance.

        Parameters
        ----------
        managed_instances : Iterable[ManagedInstance]
            Iterable of managed instances composing the design study.
        """
        node: Node = managed_instances[0].instance
        predecessors = [edge.from_slot.node for edge in node.get_connections(SlotType.INPUT)]
        design_study = ParametricDesignStudy(self.optislang, managed_instances, predecessors)
        self.__design_studies.append(design_study)

    def clear_design_studies(self, delete: Optional[bool] = False) -> None:
        """Remove all designs studies managed by the instance of ParametricDesignStudyManager.

        Parameters
        ----------
        delete: Optional[bool], optional
            If ``True``, the algorithm nodes will be deleted from the project. By default ``False``.
        """
        if delete:
            [design_study.delete() for design_study in self.__design_studies]
        self.__design_studies.clear()

    def create_design_study(self, workflow: WorkFlowTemplate) -> ParametricDesignStudy:
        """Create a design study based on the provided workflow template.

        Parameters
        ----------
        workflow : WorkFlowTemplate
            The workflow template defining the design study.

        Returns
        -------
        ParametricDesignStudy
            The created design study.
        """
        managed_instances = workflow.create_workflow(self.optislang.application.project.root_system)
        predecessors = workflow.predecessors if hasattr(workflow, "predecessors") else []
        design_study = ParametricDesignStudy(self.optislang, managed_instances, predecessors)
        self.__design_studies.append(design_study)
        return design_study

    def dispose(self):
        """Dispose the instance of SolverManager and close the associated optiSLang instance."""
        self.__design_studies.clear()
        if self.optislang:
            self.optislang.dispose()

    def execute_all_design_studies(self) -> None:
        """Execute all managed design studies."""
        order = self.__class__.get_design_study_execution_order(self.design_studies)
        for design_study in order:
            design_study.execute()

    def get_finished_design_studies(self) -> Tuple[ParametricDesignStudy, ...]:
        """Get all finished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Tuple of managed parametric studies that have been solved.
        """
        return tuple(
            [design_study for design_study in self.__design_studies if design_study.is_complete()]
        )

    def get_unfinished_design_studies(self) -> Tuple[ParametricDesignStudy, ...]:
        """Get all unfinished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Tuple of managed parametric studies that have not been solved.
        """
        return tuple(
            [
                design_study
                for design_study in self.__design_studies
                if not design_study.is_complete()
            ]
        )

    @staticmethod
    def get_design_study_execution_order(
        design_studies: Iterable[ParametricDesignStudy],
    ) -> Tuple[ParametricDesignStudy, ...]:
        """Sort design studies with predecessor before its dependent design study.

        Parameters
        ----------
        design_studies : Iterable[ParametricDesignStudy]
            Iterable of managed design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Ordered tuple of design studies for execution.
        """
        # Build dependency graph: key is ParametricDesignStudy,
        # value is set of predecessor ParametricDesignStudy
        study_to_predecessors = {
            study: set(
                pred
                for pred in study.predecessors
                if any(pred is s.managed_instances[0].instance for s in design_studies)
            )
            for study in design_studies
        }

        # Kahn's algorithm for topological sort
        ordered = []
        no_deps = [study for study, preds in study_to_predecessors.items() if not preds]
        visited = set()
        while no_deps:
            study = no_deps.pop(0)
            if study in visited:
                continue
            ordered.append(study)
            visited.add(study)
            for other_study, preds in study_to_predecessors.items():
                if study.managed_instances[0].instance in preds:
                    preds.remove(study.managed_instances[0].instance)
                    if not preds and other_study not in visited and other_study not in no_deps:
                        no_deps.append(other_study)
        # If there are cycles, append remaining in original order
        for study in design_studies:
            if study not in ordered:
                ordered.append(study)
        return tuple(ordered)
