# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from abc import ABC
from enum import Enum
from pathlib import Path
import threading
import time
from typing import (
    TYPE_CHECKING,
    Callable,
    cast,
    Iterable,
    List,
    Optional,
    Sequence,
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
    OutputSlot,
)
from ansys.optislang.core.project_parametric import (
    Design,
    DesignVariable,
    Parameter,
    Response,
    Criterion,
)

import ansys.optislang.core.node_types as nt

if TYPE_CHECKING:
    from ansys.optislang.core.project_parametric import (
        Design,
    )
    from ansys.optislang.parametric.design_study_templates import (
        DesignStudyTemplate,
        GeneralAlgorithmSettings,
        GeneralNodeSettings,
    )


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
    ) -> Optional[Union[Union[Path, str], List[Union[Path, str]], ParametricDesignStudyManager]]:
        """Input specifying the OMDB files.

        Returns
        -------
        Optional[Union[Union[Path,str], List[Union[Path, str]], ParametricDesignStudyManager]]
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of ParametricDesignStudyManager.
        """
        return self.__input

    @input.setter
    def input(
        self,
        value: Union[Union[Path, str], List[Union[Path, str]], ParametricDesignStudyManager, None],
    ):
        self.__input = value
        self.__omdb_files_specification = self.__class__.get_ombd_files_specification_from_input(
            value
        )

    def __init__(
        self,
        input: Optional[
            Union[Union[Path, str], List[Union[Path, str]], ParametricDesignStudyManager]
        ] = None,
    ):
        """Initialize the OMDBFilesProvider.

        Parameters
        ----------
        input : Optional[
                    Union[
                        Union[Path,str],
                        List[Union[Path, str]],
                        ParametricDesignStudyManager,
                    ]
            ], optional
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of `ParametricDesignStudyManager`.
        """
        self.input = input

    def get_omdb_files(self) -> Tuple[Path, ...]:
        """Get the a tuple of OMDB files to be included in the project.

        Returns
        -------
        Tuple[Path, ...]
            Tuple of paths to the OMDB files.
        """
        if self.omdb_files_specification == OMDBFilesSpecificationEnum.DESIGN_STUDY_MANAGER:
            if not isinstance(self.input, ParametricDesignStudyManager):
                raise TypeError("Unexpected input type: `{}`".format(type(self.input)))
            paths = []
            for design_study in self.input.design_studies:
                parametric_system = design_study.get_last_parametric_system()
                if parametric_system:
                    paths.extend([file.path for file in parametric_system.get_omdb_files()])
            return tuple(paths)
        elif self.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FOLDER:
            if not isinstance(self.input, (Path, str)):
                raise TypeError("Unexpected input type: `{}`".format(type(self.input)))
            folder_path = Path(self.input)
            return tuple([file for file in folder_path.rglob("*.omdb") if file.is_file()])
        elif self.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FILES:
            if not isinstance(self.input, Sequence):
                raise TypeError("Unexpected input type: `{}`".format(type(self.input)))
            return tuple([Path(file) for file in self.input])
        else:
            return tuple([])

    @staticmethod
    def get_ombd_files_specification_from_input(
        input: Optional[
            Union[Union[Path, str], List[Union[Path, str]], ParametricDesignStudyManager]
        ],
    ):
        """Determine the specification of the OMDB files based on the input.

        Parameters
        ----------
        input : Optional[Union[Union[Path, str], List[Union[Path, str]],
            ParametricDesignStudyManager]]
            Input specifying the OMDB files. Can be a path to a folder, a list of paths,
            or an instance of ParametricDesignStudyManager.

        Returns
        -------
        OMDBFilesSpecificationEnum
            The specification of the OMDB files.
        """
        if isinstance(input, ParametricDesignStudyManager):
            return OMDBFilesSpecificationEnum.DESIGN_STUDY_MANAGER
        elif isinstance(input, (str, Path)) and Path(input).is_dir():
            return OMDBFilesSpecificationEnum.OMDB_FOLDER
        elif isinstance(input, Sequence) and all(
            isinstance(item, (str, Path)) and Path(item).suffix == ".omdb" for item in input
        ):
            return OMDBFilesSpecificationEnum.OMDB_FILES
        else:
            return OMDBFilesSpecificationEnum.UNDEFINED

    # endregion


# region helpers


def _register_solver_node_locations(
    solver_node: Union[ProxySolverNode, IntegrationNode],
    parameters: Iterable[Parameter],
    responses: Iterable[Response],
) -> None:
    """Register solver node locations based on the type of the solver node.

    Parameters
    ----------
    solver_node : Union[ProxySolverNode, IntegrationNode]
        Instance of the solver node.
    parameters : Iterable[Parameter]
        Parameters to be registered.
    responses: Iterable[Response]
        Responses to be registered.
    """
    registration_function = _REGISTRATION_FUNCTION_MAPPING.get(
        solver_node.type.id, _register_integration_node_locations
    )
    registration_function(solver_node, parameters, responses)


def _register_proxy_solver_locations(
    solver_node: ProxySolverNode,
    parameters: Iterable[Parameter],
    responses: Iterable[Response],
) -> None:  # pragma: no cover
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
    load_json: dict[str, dict] = {}
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


def _register_mop_solver_locations(
    solver_node: IntegrationNode,
    parameters: Iterable[Parameter],
    responses: Iterable[Response],
) -> None:  # pragma: no cover
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


