"""Contains abstract optiSLang server class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple, Union


class OslVersion(NamedTuple):
    """optiSLang version.

    Attributes:
        major: int
            The major version number.
        minor: int
            The minor version number.
        maintenance: int
            The maintenance version number.
        revision: int
            The revision number.
    """

    major: int
    minor: int
    maintenance: int
    revision: int


class OslServer(ABC):
    """Base class for classes which provide access to optiSLang server."""

    @abstractmethod
    def __init__(self):
        """``OslServer`` class is an abstract base class and cannot be instantiated."""

    @property
    @abstractmethod
    def osl_version(
        self,
    ) -> OslVersion:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.
        """
        pass

    @property
    @abstractmethod
    def osl_version_string(self) -> str:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.
        """
        pass

    @property
    @abstractmethod
    def timeout(self) -> Optional[float]:  # pragma: no cover
        """Get the timeout value for executing commands.

        Returns
        -------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.
        """
        pass

    @timeout.setter
    @abstractmethod
    def timeout(self, timeout: Union[float, None] = 30) -> None:  # pragma: no cover
        """Set the timeout value for the executing commands.

        Parameters
        ----------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``30``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.

        Raises
        ------
        ValueError
            Raised when the timeout value is less than or equal to 0.
        TypeError
            Raised when the timeout is not a Union[float, None].
        """
        pass

    # @abstractmethod
    # def close(self) -> None:
    #     """Close the current project.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
    #     pass

    @abstractmethod
    def add_criterion(
        self, uid: str, criterion_type: str, expression: str, name: str, limit: Optional[str] = None
    ) -> None:  # pragma: no cover
        """Set the properties of existing criterion for the system.

        Parameters
        ----------
        uid : str
            Actor uid.
        criterion_type: str
            Type of the criterion.
        expression: str
            Expression to be evaluated.
        name: str
            Criterion name.
        limit: Optional[str], optional
            Limit expression to be evaluated.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def dispose(self) -> None:  # pragma: no cover
        """Terminate all local threads and unregister listeners.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def evaluate_design(self, evaluate_dict: Dict[str, float]) -> List[dict]:  # pragma: no cover
        """Evaluate requested design.

        Parameters
        ----------
        evaluate_dict: Dict[str, float]
            {'parName': value, ...}

        Returns
        -------
        List[dict]
            Output from optislang server.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_info(self, uid: str) -> Dict:  # pragma: no cover
        """Get info about actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        Dict
            Info about actor defined by uid.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_internal_variables(
        self, uid: str, include_reference_values: bool = True
    ) -> List[dict]:  # pragma: no cover
        """Get currently registered internal variables for a certain (integration) actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        include_reference_values: bool, optional
            Whether reference values are to be included.

        Returns
        -------
        List[dict]
            Actor's internal variables.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_states(self, uid: str) -> Dict:  # pragma: no cover
        """Get available actor states for a certain actor (only the IDs of the available states).

        These can be used in conjunction with "get_actor_status_info" to obtain actor status info
        for a specific state ID.

        Parameters
        ----------
        uid : str
            Actor uid.
        Returns
        -------
        Dict
            Actor state.
        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_status_info(self, uid: str, hid: str) -> Dict:  # pragma: no cover
        """Get status info of actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.
        hid : str
            State/Design hierarchical id.
        Returns
        -------
        Dict
            Actor status info.
        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_supports(self, uid: str, feature_name: str) -> bool:  # pragma: no cover
        """Get supported features of actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.
        feature_name : str
            Name of the feature.

        Returns
        -------
        bool
            Whether the given feature is supported.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_properties(self, uid: str) -> Dict:  # pragma: no cover
        """Get properties of actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        Dict
            Properties of actor defined by uid.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_registered_input_slots(
        self, uid: str, include_reference_values: bool = True
    ) -> List[dict]:  # pragma: no cover
        """Get currently registered input slots for a certain (integration) actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        include_reference_values: bool, optional
            Whether reference values are to be included.

        Returns
        -------
        List[dict]
            Actor's registered input slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_registered_output_slots(
        self, uid: str, include_reference_values: bool = True
    ) -> List[dict]:  # pragma: no cover
        """Get currently registered output slots for a certain (integration) actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        include_reference_values: bool, optional
            Whether reference values are to be included.

        Returns
        -------
        List[dict]
            Actor's registered output slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_registered_parameters(
        self, uid: str, include_reference_values: bool = True
    ) -> List[dict]:  # pragma: no cover
        """Get currently registered parameters for a certain (integration) actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        include_reference_values: bool, optional
            Whether reference values are to be included.

        Returns
        -------
        List[dict]
            Actor's registered parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_actor_registered_responses(
        self, uid: str, include_reference_values: bool = True
    ) -> List[dict]:  # pragma: no cover
        """Get currently registered responses for a certain (integration) actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        include_reference_values: bool, optional
            Whether reference values are to be included.

        Returns
        -------
        List[dict]
            Actor's registered responses.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_available_input_locations(self, uid: str) -> List[dict]:  # pragma: no cover
        """Get available input locations for a certain (integration) actor, if supported.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        List[dict]
            Actor's available input locations.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_available_nodes(self) -> Dict[str, List[str]]:  # pragma: no cover
        """Get available node types for current oSL server.

        Returns
        -------
        Dict[str, List[str]]
            Dictionary of available nodes types

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_available_output_locations(self, uid: str) -> List[dict]:  # pragma: no cover
        """Get available output locations for a certain (integration) actor, if supported.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        List[dict]
            Actor's available output locations.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_basic_project_info(self) -> Dict:  # pragma: no cover
        """Get basic project info, like name, location, global settings and status.

        Returns
        -------
        Dict
            Information data as dictionary.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_criteria(self, uid: str) -> Dict:  # pragma: no cover
        """Get information about all existing criterion from the system.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        Dict
            Criteria information.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_criterion(self, uid: str, name: str) -> Dict:  # pragma: no cover
        """Get existing criterion from the system.

        Parameters
        ----------
        uid : str
            Actor uid.
        name: str
            Criterion name.

        Returns
        -------
        Dict
            Criterion information.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_doe_size(
        self, uid: str, sampling_type: str, num_discrete_levels: int
    ) -> int:  # pragma: no cover
        """Get the DOE size for given sampling type and number of levels for a specific actor.

        Parameters
        ----------
        uid : str
            Actor uid.
        sampling_type: str
            Sampling type.
        num_discrete_levels: int
            Number of discrete levels.

        Returns
        -------
        int
            DOE size.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_full_project_status_info(self) -> Dict:  # pragma: no cover
        """Get full project status info.

        Returns
        -------
        Dict
            Full project status info.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_full_project_tree(self) -> Dict:  # pragma: no cover
        """Get full project tree.

        Returns
        -------
        Dict
            Dictionary of full project tree without properties.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_full_project_tree_with_properties(self) -> Dict:  # pragma: no cover
        """Get full project tree with properties..

        Returns
        -------
        Dict
            Dictionary of full project tree with properties.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_hpc_licensing_forwarded_environment(self, uid: str) -> Dict:  # pragma: no cover
        """Get hpc licensing forwarded environment for certain actor.

        Parameters
        ----------
        uid : str
            Actor uid.

        Returns
        -------
        Dict
            Dictionary with hpc licensing forwarded environment for certain actor.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_input_slot_value(self, uid: str, hid: str, slot_name: str) -> Dict:  # pragma: no cover
        """Get input slot value of actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.
        hid: str
            State/Design hierarchical id.
        slot_name: str
            Slot name.

        Returns
        -------
        Dict
            Input slot value of the actor.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_output_slot_value(self, uid: str, hid: str, slot_name: str) -> Dict:  # pragma: no cover
        """Get output slot value of actor defined by uid.

        Parameters
        ----------
        uid : str
            Actor uid.
        hid: str
            State/Design hierarchical id.
        slot_name: str
            Slot name.

        Returns
        -------
        Dict
            Output slot value of the actor.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_uid(self) -> str:  # pragma: no cover
        """Get project uid.

        Returns
        -------
        str
            Project uid. If no project is loaded in the optiSLang, returns `None`.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_description(self) -> str:  # pragma: no cover
        """Get description of optiSLang project.

        Returns
        -------
        str
            optiSLang project description. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_location(self) -> Path:  # pragma: no cover
        """Get path to the optiSLang project file.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project file. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_name(self) -> str:  # pragma: no cover
        """Get name of the optiSLang project.

        Returns
        -------
        str
            Name of the optiSLang project. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_status(self) -> str:  # pragma: no cover
        """Get status of the optiSLang project.

        Returns
        -------
        str
            optiSLang project status. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_tree_systems(self) -> Dict:  # pragma: no cover
        """Get project tree systems without properties.

        Returns
        -------
        Dict
            Dictionary of project tree systems without properties.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_project_tree_systems_with_properties(self) -> Dict:  # pragma: no cover
        """Get project tree systems with properties.

        Returns
        -------
        Dict
            Dictionary of project tree systems with properties.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_server_info(self) -> Dict:  # pragma: no cover
        """Get information about the application, the server configuration and the open projects.

        Returns
        -------
        Dict
            Information data as dictionary.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_server_is_alive(self) -> bool:  # pragma: no cover
        """Get info whether the server is alive.

        Returns
        -------
        bool
            Whether the server is alive.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_systems_status_info(self) -> Dict:  # pragma: no cover
        """Get project status info, including systems only.

        Returns
        -------
        Dict
            Project status info including systems only.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_working_dir(self) -> Path:  # pragma: no cover
        """Get path to the optiSLang project working directory.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project working directory. If no project is loaded
            in the optiSLang, returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def new(self) -> None:  # pragma: no cover
        """Create a new project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:  # pragma: no cover
        """Open a new project.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the optiSLang project file to open.
        force : bool, optional
            Whether to force opening of project even if (non-critical) errors occur.
            Non-critical errors include:
            - Timestamp of (auto) save point newer than project timestamp
            - Project (file) incomplete
        restore : bool, optional
            Whether to restore project from last (auto) save point (if present).
        reset : bool, optional
            Whether to reset project after load.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def remove_criteria(self, uid: str) -> None:  # pragma: no cover
        """Remove all criteria from the system.

        Parameters
        ----------
        uid : str
            Actor uid.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def remove_criterion(self, uid: str, name: str) -> None:  # pragma: no cover
        """Remove existing criterion from the system.

        Parameters
        ----------
        uid : str
            Actor uid.
        name: str
            Name of the criterion.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def reset(self):  # pragma: no cover
        """Reset complete project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def run_python_script(
        self,
        script: str,
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:  # pragma: no cover
        """Load a Python script in a project context and execute it.

        Parameters
        ----------
        script : str
            Python commands to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from executed Python script.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def run_python_file(
        self,
        file_path: Union[str, Path],
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:  # pragma: no cover
        """Read python script from the file, load it in a project context and execute it.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the Python script file which content is supposed to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from executed Python script.

        Raises
        ------
        FileNotFoundError
            Raised when the specified Python script file does not exist.
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def save(self) -> None:  # pragma: no cover
        """Save the changed data and settings of the current project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:  # pragma: no cover
        """Save and open the current project at a new location.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path where to save the project file.
        force : bool, optional
            Whether to force opening of project even if (non-critical) errors occur.
            Non-critical errors include:
            - Timestamp of (auto) save point newer than project timestamp
            - Project (file) incomplete
        restore : bool, optional
            Whether to restore project from last (auto) save point (if present).
        reset : bool, optional
            Whether to reset project after load.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def save_copy(self, file_path: Union[str, Path]) -> None:  # pragma: no cover
        """Save the current project as a copy to a location.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path where to save the project copy.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def set_criterion_property(
        self,
        uid: str,
        criterion_name: str,
        name: str,
        value: Any,
    ) -> None:  # pragma: no cover
        """Set the properties of existing criterion for the system.

        Parameters
        ----------
        uid : str
            Actor uid.
        criterion_name: str
            Name of the criterion.
        name: str
            Property name.
        value: Any
            Property value.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def shutdown(self, force: bool = False) -> None:  # pragma: no cover
        """Shutdown the optiSLang server.

        Stop listening for incoming connections, discard pending requests, and shut down
        the server. Batch mode exclusive: Continue project run until execution finished.
        Terminate optiSLang.

        Parameters
        ----------
        force : bool, optional
            Determines whether to force shutdown the local optiSLang server. Has no effect when
            the connection is established to the remote optiSLang server. In all cases, it is tried
            to shutdown the optiSLang server process in a proper way. However, if the force
            parameter is ``True``, after a while, the process is forced to terminate and no
            exception is raised. Defaults to ``False``.

        Raises
        ------
        OslCommunicationError
            Raised when the parameter force is ``False`` and an error occurs while communicating
            with server.
        OslCommandError
            Raised when the parameter force is ``False`` and the command or query fails.
        TimeoutError
            Raised when the parameter force is ``False`` and the timeout float value expires.
        """
        pass

    @abstractmethod
    def start(
        self, wait_for_started: bool = True, wait_for_finished: bool = True
    ) -> None:  # pragma: no cover
        """Start project execution.

        Parameters
        ----------
        wait_for_started : bool, optional
            Determines whether this function call should wait on the optiSlang to start
            the command execution. Defaults to ``True``.
        wait_for_finished : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def stop(self, wait_for_finished: bool = True) -> None:  # pragma: no cover
        """Stop project execution.

        Parameters
        ----------
        wait_for_finished : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_host(self) -> Union[str, None]:  # pragma: no cover
        """Get optiSLang server address or domain name.

        Get a string representation of an IPv4/v6 address or domain name
        of the running optiSLang server.

        Returns
        -------
        timeout: Union[int, None]
            The IPv4/v6 address or domain name of the running optiSLang server, if applicable.
            Defaults to ``None``.
        """
        pass

    @abstractmethod
    def get_port(self) -> Union[int, None]:  # pragma: no cover
        """Get the port the osl server is listening on.

        Returns
        -------
        timeout: Union[int, None]
            The port the osl server is listening on, if applicable.
            Defaults to ``None``.
        """
        pass

    @abstractmethod
    def send_command(self, command: str) -> Dict:  # pragma: no cover
        """Send command or query to the optiSLang server.

        Parameters
        ----------
        command : str
            Command or query to be executed on optiSLang server.

        Returns
        -------
        Dict
            Response from the server.

        Raises
        ------
        RuntimeError
            Raised when the optiSLang server is not started.
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout expires.
        """
        pass

    # to be fixed in 2023R2:
    # close method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # @abstractmethod
    # def close(self) -> None:  # pragma: no cover
    #     """Close the current project.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
    #     pass

    # stop_gently method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # @abstractmethod
    # def stop_gently(self, wait_for_finished: bool = True) -> None:  # pragma: no cover
    #     """Stop project execution after the current design is finished.

    #     Parameters
    #     ----------
    #     wait_for_finished : bool, optional
    #         Determines whether this function call should wait on the optiSlang to finish
    #         the project execution. Defaults to ``True``.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
    #     pass
