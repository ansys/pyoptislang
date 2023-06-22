"""Contains classes to obtain operate with project parametric."""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Dict, Iterable, List, Mapping, Tuple, Union

from ansys.optislang.core.managers import CriteriaManager, ParameterManager, ResponseManager
from ansys.optislang.core.project_parametric import (
    ConstraintCriterion,
    Criterion,
    DesignStatus,
    DesignVariable,
    LimitStateCriterion,
    ObjectiveCriterion,
    Parameter,
    Response,
    VariableCriterion,
)

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpCriteriaManagerProxy(CriteriaManager):
    """Contains methods for obtaining criteria."""

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
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props.get("properties", {}).get("Criteria", {}).get("sequence", [{}])
        criteria = []
        for criterion_dict in container:
            criteria.append(Criterion.from_dict(criterion_dict))
        return tuple(criteria)

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
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props.get("properties", {}).get("Criteria", {}).get("sequence", [{}])
        criteria_list = []
        for par in container:
            criteria_list.append(par["First"])
        return tuple(criteria_list)


class TcpParameterManagerProxy(ParameterManager):
    """Contains methods for obtaining parameters."""

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
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters = []
        for par_dict in container:
            parameters.append(Parameter.from_dict(par_dict))
        return tuple(parameters)

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
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters_list = []
        for par in container:
            parameters_list.append(par["name"])
        return tuple(parameters_list)


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