def _register_python2_locations(
    solver_node: IntegrationNode,
    parameters: Iterable[Parameter],
    responses: Iterable[Response],
) -> None:  # pragma: no cover
    """Register python2 node locations.

    Parameters
    ----------
    solver_node : IntegrationNode
        Instance of the python solver node.
    parameters : Iterable[Parameter]
        Parameter to be registered.
    responses: Iterable[Response]
        Responses to be registered.
    """
    solver_node.load()
    for parameter in parameters:
        solver_node.register_location_as_parameter(
            location=parameter.name,
            name=parameter.name,
            reference_value=parameter.reference_value,
        )
    for response in responses:
        solver_node.register_location_as_response(
            location=response.name,
            name=response.name,
            reference_value=response.reference_value,
        )


def _register_integration_node_locations(
    solver_node: IntegrationNode,
) -> None:  # pragma: no cover
    """Register integration node locations using `load` method.

    Parameters
    ----------
    solver_node : IntegrationNode
        Instance of the integration_node.
    """
    solver_node.load()
    solver_node.register_locations_as_parameter()
    solver_node.register_locations_as_response()


_REGISTRATION_FUNCTION_MAPPING = {
    nt.ProxySolver.id: _register_proxy_solver_locations,
    nt.Mopsolver.id: _register_mop_solver_locations,
    nt.Python2.id: _register_python2_locations,
}

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
        instance = super().instance
        if not isinstance(instance, ParametricSystem):
            raise TypeError("Unexpected instance type: `{}`".format(type(instance)))
        return instance

    @property
    def solver_node(self) -> IntegrationNode:
        """Instance of the solver node inside the managed algorithm.

        Returns
        -------
        IntegrationNode
            Instance of the solver node inside the managed algorithm.
        """
        if not isinstance(self.__solver_node, IntegrationNode):
            raise TypeError("Unexpected solver node type: `{}`".format(type(self.__solver_node)))
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

    @property
    def solver_node(self) -> ProxySolverNode:
        """Instance of the solver node inside the managed algorithm.

        Returns
        -------
        ProxySolverNode
            Instance of the solver node inside the managed algorithm.
        """
        instance = super().solver_node
        if not isinstance(instance, ProxySolverNode):
            raise TypeError("Unexpected solver node type: `{}`".format(type(instance)))
        return instance

    def __init__(
        self,
        algorithm: ParametricSystem,
        solver_node: ProxySolverNode,
        callback: Callable,
    ):
        """Initialize the ManagedAlgorithm.

        Parameters
        ----------
        parametric_system : ParametricSystem
            Instance of the managed parametric system.
        solver_node : ProxySolverNode
            Instance of the proxy solver node inside the managed parametric system.
        callback: Callable
            Callback to be executed by the proxy solver.
        """
        super().__init__(algorithm, solver_node)
        self.__callback = callback


