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
import threading
import time
from typing import (
    TYPE_CHECKING,
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
    DESIGN_STUDY_MANAGER = 3
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
        if self.omdb_files_specification == OMDBFilesSpecificationEnum.DESIGN_STUDY_MANAGER:
            paths = []
            for design_study in self.input.design_studies:
                paths.extend(
                    [
                        file.path
                        for file in design_study.get_last_parametric_system().get_omdb_files()
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
            return OMDBFilesSpecificationEnum.DESIGN_STUDY_MANAGER
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


class ExecutableBlock:
    """Class specifying execution options for a set of managed instances."""

    @property
    def instances_with_execution_options(self) -> Tuple[Tuple[ManagedInstance, ExecutionOption]]:
        """Get tuple of managed instances and its execution options.

        Returns
        -------
        Tuple[Tuple[ManagedInstance, ExecutionOption]]
           Tuple of managed instances and its execution options.
        """
        return tuple(self.__instances)

    @property
    def instances(self) -> Tuple[ManagedInstance]:
        """Get tuple of managed instances.

        Returns
        -------
        Tuple[ManagedInstance]
           Tuple of managed instances.
        """
        return tuple([instance[0] for instance in self.__instances])

    def __init__(
        self, instances: Optional[Iterable[Tuple[ManagedInstance, ExecutionOption]]] = []
    ) -> None:
        """Initialize the ExecutableBlock.

        Parameters
        ----------
        instances : Optional[Iterable[Tuple[ManagedInstance, ExecutionOption]]]
            Subset of instances managed by a single ParametricDesignStudy.
            Each block must contain maximum of 1 algorithm system.
        """
        self.__instances = []
        if len(instances) > 0:
            for instance, exec_option in instances:
                self.__instances.append((instance, exec_option))

    def add_instance(self, instance: ManagedInstance, execution_options: ExecutionOption) -> None:
        """Add instance with execution options.

        Parameters
        ----------
        instance : ManagedInstance
            Managed instance.
        execution_options : ExecutionOption
            Execution options.
        """
        self.__instances.append((instance, execution_options))

    def remove_instance_by_uid(self, uid: str) -> None:
        """Remove instance from execution block.

        Parameters
        ----------
        uid : str
            Node uid.
        """
        idx = self.__find_instance_idx_by_uid(uid)
        if idx >= 0:
            self.__instances.pop(idx)

    def __find_instance_idx_by_uid(self, uid: str) -> int:
        """Get index of instance with specified uid.

        Parameters
        ----------
        uid : str
            Node uid.

        Returns
        -------
        int
            Index of instance with specified uid.
            -1 if not specified in ExecutionBlock.
        """
        for idx, (instance, connections) in enumerate(self.instances_with_execution_options):
            if instance.instance.uid == uid:
                return idx
        return -1


# endregion


class ParametricDesignStudy:
    """A class to store data and perform operations on design study."""

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
    def execution_order(self) -> Tuple[ExecutableBlock]:
        """Get ordered tuple of executable blocks.

        Returns
        -------
        Tuple[ExecutableBlock]
            Tuple of executable blocks.
        """
        return tuple(self.__execution_blocks)

    @property
    def is_complete(self) -> bool:
        """Get info if design study is finished.

        Returns
        -------
        bool
            ``True`` if all components has been solved, ``False`` otherwise.
        """
        return self.__is_complete

    def __init__(
        self,
        osl_instance: Optislang,
        managed_instances: Tuple[ManagedInstance],
        execution_blocks: Optional[Iterable[ExecutableBlock]] = [],
    ):
        """Initialize the ParametricDesignStudy.

        Parameters
        ----------
        osl_instance: Optislang
            The optiSLang instance.
        managed_instances : Iterable[ManagedInstance]
            Elementary components of this ParametricStudy. If `execution_blocks`
            argument is not used, execution blocks are created automatically
            internally from provided order of instances.
            .. note:: Each study is meant to contain a single algorithm system.
        execution_blocks: Optional[Iterable[ExecutableBlock]], optional
            Iterable of executable blocks. Blocks must be provided in execution order.
            Each execution block contains a subset of instances managed by a single
            parametric design study. All execution block must create a complete set
            without overlap. Created automatically from managed instances ordered,
            if not provided.
        """
        self.__osl_instance: Optislang = osl_instance
        self.__managed_instances: List[ManagedParametricSystem] = list(managed_instances)
        if execution_blocks:
            self.__execution_blocks = execution_blocks
        else:
            block = ExecutableBlock()
            blocks = []
            for instance in self.managed_instances:
                if isinstance(instance, ManagedParametricSystem):
                    if block.instances_with_execution_options:
                        blocks.append(block)
                        block = ExecutableBlock()
                    blocks.append(
                        ExecutableBlock(
                            [
                                (
                                    instance,
                                    ExecutionOption.ACTIVE
                                    | ExecutionOption.STARTING_POINT
                                    | ExecutionOption.END_POINT,
                                ),
                            ]
                        )
                    )
                else:
                    block.add_instance(instance, ExecutionOption.ACTIVE)
            if block.instances_with_execution_options:
                blocks.append(block)
            self.__execution_blocks = blocks
        self.__current_proxy_solver = None
        self.__is_complete = False

    def delete(self) -> None:
        """Delete the managed algorithm from the project."""
        for item in self.__managed_instances:
            item.instance.delete()

    def execute(self):
        """Execute the managed instances automatically in blocking mode."""
        self.__deactivate_toplevel_nodes()
        for block in self.execution_order:
            proxy_solver = None
            callback = None
            # set exec options for each instance in executable block
            for item, exec_opt in block.instances_with_execution_options:
                if isinstance(item, ProxySolverManagedParametricSystem):
                    proxy_solver = item.solver_node
                    callback = item.callback
                item.instance.set_execution_options(exec_opt)
            # execute whole block (special treatment of proxy solver)
            if proxy_solver:
                self.__osl_instance.application.project.start(wait_for_finished=False)
                while True:
                    status = self.__osl_instance.application.project.get_status()
                    if status == "FINISHED":
                        self.__osl_instance.log.info(f"Project status: {status}")
                        break
                    elif status == "STOPPED":
                        self.__osl_instance.log.info(f"Project status: {status}")
                        break
                    design_list = proxy_solver.get_designs()
                    if len(design_list):
                        responses_dict = callback(design_list)
                        proxy_solver.set_designs(responses_dict)
                    time.sleep(0.5)
            else:
                self.__osl_instance.application.project.start()
            # deactivate all instances, when finished
            self.__set_managed_instances_exec_options(ExecutionOption.INACTIVE, block.instances)
        self.__is_complete = True

    def start_in_thread(self):
        """Start execution in a separate thread (non-blocking mode).

        .. note:: This method is meant to be used in combination with
            ``get/set_designs`` and ``get_status`` methods, for the
            proxy solver use case.
        """
        self.__deactivate_toplevel_nodes()
        self.__thread = threading.Thread(
            target=self.__start_in_thread,
            name=f"PyOptiSLang.StartDesignStudy",
            daemon=True,
        )
        self.__thread.start()

    def reset(self):
        """Reset the parametric design study.

        Top level nodes are dectivated and managed instances are set to "Active" prior
        to the "reset" call on the project level, then switched back to "Inactive".
        """
        self.__deactivate_toplevel_nodes()
        self.__set_managed_instances_exec_options(execution_options=ExecutionOption.ACTIVE)
        self.__osl_instance.application.project.reset()
        self.__set_managed_instances_exec_options(execution_options=ExecutionOption.INACTIVE)
        self.__is_complete = False

    def get_result_designs(self) -> Tuple[Design]:
        """Get the result designs of the final parametric system workflow component.

        Returns
        -------
        Tuple[Design]
            Tuple of result designs of the managed algorithm.
        """
        designs = []
        for item in reversed(self.execution_order):
            for item, exec_opt in item.instances_with_execution_options:
                if isinstance(item, ManagedParametricSystem):
                    designs.extend(item.instance.design_manager.get_designs("0"))
        return tuple(designs)

    def get_status(self) -> str:
        """Get project status.

        Returns
        -------
        str
            Project status.
        """
        return self.__osl_instance.application.project.get_status()

    def get_last_parametric_system(self) -> ParametricSystem:
        """Get the last parametric system workflow component.

        Returns
        -------
        ParametricSystem
            The last parametric system.
        """
        for block in reversed(self.execution_order):
            for item in block.instances:
                if isinstance(item, ManagedParametricSystem):
                    return item.instance

    def contains_proxy_solver(self) -> bool:
        """Get info whether workflow contains proxy solver.

        Returns
        -------
        bool
            Whether proxy solver is contained.
        """
        return self.__get_proxy_solver() is not None

    # region proxy solver related
    def get_designs(self) -> Optional[List[dict]]:
        """Call ``get_designs` command on proxy solver node in use.

        Returns
        -------
        Optional[dict]
            List of designs dictionaries, if proxy_solver is being executed, else ``None``.
        """
        if self.__current_proxy_solver is not None:
            return self.__current_proxy_solver.get_designs()

    def set_designs(self, designs: List[dict]):
        """Call ``set_designs`` command on proxy solver node in use.

        Parameters
        ----------
        List[dict]
            List of solved designs dictionaries.
        """
        if self.__current_proxy_solver is not None:
            self.__current_proxy_solver.set_designs(designs)

    # endregion
    def __get_proxy_solver(
        self, instances: Optional[Iterable[ManagedInstance]] = []
    ) -> Optional[ProxySolverNode]:
        """Loop through managed instances and return proxy solver.

        Parameters
        ----------
        instances: Optional[Iterable[ManagedInstance]], optional
            Instances to search in. If not provided, all managed instances are used.

        Returns
        -------
        Optional[ProxySolverNode]
            Proxy solver (if defined in current designs study, else ``None``).
        """
        for item in self.__managed_instances:
            if isinstance(item, ProxySolverManagedParametricSystem):
                return item.solver_node
        return None

    def __set_managed_instances_exec_options(
        self,
        execution_options: ExecutionOption,
        instances: Optional[Iterable[ManagedInstance]] = [],
    ) -> None:
        """Set execution options of all managed instances.

        Parameters
        ----------
        execution_option: ExecutionOption
            Execution option to be set to all managed instances.
            Multiple options can be specified using bitwise operator.
        instances: Optional[Iterable[ManagedInstance]], optional
            Instances to operate with. All managed instances are used by default.
        """
        used_instances = instances if instances else self.managed_instances
        for item in used_instances:
            item.instance.set_execution_options(execution_options)

    def __deactivate_toplevel_nodes(self) -> None:
        """Set all nodes on root level to "Inactive" state."""
        for node in self.__osl_instance.application.project.root_system.get_nodes():
            node.set_execution_options(ExecutionOption.INACTIVE)

    def __start_in_thread(self) -> None:
        for block in self.execution_order:
            self.__current_proxy_solver = None
            # set exec options for each instance in executable block
            for item, exec_opt in block.instances_with_execution_options:
                if isinstance(item, ProxySolverManagedParametricSystem):
                    self.__current_proxy_solver = item.solver_node
                item.instance.set_execution_options(exec_opt)
            # execute whole block
            self.__osl_instance.application.project.start(wait_for_finished=True)
            # deactivate all instances, when finished
            self.__set_managed_instances_exec_options(ExecutionOption.INACTIVE, block.instances)
            self.__current_proxy_solver = None
        self.__is_complete = True


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

    def append_design_study(
        self,
        design_study: ParametricDesignStudy,
    ) -> None:
        """Add an existing design study to the managed studies.

        Parameters
        ----------
        design_study: ParametricDesignStudy
            Instance of parametric design study.
        """
        if isinstance(design_study, ParametricDesignStudy):
            self.__design_studies.append(design_study)
        else:
            raise TypeError(
                "Expected instance of`ParametricDesignStudy`, but got `{}`".format(
                    type(design_study)
                )
            )

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
        managed_instances, executable_blocks = workflow.create_workflow(
            self.optislang.application.project.root_system
        )
        design_study = ParametricDesignStudy(self.optislang, managed_instances, executable_blocks)
        self.__design_studies.append(design_study)
        return design_study

    def dispose(self):
        """Dispose the instance of SolverManager and close the associated optiSLang instance."""
        self.__design_studies.clear()
        if self.optislang:
            self.optislang.dispose()

    def reset(self) -> None:
        """Reset all managed parametric design studies."""
        [study.reset() for study in self.design_studies]

    def save(self) -> None:
        """Save current project."""
        self.optislang.application.save()

    def save_as(self, path: Union[str, Path]):
        """Save current project as.

        Parameters
        ----------
        path: Union[str, Path]
            Path to project location.
        """
        self.optislang.application.save_as(path)

    def get_finished_design_studies(self) -> Tuple[ParametricDesignStudy, ...]:
        """Get all finished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Tuple of managed parametric studies that have been solved.
        """
        return tuple(
            [design_study for design_study in self.__design_studies if design_study.is_complete]
        )

    def get_unfinished_design_studies(self) -> Tuple[ParametricDesignStudy, ...]:
        """Get all unfinished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudy, ...]
            Tuple of managed parametric studies that have not been solved.
        """
        return tuple(
            [design_study for design_study in self.__design_studies if not design_study.is_complete]
        )
