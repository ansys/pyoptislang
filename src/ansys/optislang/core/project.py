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

"""Contains abstract ``Project`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Tuple, Union

if TYPE_CHECKING:
    from ansys.optislang.core.io import RegisteredFile
    from ansys.optislang.core.nodes import RootSystem
    from ansys.optislang.core.placeholder_types import PlaceholderInfo, PlaceholderType, UserLevel
    from ansys.optislang.core.project_parametric import Design


class Project(ABC):
    """Base class for classes which operate with active project."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``Project`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def root_system(self) -> RootSystem:  # pragma: no cover
        """Instance of the ``RootSystem`` class.

        Returns
        -------
        RootSystem
            Loaded project's root system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @property
    @abstractmethod
    def uid(self) -> str:  # pragma: no cover
        """Unique ID of the optiSLang project.

        Returns
        -------
        str
            Unique ID of the loaded project.
        """
        pass

    @abstractmethod
    def evaluate_design(
        self,
        design: Design,
    ) -> Design:  # pragma: no cover
        """Evaluate a design.

        Parameters
        ----------
        design: Design
            Instance of a ``Design`` class with defined parameters.

        Returns
        -------
        Design
            Evaluated design.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_description(self) -> Optional[str]:  # pragma: no cover
        """Get the description of the optiSLang project.

        Returns
        -------
        Optional[str]
            Description of the optiSLang project. If no project is loaded in optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_location(self) -> Optional[Path]:  # pragma: no cover
        """Get the path to the optiSLang project file.

        Returns
        -------
        Optional[pathlib.Path]
            Path to the optiSLang project file. If no project is loaded in the optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_name(self) -> Optional[str]:  # pragma: no cover
        """Get the name of the optiSLang project.

        Returns
        -------
        str
            Name of the optiSLang project. If no project is loaded in the optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_reference_design(self) -> Design:  # pragma: no cover
        """Get a design with reference values of the parameters.

        Returns
        -------
        Design
            Instance of the ``Design`` class with defined parameters and reference values.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_reference_files_dir(self) -> Optional[Path]:  # pragma: no cover
        """Get the path to the optiSLang project's reference files directory.

        Returns
        -------
        Optional[pathlib.Path]
            Path to the optiSLang project's reference files directory. If no project is loaded
            in optiSLang, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_registered_files(self) -> Tuple[RegisteredFile, ...]:  # pragma: no cover
        """Get all registered files in the current project.

        Returns
        -------
        Tuple[RegisteredFile, ...]
            Tuple with registered files.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_result_files(self) -> Tuple[RegisteredFile, ...]:  # pragma: no cover
        """Get result files.

        Returns
        -------
        Tuple[RegisteredFile, ...]
            Tuple with result files

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_status(self) -> Optional[str]:  # pragma: no cover
        """Get the status of the optiSLang project.

        Returns
        -------
        str
            Status of the optiSLang project. If no project is loaded in optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def get_working_dir(self) -> Optional[Path]:  # pragma: no cover
        """Get the path to the optiSLang project's working directory.

        Returns
        -------
        Optional[pathlib.Path]
            Path to the optiSLang project's working directory. If no project is loaded
            in optiSLang, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def reset(self) -> None:  # pragma: no cover
        """Reset the project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
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
        """Read a Python script from a file, load it in a project context, and run it.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the Python script file with the content to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments to use in the Python script. The default is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        FileNotFoundError
            Raised when the specified Python script file does not exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
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
        """Load a Python script in a project context and run it.

        Parameters
        ----------
        script : str
            Python commands to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in the Python script. The default
            is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
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
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to start.
            Defaults to ``True``.
        wait_for_finished : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to finish.
            This implicitly interprets wait_for_started as True.
            Defaults to ``True``.

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
            the command execution. I.e. don't continue on next line of python script after command
            was successfully sent to optiSLang but wait for execution of command inside optiSLang.
            Defaults to ``True``.

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
    def get_placeholder_ids(self) -> List[str]:  # pragma: no cover
        """Get IDs of all placeholders in the project.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Returns
        -------
        List[str]
            List of placeholder IDs.

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
    def get_placeholder(self, placeholder_id: str) -> PlaceholderInfo:  # pragma: no cover
        """Get placeholder information.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder.

        Returns
        -------
        PlaceholderInfo
            Named tuple containing placeholder information with separate fields
            for placeholder_id, user_level, type, description, range, value, and expression.

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
    def create_placeholder(
        self,
        value: Optional[Any] = None,
        placeholder_id: Optional[str] = None,
        overwrite: bool = False,
        user_level: Optional[UserLevel] = None,
        description: Optional[str] = None,
        range_: Optional[str] = None,
        type_: Optional[PlaceholderType] = None,
        expression: Optional[str] = None,
    ) -> str:  # pragma: no cover
        """Create a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        value : Optional[Any], optional
            Value for the placeholder, by default ``None``.
            If neither value nor expression are specified, the placeholder will be created
            with a suitable default value.
            If specified, the value must be of a type compatible with the placeholder type.
        placeholder_id : Optional[str], optional
            Desired placeholder ID, by default ``None``.
            If not specified, a unique ID will be generated.
        overwrite : bool, optional
            Whether to overwrite existing placeholder, by default ``False``.
        user_level : Optional[UserLevel], optional
            User level for the placeholder, by default ``None``.
            If not specified, the default user level will be used.
        description : Optional[str], optional
            Description of the placeholder, by default ``None``.
        range_ : Optional[str], optional
            Range of the placeholder, by default ``None``.
        type_ : Optional[PlaceholderType], optional
            Type of the placeholder, by default ``None``.
            If not specified, the UNKNOWN type will be used.
        expression : Optional[str], optional
            Macro expression for the placeholder, by default ``None``.

        Returns
        -------
        str
            ID of the created placeholder.

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
    def remove_placeholder(self, placeholder_id: str) -> None:  # pragma: no cover
        """Remove a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder to remove.

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
    def rename_placeholder(
        self, placeholder_id: str, new_placeholder_id: str
    ) -> None:  # pragma: no cover
        """Rename a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            Current ID of the placeholder.
        new_placeholder_id : str
            New ID for the placeholder.

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
    def set_placeholder_value(self, placeholder_id: str, value: Any) -> None:  # pragma: no cover
        """Set the value of a placeholder.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder.
        value : Any
            New value for the placeholder.

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

    # FUTURES:
    # @abstractmethod
    # TODO: Add this after it's fixed on optiSLang server side.
    # stop_gently method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # def stop_gently(self, wait_for_finished: bool = True) -> None:
    #     """Stop project execution after the current design is finished.

    #     Parameters
    #     ----------
    #     wait_for_finished : bool, optional
    #         Determines whether this function call should wait on the optiSlang to finish
    #         the command execution. I.e. don't continue on next line of python script after command
    #         was successfully sent to optiSLang but wait for execution of command inside optiSLang.
    #         Defaults to ``True``.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