class ExecutableBlock:
    """Class specifying execution options for a set of managed instances."""

    @property
    def instances_with_execution_options(
        self,
    ) -> Tuple[Tuple[ManagedInstance, ExecutionOption], ...]:
        """Get tuple of managed instances and its execution options.

        Returns
        -------
        Tuple[Tuple[ManagedInstance, ExecutionOption], ...]
           Tuple of managed instances and its execution options.
        """
        return tuple(self.__instances)

    @property
    def instances(self) -> Tuple[ManagedInstance, ...]:
        """Get tuple of managed instances.

        Returns
        -------
        Tuple[ManagedInstance, ...]
           Tuple of managed instances.
        """
        return tuple([instance[0] for instance in self.__instances])

    def __init__(
        self, instances: Optional[Sequence[Tuple[ManagedInstance, ExecutionOption]]] = None
    ) -> None:
        """Initialize the ExecutableBlock.

        Parameters
        ----------
        instances : Optional[Sequence[Tuple[ManagedInstance, ExecutionOption]]], optional
            Subset of instances managed by a single ParametricDesignStudy.
            Each block must contain maximum of 1 algorithm system. By default `None`.
        """
        self.__validate_instances_for_execution_block(instances or [])
        self.__instances: list[Tuple[ManagedInstance, ExecutionOption]] = []
        if instances is not None:
            for instance, exec_option in instances:
                self.__instances.append((instance, exec_option))

    def activate(self) -> None:
        """Activates all instances in the block, irrespective of the stored execution options."""
        active = ExecutionOption.ACTIVE
        for instance, _ in self.__instances:
            instance.instance.set_execution_options(active)

    def add_instance(self, instance: ManagedInstance, execution_options: ExecutionOption) -> None:
        """Add instance with execution options.

        Parameters
        ----------
        instance : ManagedInstance
            Managed instance.
        execution_options : ExecutionOption
            Execution options.

        Raises
        ------
        ValueError
            If an instance with the same uid already exists in the block.

        ValueError
            If adding a managed parametric system when one already exists in the block.
        """
        if (
            isinstance(instance, ManagedParametricSystem)
            and self.get_managed_parametric_system() is not None
        ):
            raise ValueError("Only one managed parametric system is allowed in the block.")
        if self.__find_instance_idx_by_uid(instance.instance.uid) < 0:
            self.__instances.append((instance, execution_options))
        else:
            raise ValueError(
                "Instance with uid `{}` already exists in the block.".format(instance.instance.uid)
            )

    def apply_execution_options(self) -> None:
        """Apply stored execution options to all instances in the block."""
        for instance, exec_option in self.__instances:
            instance.instance.set_execution_options(exec_option)

    def deactivate(self) -> None:
        """Deactivates all instances in the block, irrespective of the stored execution options."""
        inactive = ExecutionOption.INACTIVE
        for instance, _ in self.__instances:
            instance.instance.set_execution_options(inactive)

    def get_instance_by_uid(self, uid: str) -> Optional[ManagedInstance]:
        """Get managed instance by uid.

        Parameters
        ----------
        uid : str
            Node uid.

        Returns
        -------
        Optional[ManagedInstance]
            Managed instance with specified uid, if found, else ``None``.
        """
        idx = self.__find_instance_idx_by_uid(uid)
        if idx >= 0:
            instance, _ = self.__instances[idx]
            return instance
        return None

    def get_instance_execution_option_by_uid(self, uid: str) -> Optional[ExecutionOption]:
        """Get execution options of a specific instance in the block.

        Parameters
        ----------
        uid : str
            Node uid.

        Returns
        -------
        Optional[ExecutionOption]
            Execution options of the instance with specified uid, if found, else ``None``.
        """
        idx = self.__find_instance_idx_by_uid(uid)
        if idx >= 0:
            _, exec_option = self.__instances[idx]
            return exec_option
        return None

    def get_managed_parametric_system(self) -> Optional[ManagedParametricSystem]:
        """Get the managed parametric system in the block.

        Returns
        -------
        Optional[ManagedParametricSystem]
            Managed parametric system in the block, if any, else ``None``.
        """
        systems = self.__class__.__find_managed_parametric_systems(self.instances)
        return systems[0] if systems else None

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

    def set_execution_options_to_active(self) -> None:
        """Set execution options of all instances in the block to "Active".

        Notes
        -----
        This method changes only the stored execution options of the instances in the block,
        it does not change the actual state.
        """
        self.__instances = [(instance, ExecutionOption.ACTIVE) for instance, _ in self.__instances]

    def set_execution_options_to_inactive(self) -> None:
        """Set execution options of all instances in the block to "Inactive".

        Notes
        -----
        This method changes only the stored execution options of the instances in the block,
        it does not change the actual state.
        """
        self.__instances = [
            (instance, ExecutionOption.INACTIVE) for instance, _ in self.__instances
        ]

    def set_instance_execution_option_by_uid(
        self, uid: str, execution_options: ExecutionOption
    ) -> None:
        """Set execution options of a specific instance in the block.

        Parameters
        ----------
        uid : str
            Node uid.
        execution_options : ExecutionOption
            Execution options to be set.

        Notes
        -----
        This method changes only the stored execution options of the instance in the block,
        it does not change the actual state.
        """
        idx = self.__find_instance_idx_by_uid(uid)
        if idx >= 0:
            instance, _ = self.__instances[idx]
            self.__instances[idx] = (instance, execution_options)

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

    def __validate_instances_for_execution_block(
        self,
        instances: Iterable[Tuple[ManagedInstance, ExecutionOption]],
    ) -> None:
        """Validate instances uniqueness and a single parametric system.

        Parameters
        ----------
        instances : Iterable[Tuple[ManagedInstance, ExecutionOption]]
            Managed instances and execution options to be validated.

        Raises
        ------
        ValueError
            If there are duplicate uids among the managed instances.

        ValueError
            If there is more than one managed parametric system among the managed instances.
        """
        seen_uids = set()
        managed_instances: List[ManagedInstance] = []
        for instance, _ in instances:
            uid = instance.instance.uid
            if uid in seen_uids:
                raise ValueError(
                    "Duplicate uid `{}` found among the managed instances.".format(uid)
                )
            seen_uids.add(uid)
            managed_instances.append(instance)
        if len(self.__class__.__find_managed_parametric_systems(managed_instances)) > 1:
            raise ValueError("Only one managed parametric system is allowed in an execution block.")

    @staticmethod
    def __find_managed_parametric_systems(
        instances: Iterable[ManagedInstance],
    ) -> List[ManagedParametricSystem]:
        """Get all managed parametric systems from the instances.

        Parameters
        ----------
        instances : Iterable[ManagedInstance]
            Managed instances to be checked.

        Returns
        -------
        List[ManagedParametricSystem]
            List of managed parametric systems found in the instances.
        """
        return [instance for instance in instances if isinstance(instance, ManagedParametricSystem)]


# endregion