class Design:
    """Stores information about the design point, exclusively for the root system.

    Parameters
    ----------
    parameters : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Parameter, DesignVariable]],
    ], optional
        Dictionary of parameters and their values {'name': value, ...}
        or an iterable of design variables or parameters.
    constraints : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[ConstraintCriterion, DesignVariable]],
    ], optional
        Dictionary of constraint criteria and their values {'name': value, ...}
        or an iterable of design variables or constraint criteria.
    limit_states : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of limit state criteria and their values {'name': value, ...}
        or an iterable of design variables or limist state criteria.
    objectives : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of objective criteria and their values {'name': value, ...}
        or an iterable of design variables or objective criteria.
    variables : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of variable criteria and their values {'name': value, ...}
        or an iterable of design variables or variable criteria.
    responses : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Response, DesignVariable]],
    ], optional
        Dictionary of responses and their values {'name': value, ...}
        or an iterable of design variables or responses.
    feasibility: Union[bool, None], optional
        Determines whether design is feasible, defaults to `None` (no info about feasibility)
    design_id: Union[int, None], optional
        Design's id, defaults to `None`.
    status: DesignStatus, optional
        Design's status, defaults to `DesignStatus.IDLE`.

    Examples
    --------
    Get the reference design:

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> root_system = osl.project.root_system
    >>> design = root_system.get_reference_design()
    >>> design.set_parameter_by_name(parameter = 'a', value = 2)
    >>> print(design)
    >>> osl.dispose()
    """

    def __init__(
        self,
        parameters: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[Parameter, DesignVariable]],
        ] = [],
        constraints: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[LimitStateCriterion, DesignVariable]],
        ] = [],
        limit_states: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[LimitStateCriterion, DesignVariable]],
        ] = [],
        objectives: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[ObjectiveCriterion, DesignVariable]],
        ] = [],
        variables: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[VariableCriterion, DesignVariable]],
        ] = [],
        responses: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[Response, DesignVariable]],
        ] = [],
        feasibility: Union[bool, None] = None,
        design_id: Union[int, None] = None,
        status: DesignStatus = DesignStatus.IDLE,
    ) -> None:
        """Initialize a new instance of the ``TcpDesign`` class."""
        self.__constraints: List[DesignVariable] = []
        self.__feasibility: Union[bool, None] = feasibility
        self.__id: Union[int, None] = design_id
        self.__limit_states: List[DesignVariable] = []
        self.__objectives: List[DesignVariable] = []
        self.__parameters: List[DesignVariable] = []
        self.__responses: List[DesignVariable] = []
        self.__status: DesignStatus = status
        self.__variables: List[DesignVariable] = []

        # parameters
        if parameters:
            self.__parameters = self.__parse_parameters_to_designvariables(parameters=parameters)
        # criteria
        if constraints:
            self.__constraints = self.__parse_criteria_to_designvariables(criteria=constraints)
        if limit_states:
            self.__limit_states = self.__parse_criteria_to_designvariables(criteria=limit_states)
        if objectives:
            self.__objectives = self.__parse_criteria_to_designvariables(criteria=objectives)
        if variables:
            self.__variables = self.__parse_criteria_to_designvariables(criteria=variables)
        # responses
        if responses:
            self.__responses = self.__parse_responses_to_designvariables(responses=responses)

    def __str__(self) -> str:
        """Return information about the design."""
        return (
            f"ID: {self.id}\n"
            f"Status: {self.__status.name}\n"
            f"Feasibility: {self.__feasibility}\n"
            f"Criteria:\n"
            f"   constraints: {self.constraints_names}\n"
            f"   objectives: {self.objectives_names}\n"
            f"   limit_states: {self.limit_states_names}\n"
            f"Parameters: {self.parameters_names}\n"
            f"Responses: {self.responses_names}\n"
            f"Variables: {self.variables_names}\n"
        )

    def __deepcopy__(self, memo) -> Design:
        """Return deep copy of given Design."""
        return Design(
            parameters=copy.deepcopy(self.parameters),
            constraints=copy.deepcopy(self.constraints),
            limit_states=copy.deepcopy(self.limit_states),
            objectives=copy.deepcopy(self.objectives),
            variables=copy.deepcopy(self.variables),
            responses=copy.deepcopy(self.responses),
            feasibility=self.feasibility,
            design_id=self.id,
            status=self.status,
        )

    @property
    def constraints(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all constraints."""
        return tuple(self.__constraints)

    @property
    def constraints_names(self) -> Tuple[str, ...]:
        """Tuple of all constraint names."""
        return tuple([constraint.name for constraint in self.__constraints])

    @property
    def feasibility(self) -> Union[bool, None]:
        """Feasibility of the design. If the design is not evaluated, ``None`` is returned."""
        return self.__feasibility

    @property
    def id(self) -> Union[int, None]:
        """ID of the design. If no ID is assigned, ``None`` is returned."""
        return self.__id

    @property
    def limit_states(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all limit states."""
        return tuple(self.__limit_states)

    @property
    def limit_states_names(self) -> Tuple[str, ...]:
        """Tuple of all limit state names."""
        return tuple([limit_state.name for limit_state in self.__limit_states])

    @property
    def objectives(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all objectives."""
        return tuple(self.__objectives)

    @property
    def objectives_names(self) -> Tuple[str, ...]:
        """Tuple of all objective names."""
        return tuple([objective.name for objective in self.__objectives])

    @property
    def parameters(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all parameters."""
        return tuple(self.__parameters)

    @property
    def parameters_names(self) -> Tuple[str, ...]:
        """Tuple of all parameter names."""
        return tuple([parameter.name for parameter in self.__parameters])

    @property
    def responses(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all responses."""
        return tuple(self.__responses)

    @property
    def responses_names(self) -> Tuple[str, ...]:
        """Tuple of all response names."""
        return tuple([response.name for response in self.__responses])

    @property
    def status(self) -> DesignStatus:
        """Status of the ``Design`` class instance."""
        return self.__status

    @property
    def variables(self) -> Tuple[DesignVariable, ...]:
        """Tuple of all variables."""
        return tuple(self.__variables)

    @property
    def variables_names(self) -> Tuple[str, ...]:
        """Tuple of all variable names."""
        return tuple([variable.name for variable in self.__variables])

    def clear_parameters(self) -> None:
        """Remove all defined parameters from the design."""
        self.__parameters.clear()

    def copy_unevaluated_design(self) -> Design:
        """Create a deep copy of the unevaluated design.

        Returns
        -------
        Design
            Deep copy of the unevaluated design.
        """
        return Design(
            parameters=copy.deepcopy(self.parameters),
            constraints=self.__reset_output_value(copy.deepcopy(self.constraints)),
            limit_states=self.__reset_output_value(copy.deepcopy(self.limit_states)),
            objectives=self.__reset_output_value(copy.deepcopy(self.objectives)),
            variables=self.__reset_output_value(copy.deepcopy(self.variables)),
        )

    def remove_parameter(self, name: str) -> None:
        """Remove a parameter from the design.

        Parameters
        ----------
        name: str
            Name of the parameter.
        """
        index = self.__find_name_index(name, type_="parameter")
        if index is not None:
            self.__parameters.pop(index)

    def __reset(self) -> None:
        """Reset the status and feasibilit, clear output values."""
        self.__status = DesignStatus.IDLE
        self.__feasibility = None
        self.__constraints.clear()
        self.__limit_states.clear()
        self.__objectives.clear()
        self.__responses.clear()
        self.__variables.clear()

    def set_parameter(
        self,
        parameter: Union[Parameter, DesignVariable],
        reset_output: bool = True,
    ) -> None:
        """Set the value of a parameter by instance or add a new parameter.

        If no instance is specified,  a new parameter is added.

        Parameters
        ----------
        parameter: Union[Parameter, DesignVariable]
            Instance of the ``Parameter`` or ``DesignVariable`` class.
        reset_output: bool, optional
            Whether to reset the status and feasibility and then delete the output
            values. The default is ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when an invalid type of parameter is passed.
        """
        if reset_output:
            self.__reset()

        if isinstance(parameter, Parameter):
            value = parameter.reference_value
        elif isinstance(parameter, DesignVariable):
            value = parameter.value
        else:
            raise TypeError(f"Invalid type of parameter: `{type(parameter)}`.")

        index = self.__find_name_index(name=parameter.name, type_="parameter")
        if index is not None:
            self.__parameters[index].value = value
        else:
            self.__parameters.append(DesignVariable(name=parameter.name, value=value))

    def set_parameter_by_name(
        self,
        name: str,
        value: Union[str, float, bool, None] = None,
        reset_output: bool = True,
    ) -> None:
        """
        Set the value of a parameter by name or add a new parameter.

        If no name is specified,  a new parameter is added.

        Parameters
        ----------
        name: str
            Name of the parameter.
        value: float
            Value of the parameter.
        reset_output: bool, optional
            Whether to reset the status and feasibility and then delete the output
            values. The default is ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when an invalid type of parameter is passed.
        """
        if reset_output:
            self.__reset()

        if isinstance(name, str):
            index = self.__find_name_index(name=name, type_="parameter")
        else:
            raise TypeError(f"Invalid type of name: `{type(name)}`.")

        if index is not None:
            self.__parameters[index].value = value
        else:
            self.__parameters.append(DesignVariable(name=name, value=value))

    def _receive_results(self, results: Dict) -> None:
        """Store received results.

        Parameters
        ----------
        results: Dict
            Output from the ``evaluate_design`` server command.
        """
        self.__reset()
        self.__id = results["result_design"]["hid"]
        self.__feasibility = results["result_design"]["feasible"]
        self.__status = DesignStatus.from_str(results["result_design"]["status"])

        # constraint
        for position, constraint in enumerate(results["result_design"]["constraint_names"]):
            self.__constraints.append(
                DesignVariable(
                    name=constraint,
                    value=results["result_design"]["constraint_values"][position],
                )
            )
        # limit state
        for position, limit_state in enumerate(results["result_design"]["limit_state_names"]):
            self.__limit_states.append(
                DesignVariable(
                    name=limit_state,
                    value=results["result_design"]["limit_state_values"][position],
                )
            )
        # objective
        for position, objective in enumerate(results["result_design"]["objective_names"]):
            self.__objectives.append(
                DesignVariable(
                    name=objective,
                    value=results["result_design"]["objective_values"][position],
                )
            )
        # responses
        for position, response in enumerate(results["result_design"]["response_names"]):
            self.__responses.append(
                DesignVariable(
                    name=response,
                    value=results["result_design"]["response_values"][position],
                )
            )
        # variables
        for position, variable in enumerate(results["result_design"]["variable_names"]):
            self.__variables.append(
                DesignVariable(
                    name=variable,
                    value=results["result_design"]["variable_values"][position],
                )
            )

    def __find_name_index(self, name: str, type_: str) -> Union[int, None]:
        """Find the index of a criterion, parameter, response, or variable by name.

        Parameters
        ----------
        name: str
            Name of the criterion, parameter, response, or variable.
        type_: str
            Union['constraint', 'limit_state', 'objective', 'parameter', 'response', 'variable']

        Returns
        -------
        Union[int, None]
            Position of the name in the list. If the name is not found, ``None`` is returned.

        Raises
        ------
        TypeError
            Raised when an unknown type is given.
        RuntimeError
            Raised when multiple instances of a a design variable with the same name are found.
        """
        indices = []
        if type_ == "constraint":
            search_in = self.__constraints
        elif type_ == "limit_state":
            search_in = self.__limit_states
        elif type_ == "objective":
            search_in = self.__objectives
        elif type_ == "parameter":
            search_in = self.__parameters
        elif type_ == "response":
            search_in = self.__responses
        elif type_ == "variable":
            search_in = self.__variables
        else:
            raise TypeError(f"Unknown type_: ``{type(type_)}``.")

        for index, parameter in enumerate(search_in):
            if parameter.name == name:
                indices.append(index)
        if len(indices) > 1:
            raise RuntimeError(f"Name `{name}` of `{type_}` is not unique.")
        elif len(indices) == 0:
            return None
        return indices[0]

    def __parse_parameters_to_designvariables(
        self,
        parameters: Union[
            Mapping[str, Union[bool, str, float, None]], Iterable[Union[Parameter, DesignVariable]]
        ],
    ) -> List[DesignVariable]:
        """Parse parameters to design variables.

        Parameters
        ----------
        parameters : Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[Parameter, DesignVariable]],
            ], optional
        Dictionary of parameters and their values {'name': value, ...}
        or an iterable of design variables or parameters.

        Returns
        -------
        List[DesignVariable]
            List of design variables.

        Raises
        ------
        TypeError
            Raised when unsupported type of parameter is given.
        """
        parameters_list = []
        if isinstance(parameters, dict):
            for name, value in parameters.items():
                parameters_list.append(DesignVariable(name=name, value=value))
        else:
            for parameter in parameters:
                if isinstance(parameter, Parameter):
                    value = parameter.reference_value
                elif isinstance(parameter, DesignVariable):
                    value = parameter.value
                else:
                    raise TypeError(f"Parameters type: ``{type(parameter)}`` is not supported.")
                parameters_list.append(
                    DesignVariable(
                        name=parameter.name,
                        value=value,
                    )
                )
        return parameters_list

    def __parse_criteria_to_designvariables(
        self,
        criteria: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[
                Union[
                    ConstraintCriterion,
                    LimitStateCriterion,
                    ObjectiveCriterion,
                    VariableCriterion,
                    DesignVariable,
                ]
            ],
        ],
    ) -> List[DesignVariable]:
        """Parse criteria to design variables.

        Parameters
        ----------
        criteria : Union[
                Mapping[str, Union[bool, str, float, None]],
                Iterable[Union[
                    ConstraintCriterion,
                    LimitStateCriterion,
                    ObjectiveCriterion,
                    VariableCriterion,
                    DesignVariable],
                    ],
                ]
        Dictionary of criteria and their values {'name': value, ...}
        or an iterable of design variables or criteria.

        Returns
        -------
        List[DesignVariable]
            List of design variables.

        Raises
        ------
        TypeError
            Raised when unsupported type of criterion is given.
        """
        criteria_list = []
        if isinstance(criteria, dict):
            for name, value in criteria.items():
                criteria_list.append(DesignVariable(name=name, value=value))
        else:
            for criterion in criteria:
                if isinstance(criterion, (Criterion, DesignVariable)):
                    value = criterion.value
                    criteria_list.append(DesignVariable(name=criterion.name, value=criterion.value))
                else:
                    raise TypeError(f"Criterion type: ``{type(criterion)}`` is not supported.")
        return criteria_list

    def __parse_responses_to_designvariables(
        self,
        responses: Union[
            Mapping[str, Union[bool, str, float, None]],
            Iterable[Union[Response, DesignVariable]],
        ],
    ) -> List[DesignVariable]:
        """Parse responses to design variables.

        Parameters
        ----------
        criteria : Union[
                Mapping[str, Union[bool, str, float, None]],
                Iterable[Union[Response, DesignVariable]],
                ]
        Dictionary of responses and their values {'name': value, ...}
        or an iterable of design variables or responses.

        Returns
        -------
        List[DesignVariable]
            List of design variables.

        Raises
        ------
        TypeError
            Raised when unsupported type of criterion is given.
        """
        responses_list = []
        if isinstance(responses, dict):
            for name, value in responses.items():
                responses_list.append(DesignVariable(name=name, value=value))
        else:
            for response in responses:
                if isinstance(response, (Response, DesignVariable)):
                    value = response.reference_value
                    responses_list.append(
                        DesignVariable(name=response.name, value=response.reference_value)
                    )
                else:
                    raise TypeError(f"Response type: ``{type(response)}`` is not supported.")
        return responses_list

    def __reset_output_value(self, output: Iterable[DesignVariable]) -> None:
        """Set value of given output variables to `None`.

        Parameters
        ----------
        output: Iterable[DesignVariable]
            Iterable of either constraints, limit_states, objectives, responses or variables.
        """
        if not output:
            return
        else:
            for item in output:
                item.value = None
