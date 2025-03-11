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

"""Contains classes to obtain operate with project parametric."""
from __future__ import annotations

import csv
from io import StringIO
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Union

from ansys.optislang.core.io import File, FileOutputFormat
from ansys.optislang.core.managers import (
    CriteriaManager,
    DesignManager,
    ParameterManager,
    ResponseManager,
)
from ansys.optislang.core.project_parametric import (
    ConstraintCriterion,
    Criterion,
    Design,
    DesignStatus,
    LimitStateCriterion,
    Parameter,
    Response,
)

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpCriteriaManagerProxy(CriteriaManager):
    """Contains methods for obtaining criteria."""

    __PROPERTY_MAPPING = {"limit_expression": "limit"}

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpCriteriaManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the criteria manager."""
        return f"CriteriaManager uid: {self.__uid}"

    def add_criterion(self, criterion: Criterion) -> None:
        """Add criterion to the system.

        .. note:: Method is supported for Ansys optiSLang version >= 23.2 only.

        Parameters
        ----------
        criterion: Criterion
            Criterion to be created in the system.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for Ansys optiSLang version >= 23.2.")
        else:
            self.__osl_server.add_criterion(
                uid=self.__uid,
                criterion_type=criterion.criterion.name,
                expression=criterion.expression,
                name=criterion.name,
                limit=(
                    criterion.limit_expression
                    if isinstance(criterion, (ConstraintCriterion, LimitStateCriterion))
                    else None
                ),
            )

    def get_criteria(self) -> Tuple[Criterion, ...]:
        """Get the criteria of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the criterion for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        container = (
            self.__osl_server.get_actor_properties(uid=self.__uid)
            .get("Criteria", {})
            .get("sequence", [{}])
        )
        return tuple([Criterion.from_dict(criterion_dict) for criterion_dict in container])

    def get_criteria_names(self) -> Tuple[str, ...]:
        """Get all criteria names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all criteria names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        container = (
            self.__osl_server.get_actor_properties(uid=self.__uid)
            .get("Criteria", {})
            .get("sequence", [{}])
        )
        return tuple([criterion_dict["First"] for criterion_dict in container])

    def modify_criterion(self, criterion: Criterion) -> None:
        """Modify criterion in the system.

        .. note:: Method is supported for Ansys optiSLang version >= 23.2 only.

        Parameters
        ----------
        criterion : Criterion
            Criterion to be modified. Criterion name is used as idefentifier.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.modify_criterion_property(
                criterion_name=criterion.name,
                property_name="type",
                property_value=criterion.criterion.name,
            )
            self.modify_criterion_property(
                criterion_name=criterion.name,
                property_name="expression",
                property_value=criterion.expression,
            )
            if isinstance(criterion, (ConstraintCriterion, LimitStateCriterion)):
                self.modify_criterion_property(
                    criterion_name=criterion.name,
                    property_name="limit",
                    property_value=criterion.limit_expression,
                )

    def modify_criterion_property(
        self, criterion_name: str, property_name: str, property_value: Any
    ) -> None:
        """Modify property of criterion in the system.

        .. note:: Method is supported for Ansys optiSLang version >= 23.2 only.

        Parameters
        ----------
        criterion_name : str
            Name of criterion to be modified.
        property_name: str
            Name of property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.set_criterion_property(
                uid=self.__uid,
                criterion_name=criterion_name,
                name=self.__PROPERTY_MAPPING.get(property_name, property_name),
                value=property_value,
            )

    def remove_all_criteria(self) -> None:
        """Remove all criteria from the system.

        .. note:: Method is supported for Ansys optiSLang version >= 23.2 only.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.remove_criteria(uid=self.__uid)

    def remove_criterion(self, criterion_name: str) -> None:
        """Remove criterion from the system.

        .. note:: Method is supported for Ansys optiSLang version >= 23.2 only.

        Parameters
        ----------
        criterion_name : str
            Name of the criterion to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if (self.__osl_server.osl_version.major + self.__osl_server.osl_version.minor / 10) < 23.2:
            raise NotImplementedError("Method is supported for optiSLang version >= 23.2.")
        else:
            self.__osl_server.remove_criterion(uid=self.__uid, name=criterion_name)