# region parametric design studies
class ParametricDesignStudyBase:
    """A class to store data and perform operations on design study."""

    @property
    def optislang(self) -> Optislang:
        """The optiSLang instance associated with this design study."""
        return self.__osl_instance

    @property
    def managed_instances(self) -> Tuple[ManagedInstance, ...]:
        """Elementary components of this ParametricStudy.

        Returns
        -------
        Tuple[ManagedInstance, ...]
            Elementary components of this ParametricStudy.
        """
        return tuple(self.__managed_instances)

    @property
    def execution_order(self) -> Tuple[ExecutableBlock, ...]:
        """Get ordered tuple of executable blocks.

        Returns
        -------
        Tuple[ExecutableBlock, ...]
            Tuple of executable blocks.
        """
        return tuple(self.__execution_blocks)

    @property
    def _managed_instances_ref(self) -> List[ManagedInstance]:
        """Mutable managed-instances container for internal subclass use."""
        return self.__managed_instances

    @property
    def _execution_blocks_ref(self) -> List[ExecutableBlock]:
        """Mutable execution-block container for internal subclass use."""
        return self.__execution_blocks

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
        managed_instances: Iterable[ManagedInstance],
        execution_blocks: Optional[Iterable[ExecutableBlock]] = None,
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
            parametric design study. Execution blocks should collectively contain all managed
            instances without overlap. Created automatically from managed instances ordered,
            if not provided.
        """
        self.__validate_instances(managed_instances)
        self.__osl_instance: Optislang = osl_instance
        self.__managed_instances: List[ManagedInstance] = list(managed_instances)
        if execution_blocks is not None:
            self.__execution_blocks = list(execution_blocks)
        else:
            blocks: List[ExecutableBlock] = []
            current_items: List[tuple[ManagedInstance, ExecutionOption]] = []
            current_block_has_parametric_system = False

            for instance in self.managed_instances:
                is_parametric_system = isinstance(instance, ManagedParametricSystem)

                # At most one ManagedParametricSystem per block.
                if is_parametric_system and current_block_has_parametric_system:
                    # Finalize current block
                    blocks.append(ExecutableBlock(current_items))
                    current_items = []
                    current_block_has_parametric_system = False

                current_items.append((instance, ExecutionOption.ACTIVE))
                if is_parametric_system:
                    current_block_has_parametric_system = True

            if current_items:
                # Finalize trailing block
                blocks.append(ExecutableBlock(current_items))

            self.__execution_blocks = blocks
        self.__current_proxy_solver: ProxySolverNode | None = None
        self.__is_complete = False

    def contains_proxy_solver(self) -> bool:
        """Get info whether workflow contains proxy solver.

        Returns
        -------
        bool
            Whether proxy solver is contained.
        """
        return self.__get_proxy_solver() is not None

    def delete(self) -> None:
        """Delete the managed instances from the design study and the project."""
        for item in self.__managed_instances:
            item.instance.delete()

        self.__managed_instances.clear()
        self.__execution_blocks.clear()

    def execute(self):
        """Execute the managed instances automatically in blocking mode."""
        self.__deactivate_toplevel_nodes()
        for block in self.execution_order:
            proxy_solver = None
            callback = None
            # set exec options for each instance in executable block
            block.apply_execution_options()
            parametric_system = block.get_managed_parametric_system()
            if parametric_system and isinstance(parametric_system.solver_node, ProxySolverNode):
                proxy_solver = parametric_system.solver_node
                callback = parametric_system.callback

            # execute whole block (special treatment of proxy solver)
            if proxy_solver:
                self.__execute_proxy_solver(proxy_solver, callback)
            else:
                self.__osl_instance.application.project.start()
            # deactivate all instances, when finished
            block.deactivate()
        self.__is_complete = True

    def find_execution_block_index_for_instance(self, instance: ManagedInstance) -> Optional[int]:
        """Get the index of the execution block containing the specified managed instance.

        Parameters
        ----------
        instance : ManagedInstance
            The managed instance for which to find the execution block index.

        Returns
        -------
        Optional[int]
            The index of the execution block containing the specified managed instance,
            if found, else `None`.
        """
        for idx, block in enumerate(self.execution_order):
            for inst in block.instances:
                if inst.instance.uid == instance.instance.uid:  # noqa: E501
                    return idx
        return None

    def find_managed_instance_by_uid(self, uid: str) -> Optional[ManagedInstance]:
        """Find a top level managed instance by its unique identifier (uid).

        Parameters
        ----------
        uid : str
            The unique identifier of the managed instance.

        Returns
        -------
        Optional[ManagedInstance]
            The managed instance with the specified uid, if found, else `None`.

        Notes
        -----
        Solver nodes cannot accessed directly by this method, they must be accessed through
        the associated parametric system.
        """
        for item in self.__managed_instances:
            if item.instance.uid == uid:
                return item
        return None

    def get_last_parametric_system(self) -> Optional[ParametricSystem]:
        """Get the last parametric system workflow component.

        Returns
        -------
        Optional[ParametricSystem]
            The last parametric system, if design study contains any, else `None`.
        """
        for block in reversed(self.execution_order):
            parametric_system = block.get_managed_parametric_system()
            if parametric_system:
                return parametric_system.instance
        return None

    def get_result_designs(self) -> Tuple[Design, ...]:
        """Get the result designs of the design study.

        Returns
        -------
        Tuple[Design, ...]
            Tuple of result designs of the managed algorithm.
        """
        designs: List[Design] = []
        for item in reversed(self.execution_order):
            parametric_system = item.get_managed_parametric_system()
            if parametric_system:
                designs.extend(parametric_system.instance.design_manager.get_designs("0"))
        return tuple(designs)

    def get_status(self) -> Optional[str]:
        """Get project status.

        Returns
        -------
        Optional[str]
            Project status, if any project is loaded, else `None`.
        """
        return (
            self.__osl_instance.application.project.get_status()
            if self.__osl_instance.application.project
            else None
        )

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

    # region proxy solver related
    def get_designs(self) -> Optional[List[Design]]:
        """Call ``get_designs`` command on proxy solver node in use.

        Returns
        -------
        Optional[Design]
            List of designs, if proxy_solver is being executed, else ``None``.
        """
        if self.__current_proxy_solver is not None:
            designs_list: list[dict] = self.__current_proxy_solver.get_designs()
            return self.__class__.__convert_design_dicts_to_objects(designs_list)
        else:
            return None

    def set_designs(self, designs: List[Design]):
        """Call ``set_designs`` command on proxy solver node in use.

        Parameters
        ----------
        List[Design]
            List of solved design instances.
        """
        if self.__current_proxy_solver is not None:
            responses: list[dict] = self.__class__.__convert_design_object_to_response(designs)
            self.__current_proxy_solver.set_designs(responses)

    # endregion

    def __validate_instances(self, instances: Iterable[ManagedInstance]):
        """Validate the managed instances for uniqueness.

        Parameters
        ----------
        instances : Iterable[ManagedInstance]
            Managed instances to be validated.

        Raises
        ------
        ValueError
            If there are duplicate uids among the managed instances.
        """
        seen_uids = set()
        for instance in instances:
            uid = instance.instance.uid
            if uid in seen_uids:
                raise ValueError(f"Duplicate uid found: {uid}")
            seen_uids.add(uid)

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
        if not self.__osl_instance.application.project:
            raise RuntimeError("No project loaded.")
        for node in self.__osl_instance.application.project.root_system.get_nodes():
            node.set_execution_options(ExecutionOption.INACTIVE)

    def __start_in_thread(self) -> None:
        """Target method to be started in a new thread."""
        for block in self.execution_order:
            self.__current_proxy_solver = None
            # set exec options for each instance in executable block
            for item, exec_opt in block.instances_with_execution_options:
                if isinstance(item, ProxySolverManagedParametricSystem):
                    self.__current_proxy_solver = item.solver_node
                item.instance.set_execution_options(exec_opt)
            # execute whole block
            if not self.__osl_instance.application.project:
                raise RuntimeError("No project loaded.")
            self.__osl_instance.application.project.start(wait_for_finished=True)
            # deactivate all instances, when finished
            self.__set_managed_instances_exec_options(ExecutionOption.INACTIVE, block.instances)
            self.__current_proxy_solver = None
        self.__is_complete = True

    def __execute_proxy_solver(self, proxy_solver: ProxySolverNode, callback: Callable) -> None:
        """Execute the proxy solver node using callback.

        Parameters
        ----------
        proxy_solver : ProxySolverNode
            Proxy solver to be executed.
        callback : Callable
            Callback obtaining input designs and returning results.
        """
        if not self.__osl_instance.application.project:
            raise RuntimeError("No project loaded.")
        self.__osl_instance.application.project.start(wait_for_finished=False)
        while True:
            status = self.__osl_instance.application.project.get_status()
            if status == "FINISHED":
                self.__osl_instance.log.info(f"Project status: {status}")
                break
            elif status == "STOPPED":
                self.__osl_instance.log.info(f"Project status: {status}")
                break
            design_list: List[dict] = proxy_solver.get_designs()
            if len(design_list):
                design_objects: List[Design] = self.__class__.__convert_design_dicts_to_objects(
                    design_list
                )
                responses_objects: List[Design] = callback(design_objects)
                responses_list = self.__class__.__convert_design_object_to_response(
                    responses_objects
                )
                proxy_solver.set_designs(responses_list)
            time.sleep(0.5)

    @staticmethod
    def __convert_design_dicts_to_objects(design_list: List[dict]) -> List[Design]:
        design_objects = []
        for design in design_list:
            parameters = [
                DesignVariable(name=parameter.get("name"), value=parameter.get("value"))
                for parameter in design.get("parameters") or []
            ]
            design_objects.append(Design(parameters=parameters, design_id=design["hid"]))
        return design_objects

    @staticmethod
    def __convert_design_object_to_response(responses_objects: List[Design]) -> List[dict]:
        responses_list = []
        for design in responses_objects:
            responses_list.append(
                {
                    "hid": design.id,
                    "responses": [
                        {"name": response.name, "value": response.value}
                        for response in design.responses
                    ],
                }
            )
        return responses_list


class ParametricDesignStudy(ParametricDesignStudyBase):
    """Custom mutable design study with full structural modification API."""

    def __init__(
        self,
        osl_instance: Optislang,
        managed_instances: Iterable[ManagedInstance],
        execution_blocks: Optional[Iterable[ExecutableBlock]] = None,
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

        """
        super().__init__(
            osl_instance=osl_instance,
            managed_instances=managed_instances,
            execution_blocks=execution_blocks,
        )

    def add_managed_instance(
        self,
        instance: ManagedInstance,
        execution_block_idx: Optional[int] = None,
        execution_option: ExecutionOption = ExecutionOption.ACTIVE,
    ) -> None:
        """Add a managed instance to the design study.

        Parameters
        ----------
        instance : ManagedInstance
            The managed instance to be added.
        execution_block_idx : int, optional
            The index of the execution block to which the instance should be added.
            If not provided, new execution block is created at the end of the execution order.
        execution_option : ExecutionOption, optional
            The execution option for the instance. Default is `ExecutionOption.ACTIVE`.

        Raises
        ------
        IndexError
            If the provided execution block index is out of range.
        """
        if self.find_managed_instance_by_uid(instance.instance.uid) is not None:
            raise ValueError(
                "Managed instance with uid `{}` already exists in the design study.".format(
                    instance.instance.uid
                )
            )
        if execution_block_idx is not None:
            if 0 <= execution_block_idx < len(self._execution_blocks_ref):
                self._execution_blocks_ref[execution_block_idx].add_instance(
                    instance, execution_option
                )
            else:
                raise IndexError("Execution block index out of range.")
        else:
            # Create a new execution block at the end of the execution order
            new_block = ExecutableBlock(((instance, execution_option),))
            self._execution_blocks_ref.append(new_block)
        self._managed_instances_ref.append(instance)

    def add_execution_block(self, block: ExecutableBlock, index: Optional[int] = None) -> None:
        """Add a new execution block to the design study.

        Parameters
        ----------
        block : ExecutableBlock
            The execution block to be added.
        index : int, optional
            The index at which to insert the new execution block. If not provided,
            the block is added at the end of the execution order.

        Raises
        ------
        IndexError
            If the provided index is out of range.

        Notes
        -----
        If managed instances in the new block are not already part of the design study,
        they will be added to the managed instances list.
        """
        if index is not None:
            if 0 <= index <= len(self._execution_blocks_ref):
                self._execution_blocks_ref.insert(index, block)
            else:
                raise IndexError("Execution block index out of range.")
        else:
            self._execution_blocks_ref.append(block)

        for instance in block.instances:
            if self.find_managed_instance_by_uid(instance.instance.uid) is None:
                self._managed_instances_ref.append(instance)

    def move_execution_block(self, from_idx: int, to_idx: int) -> None:
        """Move an execution block from one index to another.

        Parameters
        ----------
        from_idx : int
            The current index of the execution block to be moved.
        to_idx : int
            The target index where the execution block should be moved.

        Raises
        ------
        IndexError
            If either the `from_idx` or `to_idx` is out of range.
        """
        if not (0 <= from_idx < len(self._execution_blocks_ref)):
            raise IndexError("from_idx is out of range.")
        if not (0 <= to_idx < len(self._execution_blocks_ref)):
            raise IndexError("to_idx is out of range.")

        block = self._execution_blocks_ref.pop(from_idx)
        self._execution_blocks_ref.insert(to_idx, block)

    def remove_managed_instance(self, instance: ManagedInstance) -> None:
        """Remove a top level managed instance from the design study.

        Parameters
        ----------
        instance : ManagedInstance
            The managed instance to be removed.

        Notes
        -----
        - Managed instance is also removed from any execution block it belongs to,
          blocks without any instances are removed from the execution order.
        - Solver nodes cannot be removed separately, they must be removed together
          with the associated parametric system.

        """
        indices_to_remove = []
        for idx, item in enumerate(self._managed_instances_ref):
            if item.instance.uid == instance.instance.uid:
                indices_to_remove.append(idx)
        for idx in reversed(indices_to_remove):
            self._managed_instances_ref.pop(idx)

        # Remove the instance from any execution block it belongs to
        for block in self._execution_blocks_ref:
            block.remove_instance_by_uid(instance.instance.uid)
        self._execution_blocks_ref[:] = [
            block for block in self._execution_blocks_ref if block.instances
        ]

    def remove_execution_block(self, idx: int) -> None:
        """Remove an execution block by its index from the design study.

        Parameters
        ----------
        idx : int
            Index of the execution block to be removed.

        Raises
        ------
        IndexError
            If the provided index is out of range.

        Notes
        -----
        All managed instances within the removed block are also removed from the design study,
        unless they are also present in other execution blocks.
        """
        if 0 <= idx < len(self._execution_blocks_ref):
            block = self._execution_blocks_ref.pop(idx)
        else:
            raise IndexError("Execution block index out of range.")

        for instance in block.instances:
            exists_elsewhere = False
            for other_block in self._execution_blocks_ref:
                if other_block.get_instance_by_uid(instance.instance.uid) is not None:
                    exists_elsewhere = True
                    break
            if not exists_elsewhere:
                self.remove_managed_instance(instance)


class FixedParametricDesignStudy(ParametricDesignStudyBase, ABC):
    """Base class for template-managed fixed design studies."""

    def __init__(
        self,
        osl_instance: Optislang,
        managed_instances: Iterable[ManagedInstance],
        execution_blocks: Iterable[ExecutableBlock],
    ):
        super().__init__(osl_instance, managed_instances, execution_blocks)

    def apply_settings(self, **kwargs) -> None:
        """Apply template-specific settings to this fixed study.

        Notes
        -----
        This fallback implementation intentionally raises because generic fixed studies
        do not know template-specific settings semantics.
        """
        if kwargs:
            unknown = ", ".join(sorted(kwargs.keys()))
            raise TypeError(
                "Settings are not implemented for this fixed design study. "
                f"Unknown setting(s): {unknown}."
            )
        raise TypeError("Settings are not implemented for this fixed design study.")

    def convert_to_modifiable(self) -> ParametricDesignStudy:
        """Convert the fixed design study to a modifiable one.

        Returns
        -------
        ParametricDesignStudy
            A new instance of ``ParametricDesignStudy`` with independent instance/block
            containers while reusing the same managed-instance wrappers.
        """
        converted_instances = list(self.managed_instances)

        converted_blocks: list[ExecutableBlock] = []
        for block in self.execution_order:
            block_instances: list[Tuple[ManagedInstance, ExecutionOption]] = []
            for instance, execution_option in block.instances_with_execution_options:
                block_instances.append((instance, execution_option))
            converted_blocks.append(ExecutableBlock(block_instances))

        return ParametricDesignStudy(
            osl_instance=self.optislang,
            managed_instances=converted_instances,
            execution_blocks=converted_blocks,
        )

    @staticmethod
    def _apply_pre_registration_settings_to_managed_parametric_system(
        optislang: Optislang,
        parametric_system: ParametricSystem,
        parameters: Optional[Iterable[Parameter]] = None,
        parametric_system_name: Optional[str] = None,
        parametric_system_settings: Optional[GeneralAlgorithmSettings] = None,
    ) -> None:
        """Apply settings to the parametric system prior to registration of locations."""

        if parametric_system_name is not None:
            if not (optislang.osl_version.major, optislang.osl_version.minor) >= (25, 2):
                raise EnvironmentError(
                    "Setting name is not supported in optiSLang versions prior to 2025.2."
                )
            parametric_system.set_name(parametric_system_name)

        if parametric_system_settings is not None:
            property_dict = parametric_system_settings.convert_properties_to_dict()
            parametric_system.set_properties(property_dict)

        if parameters is not None:
            parameter_manager = parametric_system.parameter_manager
            for parameter in parameters:
                if parameter.name in parameter_manager.get_parameters_names():
                    parameter_manager.modify_parameter(parameter)
                else:
                    parameter_manager.add_parameter(parameter)

    @staticmethod
    def _apply_settings_to_solver_node(
        optislang: Optislang,
        solver_node: IntegrationNode,
        parameters: Iterable[Parameter],
        responses: Iterable[Response],
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
    ) -> None:
        """Apply settings to the solver node.

        Parameters
        ----------
        optislang : Optislang
            The optiSLang instance.
        solver_node : IntegrationNode
            The solver node to which settings will be applied.
        parameters : Iterable[Parameter]
            Parameters to be set on the solver node.
        responses : Iterable[Response]
            Responses to be set on the solver node.
        solver_name : Optional[str], optional
            Name to be set for the solver node. If not provided, the name will not be changed.
        solver_settings : Optional[GeneralNodeSettings], optional
            Settings to be applied to the solver node. If not provided, settings will not be changed.
        """
        if solver_name is not None:
            if not (optislang.osl_version.major, optislang.osl_version.minor) >= (25, 2):
                raise EnvironmentError(
                    "Setting name is not supported in optiSLang versions prior to 2025.2."
                )
            solver_node.set_name(solver_name)
        if solver_settings is not None:
            property_dict = solver_settings.convert_properties_to_dict()
            solver_node.set_properties(property_dict)

    @staticmethod
    def _apply_post_registration_settings(
        parametric_system: ParametricSystem,
        start_designs: Optional[Iterable[Design]] = None,
        criteria: Optional[Iterable[Criterion]] = None,
    ) -> None:
        """Apply settings to the design study after registration of locations."""
        if start_designs is not None:
            design_manager = parametric_system.design_manager
            design_manager.set_start_designs(start_designs)

        if criteria is not None:
            criterion_manager = parametric_system.criteria_manager
            for criterion in criteria:
                if criterion.name in criterion_manager.get_criteria_names():
                    criterion_manager.modify_criterion(criterion)
                else:
                    criterion_manager.add_criterion(criterion)