class TcpDesignManagerProxy(DesignManager):
    """Contains methods for obtaining designs."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpDesignManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def _get_status_info(
        self,
        hid: str,
        include_designs: bool = True,
        include_design_values: Optional[bool] = True,
        include_non_scalar_design_values: Optional[bool] = False,
        include_algorithm_info: Optional[bool] = False,
    ) -> Dict:
        """Get status info about actor defined by actor uid and state hid.

        Parameters
        ----------
        hid : str
            State/Design hierarchical id.
        include_designs : bool, optional
           Include (result) designs in status info response. By default ``True``.
        include_design_values : Optional[bool], optional
            Include values in (result) designs. By default ``True``.
        include_non_scalar_design_values : Optional[bool], optional
            Include non scalar values in (result) designs. By default ``False``.
        include_algorithm_info : Optional[bool], optional
            Include algorithm result info in status info response, by default ``False``.

        Returns
        -------
        Dict
            Info about actor defined by uid.
        """
        return self.__osl_server.get_actor_status_info(
            self.__uid,
            hid=hid,
            include_designs=include_designs,
            include_design_values=include_design_values,
            include_non_scalar_design_values=include_non_scalar_design_values,
            include_algorithm_info=include_algorithm_info,
        )

    def get_design(self, id: str) -> Design:
        """Get design by id.

        Parameters
        ----------
        id : str
            Design id.

        Returns
        -------
        Design
            Design object.

        Notes
        -----
        Information about `pareto_design` property is not provided by this query.
        """
        design = self.__osl_server.get_result_design(
            uid=self.__uid,
            design_id=id,
        )["design"]
        return Design(
            parameters=dict(zip(design["parameter_names"], design["parameter_values"])),
            constraints=dict(zip(design["constraint_names"], design["constraint_values"])),
            limit_states=dict(zip(design["limit_state_names"], design["limit_state_values"])),
            objectives=dict(zip(design["objective_names"], design["objective_values"])),
            responses=dict(zip(design["response_names"], design["response_values"])),
            feasibility=design["feasible"],
            design_id=design["hid"],
            status=DesignStatus.from_str(design["status"]),
            pareto_design=None,
        )

    def get_designs(
        self,
        hid: Optional[str] = None,
        include_design_values=True,
        include_non_scalar_design_values=False,
    ) -> Tuple[Design]:
        """Get designs for a given state.

        Parameters
        ----------
        hid : Optional[str], optional
            State/Design hierarchical id. By default ``None``.
        include_design_values : bool, optional
            Include values. By default ``True``.
        include_non_scalar_design_values : Optional[bool], optional
            Include non scalar values. By default ``False``.

        Returns
        -------
        Tuple[Design]
            Tuple of designs for a given state.
        """
        design_classes = []
        status_info = self._get_status_info(
            hid=hid,
            include_designs=True,
            include_design_values=include_design_values,
            include_non_scalar_design_values=include_design_values
            and include_non_scalar_design_values,
            include_algorithm_info=False,
        )
        designs = status_info.get("designs", {})
        design_states = status_info["design_status"]

        if include_design_values:
            design_values = designs.get("values")
            for design_value, design_state in zip(design_values, design_states):
                if design_value["hid"] != design_state["id"]:
                    raise ValueError(f'{design_value["hid"]} != {design_state["id"]}')
                design_classes.append(
                    Design(
                        parameters=dict(
                            zip(
                                designs.get("parameter_names", []),
                                design_value.get("parameter_values", []),
                            )
                        ),
                        constraints=dict(
                            zip(
                                designs.get("constraint_names", []),
                                design_value.get("constraint_values", []),
                            )
                        ),
                        limit_states=dict(
                            zip(
                                designs.get("limit_state_names", []),
                                design_value.get("limit_state_values", []),
                            )
                        ),
                        objectives=dict(
                            zip(
                                designs.get("objective_names", []),
                                design_value.get("objective_values", []),
                            )
                        ),
                        responses=dict(
                            zip(
                                designs.get("response_names", []),
                                design_value.get("response_values", []),
                            )
                        ),
                        feasibility=design_state["feasible"],
                        design_id=design_state["id"],
                        status=DesignStatus.from_str(design_state["status"]),
                        pareto_design=design_state["pareto_design"],
                    )
                )
        else:
            for design_state in design_states:
                design_classes.append(
                    Design(
                        feasibility=design_state["feasible"],
                        design_id=design_state["id"],
                        status=DesignStatus.from_str(design_state["status"]),
                        pareto_design=design_state["pareto_design"],
                    )
                )
        return tuple(design_classes)

    def save_designs_as_json(self, hid: str, file_path: Union[Path, str]) -> File:
        """Save designs for a given state to JSON file.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_path : Union[Path, str]
            Path to the file.

        Returns
        -------
        File
            Object representing saved file.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when the `hid` is `None`
            -or-
            `file_path` is `None` or unsupported type.
        ValueError
            Raised when ``hid`` does not exist.
        """
        return self.__save_designs_as(hid, file_path, FileOutputFormat.JSON)

    def save_designs_as_csv(self, hid: str, file_path: Union[Path, str]) -> File:
        """Save designs for a given state to CSV file.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_path : Union[Path, str]
            Path to the file.

        Returns
        -------
        File
            Object representing saved file.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when the `hid` is `None`
            -or-
            `file_path` is `None` or unsupported type.
        ValueError
            Raised when ``hid`` does not exist.
        """
        return self.__save_designs_as(hid, file_path, FileOutputFormat.CSV)

    def __save_designs_as(self, hid: str, file_path: Union[Path, str], format: FileOutputFormat):
        """Save designs for a given state.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_path : Union[Path, str]
            Path to the file.
        format : FileOutputFormat
            Format of the file.

        Returns
        -------
        File
            Object representing saved file.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when the `hid` is `None`
            -or-
            `file_path` is `None` or unsupported type.
        ValueError
            Raised when ``format`` is not unsupported
            -or-
            ``hid`` does not exist.
        """
        if hid is None:
            raise TypeError("Actor's state cannot be `None`.")
        if file_path is None:
            raise TypeError("Path to the file cannot be `None`.")
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if not isinstance(file_path, Path):
            raise TypeError(
                "Type of the `file_path` argument is not supported: `file_path` = "
                f"`{type(file_path)}`."
            )

        status_info = self._get_status_info(
            hid=hid,
            include_designs=True,
            include_design_values=True,
            include_non_scalar_design_values=(format == FileOutputFormat.JSON),
            include_algorithm_info=False,
        )
        designs = status_info["designs"]
        design_states = status_info["design_status"]
        for design, state in zip(designs["values"], design_states):
            if design["hid"] != state["id"]:
                raise ValueError(f'{design["hid"]} != {status_info["id"]}')
            to_append = {
                key: state[key] for key in ("feasible", "status", "pareto_design", "directory")
            }
            design.update(to_append)

        if format == FileOutputFormat.JSON:
            file_output = json.dumps(designs)
            newline = None
        elif format == FileOutputFormat.CSV:
            file_output = self.__convert_design_dict_to_csv(designs)
            newline = ""
        else:
            raise ValueError(f"Output file format `{format}` is not supported.")

        with open(file_path, "w", newline=newline) as f:
            f.write(file_output)
        return File(file_path)

    @staticmethod
    def filter_designs_by(
        designs: Iterable[Design],
        hid: Optional[str] = None,
        status: Optional[DesignStatus] = None,
        pareto_design: Optional[bool] = None,
        feasible: Optional[bool] = None,
    ) -> Tuple[Design]:
        """Filter designs by given parameters.

        Parameters
        ----------
        designs : Iterable[Design]
            Designs to be filtered.
        hid : Optional[str], optional
            State/Design hierarchical id. By default ``None``.
        status : Optional[DesignStatus], optional
            Design status. By default ``None``.
        pareto_design : Optional[bool], optional
            Pareto flag. By default ``None``.
        feasible : Optional[bool], optional
            Feasibility of design. By default ``None``.

        Returns
        -------
        Tuple[Design]
            Tuple of filtered designs
        """

        def filter_condition(design: Design) -> bool:
            conditions = [
                hid is None or design.id == hid,
                status is None or design.status == status,
                pareto_design is None or design.pareto_design == pareto_design,
                feasible is None or design.feasibility == feasible,
            ]
            return all(conditions)

        return tuple([design for design in filter(filter_condition, designs)])

    @staticmethod
    def sort_designs_by_hid(designs: Iterable[Design]) -> Tuple[Design]:
        """Sort designs by hierarchical id.

        Parameters
        ----------
        designs : Iterable[Design]
            Designs to be sorted.

        Returns
        -------
        Tuple[Design]
            Tuple of sorted designs.
        """
        sorted_designs = sorted(
            designs, key=lambda design: [int(part) for part in design.id.split(".")]
        )
        return tuple(sorted_designs)

    @staticmethod
    def __convert_design_dict_to_csv(designs: dict) -> str:
        csv_buffer = StringIO()
        try:
            csv_writer = csv.writer(csv_buffer)
            header = ["Design"]
            header.append("Feasible")
            header.append("Status")
            header.append("Pareto")
            header.extend(designs["constraint_names"])
            header.extend(designs["limit_state_names"])
            header.extend(designs["objective_names"])
            header.extend(designs["parameter_names"])
            header.extend(designs["response_names"])
            csv_writer.writerow(header)
            for design in designs["values"]:
                line = [design["hid"]]
                line.append(design["feasible"])
                line.append(design["status"])
                line.append(design["pareto_design"])
                line.extend(design["constraint_values"])
                line.extend(design["limit_state_values"])
                line.extend(design["objective_values"])
                line.extend(design["parameter_values"])
                line.extend(design["response_values"])
                csv_writer.writerow(line)
            return csv_buffer.getvalue()
        finally:
            if csv_buffer is not None:
                csv_buffer.close()


class TcpParameterManagerProxy(ParameterManager):
    """Contains methods for obtaining parameters."""

    __PROPERTY_MAPPING = {
        "operation": "dependency_expression",
    }

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpParameterManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the parameter manager."""
        return f"ParameterManager uid: {self.__uid}"

    def add_parameter(self, parameter: Parameter) -> None:
        """Add parameter to the system.

        Parameters
        ----------
        parameter: Parameter
            Parameter to be created in the system.

        Raises
        ------
        NameError
            Raised when the parameter with the given name already exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        if self.__get_parameter_idx(container=container, parameter_name=parameter.name) is not None:
            raise NameError(
                f"Parameter `{parameter.name}` already exists, choose another name"
                " or modify this parameter instead."
            )
        else:
            container.append(parameter.to_dict())
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )

    def get_parameters(self) -> Tuple[Parameter, ...]:
        """Get the parameters of the system.

        Returns
        -------
        Tuple[Parameter, ...]
            Tuple of the parameters for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        return tuple([Parameter.from_dict(parameter_dict) for parameter_dict in container])

    def get_parameters_names(self) -> Tuple[str, ...]:
        """Get all parameter names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all parameter names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        return tuple([parameter["name"] for parameter in container])

    def modify_parameter(self, parameter: Parameter):
        """Modify parameter in the system.

        Parameters
        ----------
        parameter: Parameter
            Parameter to be modified. Parameter name is used as identifier.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter.name)
        if idx is not None:
            parameter.id = container[idx]["id"]
            container[idx] = parameter.to_dict()
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )
        else:
            raise NameError(
                f"Parameter `{parameter.name}` doesn't exist in current parametric system."
            )

    def modify_parameter_property(
        self, parameter_name: str, property_name: str, property_value: Any
    ) -> None:
        """Modify property of parameter in the system.

        Parameters
        ----------
        parameter_name: str
            Name of the parameter to be modified.
        property_name: str
            Name of the property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter_name)
        if idx is not None:
            container[idx][
                self.__PROPERTY_MAPPING.get(property_name, property_name)
            ] = property_value
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )
        else:
            raise NameError(
                f"Parameter `{parameter_name}` doesn't exist in current parametric system."
            )

    def remove_all_parameters(self) -> None:
        """Remove all parameters from the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        parameter_manager["parameter_container"] = []
        self.__osl_server.set_actor_property(
            actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
        )

    def remove_parameter(self, parameter_name: str) -> None:
        """Remove parameter from the system.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parameter_manager, container = self.__get_parameter_container()
        idx = self.__get_parameter_idx(container=container, parameter_name=parameter_name)
        if idx is not None:
            container.pop(idx)
            parameter_manager["parameter_container"] = container
            self.__osl_server.set_actor_property(
                actor_uid=self.__uid, name="ParameterManager", value=parameter_manager
            )

        else:
            raise NameError(
                f"Parameter `{parameter_name}` doesn't exist in current parametric system."
            )

    def __get_parameter_container(self) -> Tuple[Dict[str, list], List[dict]]:
        parameter_manager = self.__osl_server.get_actor_properties(uid=self.__uid)[
            "ParameterManager"
        ]
        container = parameter_manager["parameter_container"]
        return parameter_manager, container

    @staticmethod
    def __get_parameter_idx(container: list, parameter_name: str) -> Optional[int]:
        for idx, parameter in enumerate(container):
            if parameter["name"] == parameter_name:
                return idx
        return None


class TcpResponseManagerProxy(ResponseManager):
    """Contains methods for obtaining responses."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpResponseManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the response manager."""
        return f"ResponseManager uid: {self.__uid}"

    def get_responses(self) -> Tuple[Response, ...]:
        """Get the responses of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the responses for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        responses = []
        for key, res_dict in container.items():
            responses.append(Response.from_dict(key, res_dict))
        return tuple(responses)

    def get_responses_names(self) -> Tuple[str, ...]:
        """Get all responses names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all responses names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        return tuple(container.keys())