# region fixed (template-specific) parametric design studies
class ParametricSystemIntegrationDesignStudy(FixedParametricDesignStudy):
    """Fixed study created from ``ParametricSystemIntegrationTemplate``."""

    def apply_settings(
        self,
        parameters: Optional[Iterable[Parameter]] = None,
        responses: Optional[Iterable[Response]] = None,
        parametric_system_name: Optional[str] = None,
        parametric_system_settings: Optional[GeneralAlgorithmSettings] = None,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        start_designs: Optional[Iterable[Design]] = None,
        criteria: Optional[Iterable[Criterion]] = None,
    ) -> None:
        """Apply template-specific settings to this fixed study."""
        managed_instances = cast(ManagedParametricSystem, self.managed_instances[0])
        parametric_system = managed_instances.instance
        solver_node = managed_instances.solver_node

        self.__class__._apply_pre_registration_settings_to_managed_parametric_system(
            optislang=self.optislang,
            parametric_system=parametric_system,
            parameters=parameters,
            parametric_system_name=parametric_system_name,
            parametric_system_settings=parametric_system_settings,
        )
        self.__class__._apply_settings_to_solver_node(
            optislang=self.optislang,
            solver_node=solver_node,
            parameters=parameters,
            responses=responses,
            solver_name=solver_name,
            solver_settings=solver_settings,
        )
        self.__class__._apply_post_registration_settings(
            parametric_system=parametric_system,
            start_designs=start_designs,
            criteria=criteria,
        )


class GeneralAlgorithmDesignStudy(FixedParametricDesignStudy):
    """Fixed study created from ``GeneralAlgorithmTemplate``."""

    def apply_settings(
        self,
        parameters: Iterable[Parameter] = None,
        criteria: Iterable[Criterion] = None,
        responses: Iterable[Response] = None,
        algorithm_name: Optional[str] = None,
        algorithm_settings: Optional[GeneralAlgorithmSettings] = None,
        solver_name: Optional[str] = None,
        solver_settings: Optional[GeneralNodeSettings] = None,
        start_designs: Optional[Iterable[Design]] = None,
    ) -> None:
        """Apply template-specific settings to this fixed study."""
        managed_instances = cast(ManagedParametricSystem, self.managed_instances[0])
        parametric_system = managed_instances.instance
        solver_node = managed_instances.solver_node

        self.__class__._apply_pre_registration_settings_to_managed_parametric_system(
            optislang=self.optislang,
            parametric_system=parametric_system,
            parameters=parameters,
            parametric_system_name=algorithm_name,
            parametric_system_settings=algorithm_settings,
        )
        self.__class__._apply_settings_to_solver_node(
            optislang=self.optislang,
            solver_node=solver_node,
            parameters=parameters,
            responses=responses,
            solver_name=solver_name,
            solver_settings=solver_settings,
        )
        self.__class__._apply_post_registration_settings(
            parametric_system=parametric_system,
            start_designs=start_designs,
            criteria=criteria,
        )


class OptimizationOnMOPDesignStudy(FixedParametricDesignStudy):
    """Fixed study created from ``OptimizationOnMOPTemplate``."""

    def apply_settings(
        self,
        parameters: Iterable[Parameter] = None,
        criteria: Iterable[Criterion] = None,
        responses: Iterable[Response] = None,
        mop_predecessor: Node = None,
        optimizer_name: Optional[str] = None,
        optimizer_settings: Optional[GeneralAlgorithmSettings] = None,
        optimizer_start_designs: Optional[Iterable[Design]] = None,
        callback: Optional[Callable] = None,
        extrapolate: Optional[str] = None,
        number_of_best_designs_to_validate: int = None,
    ) -> None:
        """Apply template-specific settings to this fixed study."""

        # optimizer block
        if any(
            (
                mop_predecessor,
                parameters,
                criteria,
                responses,
                optimizer_name,
                optimizer_settings,
                optimizer_start_designs,
                extrapolate,
            )
        ):
            optimizer_instances = cast(ManagedParametricSystem, self.managed_instances[0])
            optimizer_algorithm = optimizer_instances.instance
            optimizer_node = optimizer_instances.solver_node

            if mop_predecessor is not None:
                optimizer_algorithm_input_slot = optimizer_algorithm.get_input_slots(
                    "IParameterManager"
                )[0]
                optimizer_algorithm_input_slot.disconnect()
                mop_predecessor.get_output_slots("OParameterManager")[0].connect_to(
                    optimizer_algorithm_input_slot
                )

                optimizer_node_input_slot = optimizer_node.get_input_slots("IMDBPath")[0]
                optimizer_node_input_slot.disconnect()
                mop_predecessor.get_output_slots("OMDBPath")[0].connect_to(
                    optimizer_node_input_slot
                )

                optimizer_algorithm.get_output_slots("IODesign")[0].connect_to(
                    optimizer_node.get_input_slots("IDesign")[0]
                )

            mop_solver_settings = (
                GeneralNodeSettings(
                    additional_settings={"ExtrapolationType": {"value": extrapolate}}
                )
                if extrapolate is not None
                else None
            )

            self.__class__._apply_pre_registration_settings_to_managed_parametric_system(
                optislang=self.optislang,
                parametric_system=optimizer_algorithm,
                parameters=parameters,
                parametric_system_name=optimizer_name,
                parametric_system_settings=optimizer_settings,
            )
            self.__class__._apply_settings_to_solver_node(
                optislang=self.optislang,
                solver_node=optimizer_node,
                parameters=parameters,
                responses=responses,
                solver_settings=mop_solver_settings,
            )
            self.__class__._apply_post_registration_settings(
                parametric_system=optimizer_algorithm,
                start_designs=optimizer_start_designs,
                criteria=criteria,
            )

        # validator block
        if any([parameters, criteria, responses, callback, number_of_best_designs_to_validate]):
            validator_managed_instance = cast(
                ProxySolverManagedParametricSystem, self.managed_instances[2]
            )
            validator_algorithm = validator_managed_instance.instance
            validator_node = validator_managed_instance.solver_node

            if callback is not None:
                validator_managed_instance.callback = callback

            self.__class__._apply_pre_registration_settings_to_managed_parametric_system(
                optislang=self.optislang,
                parametric_system=validator_algorithm,
                parameters=parameters,
            )
            self.__class__._apply_settings_to_solver_node(
                optislang=self.optislang,
                solver_node=validator_node,
                parameters=parameters,
                responses=responses,
            )
            self.__class__._apply_post_registration_settings(
                parametric_system=validator_algorithm,
                criteria=criteria,
            )

        # filter block
        if number_of_best_designs_to_validate is not None:
            filter_node_instance = cast(ManagedInstance, self.managed_instances[1])
            filter_node = cast(IntegrationNode, filter_node_instance.instance)

            getbestdesigns = {
                "First": {"name": "GetBestDesigns"},
                "Second": [
                    {"design_container": []},
                    {"design_entry": number_of_best_designs_to_validate},
                ],
            }

            dmm = filter_node.get_property("DataMiningManager")
            dmm["id_filter_list_map"]["OFilteredBestDesigns"] = [getbestdesigns]
            filter_node.set_property("DataMiningManager", dmm)
            filter_node.load()
            filter_node.register_location_as_output_slot(
                location="OFilteredBestDesigns", name="OFilteredBestDesigns"
            )


# endregion


# endregion
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
    def design_studies(self) -> Tuple[ParametricDesignStudyBase, ...]:
        """Managed design studies.

        Returns
        -------
        Tuple[ParametricDesignStudyBase, ...]
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

        self.__design_studies: List[ParametricDesignStudyBase] = []

    def append_design_study(
        self,
        design_study: ParametricDesignStudyBase,
    ) -> None:
        """Add an existing design study to the managed studies.

        Parameters
        ----------
        design_study: ParametricDesignStudyBase
            Instance of parametric design study.
        """
        if isinstance(design_study, ParametricDesignStudyBase):
            self.__design_studies.append(design_study)
        else:
            raise TypeError(
                "Expected instance of`ParametricDesignStudyBase`, but got `{}`".format(
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
            for design_study in self.__design_studies:
                design_study.delete()
        self.__design_studies.clear()

    def create_design_study(self, template: DesignStudyTemplate) -> ParametricDesignStudy:
        """Create a design study based on the provided template.

        Parameters
        ----------
        template : DesignStudyTemplate
            The template defining the design study.

        Returns
        -------
        ParametricDesignStudy
            The created design study.
        """
        if self.optislang.application.project:
            managed_instances, executable_blocks = template.create_design_study(
                self.optislang.application.project.root_system
            )
            design_study = ParametricDesignStudy(
                self.optislang, managed_instances, executable_blocks
            )
            self.__design_studies.append(design_study)
            return design_study
        else:
            raise RuntimeError("No project loaded.")

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

    def get_finished_design_studies(self) -> Tuple[ParametricDesignStudyBase, ...]:
        """Get all finished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudyBase, ...]
            Tuple of managed parametric studies that have been solved.
        """
        return tuple(
            [design_study for design_study in self.__design_studies if design_study.is_complete]
        )

    def get_unfinished_design_studies(self) -> Tuple[ParametricDesignStudyBase, ...]:
        """Get all unfinished design studies.

        Returns
        -------
        Tuple[ParametricDesignStudyBase, ...]
            Tuple of managed parametric studies that have not been solved.
        """
        return tuple(
            [design_study for design_study in self.__design_studies if not design_study.is_complete]
        )
