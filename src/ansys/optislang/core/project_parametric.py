# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Contains ``Parameter``, ``Criterion``, ``Response``, it's child classes and enumerations."""
from __future__ import annotations

import copy
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union
import uuid

from ansys.optislang.core.utils import enum_from_str


# region ENUMERATIONS:
class CriterionType(Enum):
    """Available criteria types."""

    CONSTRAINT = 0
    LIMIT_STATE = 1
    OBJECTIVE = 2
    VARIABLE = 3

    @staticmethod
    def from_str(string: str) -> CriterionType:
        """Convert string to CriterionType.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        CriterionType
            Instance of the ``CriterionType`` class.

        Raises
        ------
        TypeError
            Raised when the type of the ``string`` is invalid.
        ValueError
            Raised when the value for the ``string`` is invalid.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class ComparisonType(Enum):
    """Provides criterion comparison types."""

    IGNORE = 0
    MIN = 1
    MAX = 2
    LESSEQUAL = 3
    EQUAL = 4
    GREATEREQUAL = 5
    LESSLIMITSTATE = 6
    GREATERLIMITSTATE = 7

    @staticmethod
    def from_str(string: str) -> ComparisonType:
        """Convert string to ComparisonType.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        ComparisonType
            Instance of the ``ComparisonType`` class.

        Raises
        ------
        TypeError
            Raised when the type of the ``string`` is invalid.
        ValueError
            Raised when the value for the ``string`` is invalid.
        """
        return enum_from_str(string=string, enum_class=__class__)


class CriterionValueType(Enum):
    """Available types of criterion values."""

    UNINITIALIZED = 0
    BOOL = 1
    SCALAR = 2
    VECTOR = 3
    MATRIX = 4
    SIGNAL = 5
    XYDATA = 6

    @staticmethod
    def from_str(string: str) -> CriterionValueType:
        """Convert string to CriterionValueType.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        CriterionValueType
            Instance of the ``CriterionValueType`` class.

        Raises
        ------
        TypeError
            Raised when the type of the ``string`` is invalid.
        ValueError
            Raised when the value for the ``string`` is invalid.
        """
        return enum_from_str(string=string, enum_class=__class__)


class DesignStatus(Enum):
    """Provides the design states."""

    IDLE = 0
    PENDING = 1
    SUCCEEDED = 2
    NOT_SUCCEEDED = 3
    FAILED = 4

    @staticmethod
    def from_str(string: str) -> DesignStatus:
        """Convert a string to an instance of the ``DesignStatus`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        DesignStatus
            Instance of the ``DesignStatus`` class.

        Raises
        ------
        TypeError
            Raised when the type of the ``string`` is invalid.
        ValueError
            Raised when the value for the ``string`` is invalid.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class DistributionType(Enum):
    """Available distribution types."""

    EXTERNALCOHERENCE = 0
    UNTYPED = 1
    EXTERNAL = 2
    UNIFORM = 3
    NORMAL = 4
    TRUNCATEDNORMAL = 5
    LOGNORMAL = 6
    EXPONENTIAL = 7
    RAYLEIGH = 8
    SMALL_I = 9
    LARGE_I = 10
    SMALL_II = 11
    LARGE_II = 12
    SMALL_III = 13
    LARGE_III = 14
    TRIANGULAR = 15
    BETA = 16
    CHI_SQUARE = 17
    ERLANG = 18
    FISHER_F = 19
    GAMMA = 20
    PARETO = 21
    WEIBULL = 22
    EXTREME_VALUE = 23
    STUDENTS_F = 24
    INVERSE_NORMAL = 25
    LOG_GAMMA = 26
    LOG_NORMAL = 27
    LORENTZ = 28
    FISHER_TIPPETT = 29
    GUMBEL = 30
    FISHER_Z = 31
    LAPLACE = 32
    LEVY = 33
    LOGISTIC = 34
    ROSSI = 35
    FRECHET = 36
    MAX_TYPE = 37
    POLYMAP = 38
    KERNEL = 39
    BERNOULLI = 40
    LOG_UNIFORM = 41
    DISCRETE = 42
    MULTIUNIFORM = 43
    LAMBDA = 44
    POISSON = 45

    @staticmethod
    def from_str(string: str) -> DistributionType:
        """Convert string to DistributionType.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        DistributionType
            Instance of the ``DistributionType`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class ParameterResolution(Enum):
    """Available parameter resolution kinds."""

    # optimization (deterministic)
    CONTINUOUS = 0
    ORDINALDISCRETE_VALUE = 1
    ORDINALDISCRETE_INDEX = 2
    NOMINALDISCRETE = 3
    # stochastic
    DETERMINISTIC = 4
    MARGINALDISTRIBUTION = 5
    EMPIRICAL_DISCRETE = 6
    EMPIRICAL_CONTINUOUS = 7

    @staticmethod
    def from_str(string: str) -> ParameterResolution:
        """Convert string to ``ParameterResolution``.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        ParameterResolution
            Instance of the ``ParameterResolution`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class ParameterType(Enum):
    """Provides parameter types."""

    DETERMINISTIC = 0
    STOCHASTIC = 1
    MIXED = 2
    DEPENDENT = 3

    @staticmethod
    def from_str(string: str) -> ParameterType:
        """Convert a string to an instance of the ``ParameterType`` class.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        ParameterType
            Instance of the ``ParameterType`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=__class__)


class ParameterValueType(Enum):
    """Available parameter value types."""

    UNINITIALIZED = 0
    BOOL = 1
    REAL = 2
    INTEGER = 3
    STRING = 4
    VARIANT = 5

    @staticmethod
    def from_str(string: str) -> ParameterValueType:
        """Convert string to ParameterValueType.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        ParameterValueType
            Instance of the ``ParameterValueType`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=__class__)


class ResponseValueType(Enum):
    """Available types of response values."""

    UNINITIALIZED = 0
    BOOL = 1
    SCALAR = 2
    VECTOR = 3
    SIGNAL = 4
    XYDATA = 5

    @staticmethod
    def from_str(string: str) -> CriterionValueType:
        """Convert string to ResponseValueType.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        ResponseValueType
            Instance of the ``ResponseValueType`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=__class__)


# endregion

# region CLASSES:


# region Criteria
class Criterion:
    """Stores criterion data."""

    def __init__(
        self,
        name: str = "",
        type_: Union[CriterionType, str] = CriterionType.VARIABLE,
        expression: str = "0",
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        expression_value_type: Optional[CriterionValueType] = None,
        criterion: Union[ComparisonType, str] = ComparisonType.IGNORE,
        value: Optional[
            Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict]
        ] = None,
        value_type: Optional[CriterionValueType] = None,
    ) -> None:
        """Create a new instance of ``Criterion``.

        Parameters
        ----------
        name: str, optional
            Criterion name, by default ``""``.
        type_: Union[CriterionKind, str], optional
            Type of criterion, e. g. 'objective', by default ``CriterionType.VARIABLE``.
        expression: str, optional
            Criterion expression, by default ``"0"``.
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Expression value, by default ``None``.
        expression_value_type: Optional[CriterionValueType], optional
            Expression value type, by default ``None``.
        criterion: Union[CriterionType, str], optional
            Type of comparison symbol, e. g. 'min', by default ``ComparisonType.IGNORE``.
        value: Optional[
            Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict]
        ], optional
            Value of the criterion, by default ``None``.
        value_type: Optional[CriterionValueType], optional
            Type of the criterion value, by default ``None``.
        """
        self.name = name
        self.expression = expression
        self.criterion = criterion

        if isinstance(type_, str):
            type_ = CriterionType.from_str(type_)
        if isinstance(type_, CriterionType):
            self.__type = type_
        else:
            raise TypeError(
                "Type Union[CriterionType, str] was expected, but type: "
                f"``{type(type_)}`` was given."
            )

        if expression_value and isinstance(expression_value_type, CriterionValueType):
            self.expression_value = (expression_value_type, expression_value)
        else:
            self.expression_value = expression_value
        if value and isinstance(value_type, CriterionValueType):
            self.value = (value_type, value)
        else:
            self.value = value

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``Criterion`` class.

        Parameters
        ----------
        other: Criterion
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.type == other.type
            and self.expression == other.expression
            and self.expression_value == other.expression_value
            and self.expression_value_type == other.expression_value_type
            and self.criterion == other.criterion
            and self.value == other.value
            and self.value_type == other.value_type
        )

    def __deepcopy__(self, memo) -> Criterion:
        """Return deep copy of given criterion."""
        return Criterion(
            name=self.name,
            type_=self.type,
            expression=self.expression,
            expression_value=copy.deepcopy(self.expression_value),
            expression_value_type=self.expression_value_type,
            criterion=self.criterion,
            value=copy.deepcopy(self.value),
            value_type=self.value_type,
        )

    @property
    def criterion(self) -> ComparisonType:
        """Type of the criterion."""
        return self.__criterion

    @criterion.setter
    def criterion(self, type_: Union[ComparisonType, str]) -> None:
        """Set type of the criterion."""
        if isinstance(type_, str):
            type_ = ComparisonType.from_str(type_)
        if isinstance(type_, ComparisonType):
            self.__criterion = type_
            self.value = None
        else:
            raise TypeError(
                "Type Union[CriterionType, str] was expected, but type: "
                f"``{type(type_)}`` was given."
            )

    @property
    def expression(self) -> str:
        """Expression for value."""
        return self.__expression

    @expression.setter
    def expression(self, expression: str) -> None:
        """Set expression.

        Parameters
        ----------
        expression: str
            Expression to be evaluated.

        Raises
        ------
        TypeError
            Raised when type of expression is invalid.
        """
        if not isinstance(expression, str):
            raise TypeError(f"Type `str` was expected, but type: `{type(expression)}` was given.")
        self.__expression = expression
        self.expression_value = None
        self.value = None

    @property
    def expression_value(self) -> Union[bool, float, complex, list, dict, None]:
        """Return expression value."""
        return self.__expression_value

    @expression_value.setter
    def expression_value(
        self,
        expression_value: Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict],
    ) -> None:
        """Set limit value."""
        if isinstance(expression_value, tuple) and isinstance(
            expression_value[0], CriterionValueType
        ):
            self.__expression_value = self._parse_str_to_value(
                expression_value[0], expression_value[1]
            )
            self.__expression_value_type = expression_value[0]
        else:
            self.__expression_value = expression_value
            self.__expression_value_type = self._get_value_type(self.expression_value)

    @property
    def expression_value_type(self) -> CriterionValueType:
        """Type of the expression value."""
        return self.__expression_value_type

    @property
    def name(self) -> str:
        """Name of the criterion."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the criterion.

        Parameters
        ----------
        name: str
            Name of the criterion.

        Raises
        ------
        TypeError
            Raised when the type of the name is invalid.
        """
        if not isinstance(name, str):
            raise TypeError(
                f"Type of ``name`` must be ``str`` but type: ``{type(name)}`` was given."
            )
        self.__name = name

    @property
    def type(self) -> CriterionType:
        """Type of the criterion."""
        return self.__type

    @property
    def value(self) -> Union[bool, float, complex, list, dict, None]:
        """Return criterion value."""
        return self.__value

    @value.setter
    def value(
        self, value: Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict, None]
    ) -> None:
        """Set criterion value."""
        if isinstance(value, tuple) and isinstance(value[0], CriterionValueType):
            self.__value = self._parse_str_to_value(value[0], value[1])
            self.__value_type = value[0]
        else:
            self.__value = value
            self.__value_type = self._get_value_type(value)

    @property
    def value_type(self) -> CriterionValueType:
        """Return type of the criterion value."""
        return self.__value_type

    @staticmethod
    def from_dict(criterion_dict: dict) -> Criterion:
        """Create an instance of the ``Criterion`` class from actor properties.

        Parameters
        ----------
        criterion_dict : dict
            Output from optiSLang server.

        Returns
        -------
        Criterion
            Instance of the ``Criterion`` class.

        Raises
        ------
        TypeError
            Raised when undefined type of criterion is given.
        """
        criterion_properties = __class__._extract_criterion_properties_from_dict(criterion_dict)
        if criterion_properties["criterion"] == ComparisonType.IGNORE:
            return VariableCriterion(
                name=criterion_properties["name"],
                expression=criterion_properties["limit_expression"],
                expression_value=criterion_properties["limit_expression_value"],
                expression_value_type=criterion_properties["limit_expression_value_type"],
                value=criterion_properties["value"],
                value_type=criterion_properties["value_type"],
            )
        elif criterion_properties["criterion"] in [ComparisonType.MIN, ComparisonType.MAX]:
            return ObjectiveCriterion(
                name=criterion_properties["name"],
                expression=criterion_properties["limit_expression"],
                expression_value=criterion_properties["limit_expression_value"],
                expression_value_type=criterion_properties["limit_expression_value_type"],
                criterion=criterion_properties["criterion"],
                value=criterion_properties["value"],
                value_type=criterion_properties["value_type"],
            )
        elif criterion_properties["criterion"] in [
            ComparisonType.LESSEQUAL,
            ComparisonType.EQUAL,
            ComparisonType.GREATEREQUAL,
        ]:
            return ConstraintCriterion(
                name=criterion_properties["name"],
                expression=criterion_properties["expression"],
                expression_value=criterion_properties["expression_value"],
                expression_value_type=criterion_properties["expression_value_type"],
                criterion=criterion_properties["criterion"],
                limit_expression=criterion_properties["limit_expression"],
                limit_expression_value=criterion_properties["limit_expression_value"],
                limit_expression_value_type=criterion_properties["limit_expression_value_type"],
                value=criterion_properties["value"],
                value_type=criterion_properties["value_type"],
            )
        elif criterion_properties["criterion"] in [
            ComparisonType.LESSLIMITSTATE,
            ComparisonType.GREATERLIMITSTATE,
        ]:
            return LimitStateCriterion(
                name=criterion_properties["name"],
                expression=criterion_properties["expression"],
                expression_value=criterion_properties["expression_value"],
                expression_value_type=criterion_properties["expression_value_type"],
                criterion=criterion_properties["criterion"],
                limit_expression=criterion_properties["limit_expression"],
                limit_expression_value=criterion_properties["limit_expression_value"],
                limit_expression_value_type=criterion_properties["limit_expression_value_type"],
                value=criterion_properties["value"],
                value_type=criterion_properties["value_type"],
            )

    @staticmethod
    def _extract_criterion_properties_from_dict(criterion_dict: dict) -> Dict[str, Any]:
        """Get type of criterion from optiSLang output.

        Parameters
        ----------
        criterion_dict : dict
            Output from `get_actor_properties` query.

        Returns
        -------
        Dict[str, Any]
           name: str,
           expression: str,
           expression_value: Any,
           expression_value_type: CriterionValueType,
           criterion: ComparisonType,
           limit_expression: Optional[str],
           limit_expression_value: Optional[Any],
           limit_expression_value_type: Optional[CriterionValueType],
           value: Any,
           value_type: CriterionValueType
        """
        if not ("First" in criterion_dict.keys() and "Second" in criterion_dict.keys()):
            raise TypeError("Unsupported format of criterion dictionary.")
        name = criterion_dict["First"]
        criterion_dict = criterion_dict["Second"]
        criterion = ComparisonType.from_str(criterion_dict["type"]["value"])
        expression = criterion_dict["lhs"]
        expression_value_type = (
            CriterionValueType.from_str(
                criterion_dict["lhs_value"].get("kind", {}).get("value", "UNINITIALIZED")
            )
            if criterion_dict.get("lhs_value")
            else None
        )
        if expression_value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            expression_value = (
                criterion_dict["lhs_value"]["matrix"],
                criterion_dict["lhs_value"]["vector"],
            )
        elif expression_value_type in [CriterionValueType.UNINITIALIZED, None]:
            expression_value = None
        else:
            expression_value = criterion_dict["lhs_value"][expression_value_type.name.lower()]

        limit_expression = criterion_dict.get("rhs")  # optional
        limit_expression_value_type = (
            CriterionValueType.from_str(
                criterion_dict["rhs_value"].get("kind", {}).get("value", "UNINITIALIZED")
            )
            if criterion_dict.get("rhs_value")
            else None
        )
        if limit_expression_value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            limit_expression_value = (
                criterion_dict["rhs_value"]["matrix"],
                criterion_dict["rhs_value"]["vector"],
            )
        elif limit_expression_value_type in [CriterionValueType.UNINITIALIZED, None]:
            limit_expression_value = None
        else:
            limit_expression_value = criterion_dict["rhs_value"][
                limit_expression_value_type.name.lower()
            ]

        value_type = value_type = (
            CriterionValueType.from_str(
                criterion_dict["value"].get("kind", {}).get("value", "UNINITIALIZED")
            )
            if criterion_dict.get("value")
            else None
        )
        if value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            value = (
                criterion_dict["value"]["matrix"],
                criterion_dict["value"]["vector"],
            )
        elif value_type in [CriterionValueType.UNINITIALIZED, None]:
            value = None
        else:
            value = criterion_dict["value"][value_type.name.lower()]
        return {
            "name": name,
            "expression": expression,
            "expression_value": expression_value,
            "expression_value_type": expression_value_type,
            "criterion": criterion,
            "limit_expression": limit_expression,
            "limit_expression_value": limit_expression_value,
            "limit_expression_value_type": limit_expression_value_type,
            "value": value,
            "value_type": value_type,
        }

    @staticmethod
    def _get_value_type(value: Any) -> CriterionValueType:
        """Return type of the value.

        Parameters
        ----------
        value: Any
            Criterion value.
        """
        if isinstance(value, bool):
            return CriterionValueType.BOOL
        elif isinstance(value, (float, int, complex)):
            return CriterionValueType.SCALAR
        elif value == None:
            return CriterionValueType.UNINITIALIZED
        elif isinstance(value, list):
            if isinstance(value[0], list):
                return CriterionValueType.MATRIX
            else:
                return CriterionValueType.VECTOR
        elif isinstance(value, dict):
            if value.get("channels") is not None:
                return CriterionValueType.SIGNAL
            else:
                return CriterionValueType.XYDATA
        else:
            raise TypeError(f"Unsupported type of value: ``{value}``.")

    @staticmethod
    def _parse_str_to_matrix(string: str):
        """Parse string to matrix.

        Parameters
        ----------
        string: str
            Expression describing matrix.
        """
        # split by square bracket end
        splitted_str = string.split("]")
        size_str = splitted_str[0] + "]"
        size = eval(size_str)
        if size[0] == 1:
            splitted_str[1] = splitted_str[1][:-1] + "," + splitted_str[1][-1:]
        if size[1] == 1 and size[0] > 1:
            splitted_str[1] = splitted_str[1][:-2] + "," + splitted_str[1][-2:]
        else:
            splitted_str[1] = splitted_str[1][:-3] + "," + splitted_str[1][-3:]

        # evaluation of second part creates tuple
        eval_str = eval(splitted_str[1])
        matrix_list = []
        for row_index in range(size[0]):
            matrix_list.append([])
            for column_index in range(size[1]):
                if eval_str[row_index][column_index][1] == 0:
                    matrix_list[row_index].append(eval_str[row_index][column_index][0])
                else:
                    matrix_list[row_index].append(
                        complex(
                            eval_str[row_index][column_index][0],
                            eval_str[row_index][column_index][1],
                        )
                    )

        return matrix_list

    @staticmethod
    def _parse_str_to_value(value_type: CriterionValueType, value: dict):
        """Parse string representation of value to value.

        Parameters
        ----------
        value_type: CriterionValueType
            Type of value.
        value: dict
            Dictionary with stored data.
        """
        if value_type == CriterionValueType.UNINITIALIZED:
            return None
        elif value_type == CriterionValueType.BOOL:
            return value
        elif value_type == CriterionValueType.SCALAR:
            if isinstance(value, dict):
                real = value.get("real")
                imag = value.get("imag")
                if imag == 0:
                    return real
                else:
                    return complex(real=real, imag=imag)
            elif isinstance(value, (int, float)):
                return value
        elif value_type == CriterionValueType.VECTOR:
            return Criterion._parse_str_to_vector(value)
        elif value_type == CriterionValueType.MATRIX:
            return Criterion._parse_str_to_matrix(value)
        elif value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            return (
                Criterion._parse_str_to_matrix(value[0]),
                Criterion._parse_str_to_vector(value[1]),
            )
        else:
            raise TypeError(f"Invalid kind of criterion: ``{type}``.")

    @staticmethod
    def _parse_str_to_vector(string: str):
        """Parse string to vector.

        Parameters
        ----------
        string: str
            Expression describing matrix.
        """
        # split by square bracket end
        splitted_str = string.split("]")
        size_str = splitted_str[0] + "]"
        size = eval(size_str)
        if size[0] == 1:
            splitted_str[1][-2:-2] = ","
        # evaluatiaon of second part creates tuple
        eval_str = eval(splitted_str[1])
        vector_list = []
        for row_index in range(size[0]):
            if eval_str[row_index][1] == 0:
                vector_list.append(eval_str[row_index][0])
            else:
                vector_list.append(
                    complex(
                        eval_str[row_index][0],
                        eval_str[row_index][1],
                    )
                )
        return vector_list

    @staticmethod
    def _lhs_rhs_value_to_dict(
        value: Union[bool, float, complex, list, dict, None], value_type: CriterionValueType
    ) -> dict:
        """Convert given value to `lhs_value` or `rhs_value` dictionary."""
        if value_type == CriterionValueType.UNINITIALIZED:
            return {"kind": {"value": None}}

        value_dict = {"kind": {"value": value_type.name.lower()}}
        if value_type == CriterionValueType.SCALAR:
            if isinstance(value, complex):
                value_dict.update(
                    {value_type.name.lower(): {"imag": value.imag, "real": value.real}}
                )
            else:
                value_dict.update({value_type.name.lower(): {"real": value}})
        elif value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            value_dict.update({"matrix": value[0], "vector": value[1]})
        elif value_type in [
            CriterionValueType.BOOL,
            CriterionValueType.MATRIX,
            CriterionValueType.VECTOR,
        ]:
            value_dict.update({value_type.name.lower(): value})
        return value_dict

    @staticmethod
    def _value_to_dict(
        value: Union[bool, float, complex, list, dict, None], value_type: CriterionValueType
    ) -> dict:
        """Convert given value to dictionary."""
        if value_type == CriterionValueType.UNINITIALIZED:
            return {"kind": {"value": None}}

        value_dict = {"kind": {"value": value_type.name.lower()}}
        if value_type == CriterionValueType.SCALAR:
            if isinstance(value, complex):
                value_dict["kind"].update(
                    {value_type.name.lower(): {"imag": value.imag, "real": value.real}}
                )
            else:
                value_dict["kind"].update({value_type.name.lower(): {"real": value}})
        elif value_type in [CriterionValueType.SIGNAL, CriterionValueType.XYDATA]:
            value_dict["kind"].update({"matrix": value[0], "vector": value[1]})
        elif value_type in [
            CriterionValueType.BOOL,
            CriterionValueType.MATRIX,
            CriterionValueType.VECTOR,
        ]:
            value_dict["kind"].update({value_type.name.lower(): value})
        return value_dict


class ConstraintCriterion(Criterion):
    """Stores constraint criterion data."""

    def __init__(
        self,
        name: str = "",
        expression: str = "0",
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        expression_value_type: Optional[CriterionValueType] = None,
        criterion: Union[ComparisonType, str] = ComparisonType.LESSEQUAL,
        limit_expression: str = "0",
        limit_expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        limit_expression_value_type: Optional[CriterionValueType] = None,
        value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        value_type: Optional[CriterionValueType] = None,
    ) -> None:
        """Initialize a new instance of ``ConstraintCriterion`` class.

        Parameters
        ----------
        name: str, optional
            Criterion name. By default ``""``.
        expression: str, optional
            Criterion expression. By default ``"0"``.
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Expression value. By default ``None``.
        expression_value_type: Optional[CriterionValueType], optional
            Expression value type. By default ``ComparisonType.LESSEQUAL``
        criterion: Union[CriterionType, str], optional
            Comparison symbol type, e. g. 'lessequal'.
        limit_expression: str, optional
            Limit expression. By default ``"0"``.
        limit_expression_value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Limit expression value. By default ``None``.
        limit_expression_value_type: Optional[CriterionValueType], optional
            Limit expression value type. By default ``None``.
        value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Criterion value. By default ``None``.
        value_type: Optional[CriterionValueType], optional
            Type of the criterion value. By default ``None``.
        """
        super().__init__(
            name=name,
            type_=CriterionType.CONSTRAINT,
            expression=expression,
            expression_value=expression_value,
            expression_value_type=expression_value_type,
            criterion=criterion,
            value=value,
            value_type=value_type,
        )
        if not isinstance(limit_expression, str):
            raise TypeError(
                f"Type `str` was expected, but type: `{type(limit_expression)}` was given."
            )
        self.__limit_expression = limit_expression

        if limit_expression_value and isinstance(limit_expression_value_type, CriterionValueType):
            self.limit_expression_value = (limit_expression_value_type, limit_expression_value)
        else:
            self.limit_expression_value = limit_expression_value

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``ConstraintCriterion`` class.

        Parameters
        ----------
        other: ConstraintCriterion
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.type == other.type
            and self.expression == other.expression
            and self.expression_value == other.expression_value
            and self.expression_value_type == other.expression_value_type
            and self.criterion == other.criterion
            and self.value == other.value
            and self.value_type == other.value_type
            and self.limit_expression == other.limit_expression
            and self.limit_expression_value == other.limit_expression_value
            and self.limit_expression_value_type == other.limit_expression_value_type
        )

    def __deepcopy__(self, memo) -> ConstraintCriterion:
        """Return deep copy of given constraint criterion."""
        return ConstraintCriterion(
            name=self.name,
            expression=self.expression,
            expression_value=copy.deepcopy(self.expression_value),
            expression_value_type=self.expression_value_type,
            criterion=self.criterion,
            limit_expression=self.limit_expression,
            limit_expression_value=copy.deepcopy(self.limit_expression_value),
            limit_expression_value_type=self.limit_expression_value_type,
            value=copy.deepcopy(self.value),
            value_type=self.value_type,
        )

    @property
    def limit_expression(self) -> str:
        """Expression for limit value."""
        return self.__limit_expression

    @limit_expression.setter
    def limit_expression(self, limit_expression: str) -> None:
        """Set limit expression.

        Parameters
        ----------
        limit_expression: str
            Expression for limit to be evaluated.

        Raises
        ------
        TypeError
            Raised when type of expression is invalid.
        """
        if not isinstance(limit_expression, str):
            raise TypeError(
                f"Type `str` was expected, but type: `{type(limit_expression)}` was given."
            )
        self.__limit_expression = limit_expression
        self.limit_expression_value = None
        self.value = None

    @property
    def limit_expression_value(self) -> Union[bool, float, complex, list, dict, None]:
        """Return limit value."""
        return self.__limit_expression_value

    @limit_expression_value.setter
    def limit_expression_value(
        self, limit_value: Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict]
    ) -> None:
        """Set limit value."""
        if isinstance(limit_value, tuple) and isinstance(limit_value[0], CriterionValueType):
            self.__limit_expression_value = self._parse_str_to_value(limit_value[0], limit_value[1])
            self.__limit_expression_value_type = limit_value[0]
        else:
            self.__limit_expression_value = limit_value
            self.__limit_expression_value_type = self._get_value_type(self.limit_expression_value)

    @property
    def limit_expression_value_type(self) -> CriterionValueType:
        """Return type of the limit value."""
        return self.__limit_expression_value_type

    def to_dict(self) -> dict:
        """Convert an instance of the ``ConstraintCriterion`` class to a dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.
        """
        return {
            "First": self.name,
            "Second": {
                "lhs": self.expression,
                "lhs_value": Criterion._lhs_rhs_value_to_dict(
                    value=self.expression_value, value_type=self.expression_value_type
                ),
                "need_eval": False,
                "rhs": self.limit_expression,
                "rhs_value": Criterion._lhs_rhs_value_to_dict(
                    value=self.limit_expression_value, value_type=self.limit_expression_value_type
                ),
                "type": {"value": self.criterion.name.lower()},
                "value": Criterion._value_to_dict(value=self.value, value_type=self.value_type),
            },
        }

    def __str__(self) -> str:
        """Return information about the criterion."""
        return (
            f"Name: {self.name}\n"
            f"Expression: {self.expression}\n"
            f"Expression value: {self.expression_value}\n"
            f"Expression value type: {self.expression_value_type}\n"
            f"Criterion: {self.criterion}\n"
            f"Limit expression: {self.limit_expression}\n"
            f"Limit expression value: {self.limit_expression_value}\n"
            f"Limit expression value type: {self.limit_expression_value_type}\n"
            f"Value: {self.value}\n"
            f"Value type: {self.value_type}\n"
        )


class LimitStateCriterion(Criterion):
    """Stores limit state criterion data."""

    def __init__(
        self,
        name: str = "",
        expression: str = "0",
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        expression_value_type: Optional[CriterionValueType] = None,
        criterion: Union[ComparisonType, str] = ComparisonType.LESSLIMITSTATE,
        limit_expression: str = "0",
        limit_expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        limit_expression_value_type: Optional[CriterionValueType] = None,
        value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        value_type: Optional[CriterionValueType] = None,
    ) -> None:
        """Initialize a new instance of ``LimitStateCriterion`` class.

        Parameters
        ----------
        name: str, optional
            Criterion name. By default ``""``.
        expression: str, optional
            Criterion expression. By default ``"0"``.
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict, None]], optional
            Expression value. Defaults to ``None``.
        expression_value_type: Optional[CriterionValueType], optional
            Expression value type. Defaults to ``None``.
        criterion: Union[CriterionType, str], optional
            Comparison symbol type, e. g. 'min'. By default ``ComparisonType.LESSLIMITSTATE``.
        limit_expression: str, optional
            Limit expression. By default ``"0"``.
        limit_expression_value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Limit expression value. Defaults to ``None``.
        limit_expression_value_type: Optional[Union[CriterionValueType, None]], optional
            Limit expression value type. Defaults to ``None``.
        value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Criterion value. By default ``None``.
        value_type: Optional[CriterionValueType], optional
            Type of the criterion value. By default ``None``.
        """
        super().__init__(
            name=name,
            type_=CriterionType.LIMIT_STATE,
            expression=expression,
            expression_value=expression_value,
            expression_value_type=expression_value_type,
            criterion=criterion,
            value=value,
            value_type=value_type,
        )
        if not isinstance(limit_expression, str):
            raise TypeError(
                f"Type `str` was expected, but type: `{type(limit_expression)}` was given."
            )
        self.__limit_expression = limit_expression

        if limit_expression_value and isinstance(limit_expression_value_type, CriterionValueType):
            self.limit_expression_value = (limit_expression_value_type, limit_expression_value)
        else:
            self.limit_expression_value = limit_expression_value

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``LimitStateCriterion`` class.

        Parameters
        ----------
        other: LimitStateCriterion
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.type == other.type
            and self.expression == other.expression
            and self.expression_value == other.expression_value
            and self.expression_value_type == other.expression_value_type
            and self.criterion == other.criterion
            and self.value == other.value
            and self.value_type == other.value_type
            and self.limit_expression == other.limit_expression
            and self.limit_expression_value == other.limit_expression_value
            and self.limit_expression_value_type == other.limit_expression_value_type
        )

    def __deepcopy__(self, memo) -> LimitStateCriterion:
        """Return deep copy of given limit state criterion."""
        return LimitStateCriterion(
            name=self.name,
            expression=self.expression,
            expression_value=copy.deepcopy(self.expression_value),
            expression_value_type=self.expression_value_type,
            criterion=self.criterion,
            limit_expression=self.limit_expression,
            limit_expression_value=copy.deepcopy(self.limit_expression_value),
            limit_expression_value_type=self.limit_expression_value_type,
            value=copy.deepcopy(self.value),
            value_type=self.value_type,
        )

    @property
    def limit_expression(self) -> str:
        """Expression for limit value."""
        return self.__limit_expression

    @limit_expression.setter
    def limit_expression(self, limit_expression: str) -> None:
        """Set limit expression.

        Parameters
        ----------
        limit_expression: str
            Expression for limit to be evaluated.

        Raises
        ------
        TypeError
            Raised when type of expression is invalid.
        """
        if not isinstance(limit_expression, str):
            raise TypeError(
                f"Type `str` was expected, but type: `{type(limit_expression)}` was given."
            )
        self.__limit_expression = limit_expression
        self.limit_expression_value = None
        self.value = None

    @property
    def limit_expression_value(self) -> Union[bool, float, complex, list, dict, None]:
        """Return limit value."""
        return self.__limit_expression_value

    @limit_expression_value.setter
    def limit_expression_value(
        self, limit_value: Union[Tuple[CriterionValueType, str], bool, float, complex, list, dict]
    ) -> None:
        """Set limit value."""
        if isinstance(limit_value, tuple) and isinstance(limit_value[0], CriterionValueType):
            self.__limit_expression_value = self._parse_str_to_value(limit_value[0], limit_value[1])
            self.__limit_expression_value_type = limit_value[0]
        else:
            self.__limit_expression_value = limit_value
            self.__limit_expression_value_type = self._get_value_type(self.limit_expression_value)

    @property
    def limit_expression_value_type(self) -> CriterionValueType:
        """Return type of the limit value."""
        return self.__limit_expression_value_type

    def to_dict(self) -> dict:
        """Convert an instance of the ``LimitStateCriterion`` class to a dictionary.

        Returns
        -------
        dict
            Dictionary input for the optiSLang server.
        """
        return {
            "First": self.name,
            "Second": {
                "lhs": self.expression,
                "lhs_value": Criterion._lhs_rhs_value_to_dict(
                    value=self.expression_value, value_type=self.expression_value_type
                ),
                "need_eval": False,
                "rhs": self.limit_expression,
                "rhs_value": Criterion._lhs_rhs_value_to_dict(
                    value=self.expression_value, value_type=self.expression_value_type
                ),
                "type": {
                    "value": self.criterion.name.lower(),
                },
                "value": Criterion._value_to_dict(value=self.value, value_type=self.value_type),
            },
        }

    def __str__(self) -> str:
        """Return information about the criterion."""
        return (
            f"Name: {self.name}\n"
            f"Expression: {self.expression}\n"
            f"Expression value: {self.expression_value}\n"
            f"Expression value type: {self.expression_value_type}\n"
            f"Criterion: {self.criterion}\n"
            f"Limit expression: {self.limit_expression}\n"
            f"Limit expression value: {self.limit_expression_value}\n"
            f"Limit expression value type: {self.limit_expression_value_type}\n"
            f"Value: {self.value}\n"
            f"Value type: {self.value_type}\n"
        )


class ObjectiveCriterion(Criterion):
    """Stores objective criterion data."""

    def __init__(
        self,
        name: str = "",
        expression: str = "0",
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        expression_value_type: Optional[CriterionValueType] = None,
        criterion: Union[ComparisonType, str] = ComparisonType.MIN,
        value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        value_type: Optional[CriterionValueType] = None,
    ) -> None:
        """Create a new instance of the ``ObjectiveCriterion`` class.

        Parameters
        ----------
        name: str, optional
            Criterion name. By default ``""``.
        expression: str, optional
            Criterion expression. By default ``"0"``.
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Expression value. By default ``None``.
        expression_value_type: Optional[CriterionValueType], optional
            Expression value type. By default ``None``.
        criterion: Union[CriterionType, str], optional
            Comparison symbol type, e. g. 'min'. By default ``ComparisonType.MIN``.
        value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Criterion value. By default ``None``.
        value_type: Optional[CriterionValueType], optional
            Type of the criterion value. By default ``None``.
        """
        super().__init__(
            name=name,
            type_=CriterionType.OBJECTIVE,
            expression=expression,
            expression_value=expression_value,
            expression_value_type=expression_value_type,
            criterion=criterion,
            value=value,
            value_type=value_type,
        )

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``ObjectiveCriterion`` class.

        Parameters
        ----------
        other: ObjectiveCriterion
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.type == other.type
            and self.expression == other.expression
            and self.expression_value == other.expression_value
            and self.expression_value_type == other.expression_value_type
            and self.criterion == other.criterion
            and self.value == other.value
            and self.value_type == other.value_type
        )

    def __deepcopy__(self, memo) -> ObjectiveCriterion:
        """Return deep copy of given objective criterion."""
        return ObjectiveCriterion(
            name=self.name,
            expression=self.expression,
            expression_value=copy.deepcopy(self.expression_value),
            expression_value_type=self.expression_value_type,
            criterion=self.criterion,
            value=copy.deepcopy(self.value),
            value_type=self.value_type,
        )

    def to_dict(self) -> dict:
        """Convert an instance of the ``ObjectiveCriterion`` class to a dictionary.

        Returns
        -------
        dict
            Dictionary input for the optiSLang server.
        """
        return {
            "First": self.name,
            "Second": {
                "lhs": "",
                "lhs_value": None,
                "need_eval": False,
                "rhs": self.expression,
                "rhs_value": Criterion._lhs_rhs_value_to_dict(
                    self.expression_value, self.expression_value_type
                ),
                "type": {"value": self.criterion.name.lower()},
                "value": Criterion._value_to_dict(self.value, self.value_type),
            },
        }

    def __str__(self) -> str:
        """Return information about the criterion."""
        return (
            f"Name: {self.name}\n"
            f"Expression: {self.expression}\n"
            f"Expression value: {self.expression_value}\n"
            f"Expression value type: {self.expression_value_type}\n"
            f"Criterion: {self.criterion}\n"
            f"Value: {self.value}\n"
            f"Value type: {self.value_type}\n"
        )


class VariableCriterion(Criterion):
    """Stores variable criterion data."""

    def __init__(
        self,
        name: str = "",
        expression: str = "0",
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        expression_value_type: Optional[CriterionValueType] = None,
        value: Optional[Union[tuple, bool, float, complex, list, dict]] = None,
        value_type: Optional[CriterionValueType] = None,
    ) -> None:
        """Create a new instance of ``VariableCriterion`` class.

        Parameters
        ----------
        name: str, optional
            Criterion name. By default ``""``.
        expression: str, optional
            Criterion expression. By default ``"0"``.
        expression_value: Optional[Union[tuple, bool, float, complex, list, dict, None]], optional
            Expression value. By default ``None``.
        expression_value_type: Optional[CriterionValueType], optional
            Expression value type. By default ``None``.
        value: Optional[Union[tuple, bool, float, complex, list, dict]], optional
            Criterion value. By default ``None``.
        value_type: Optional[CriterionValueType], optional
            Type of the criterion value. By default ``None``.
        """
        super().__init__(
            name=name,
            type_=CriterionType.VARIABLE,
            expression=expression,
            expression_value=expression_value,
            expression_value_type=expression_value_type,
            criterion=ComparisonType.IGNORE,
            value=value,
            value_type=value_type,
        )

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``VariableCriterion`` class.

        Parameters
        ----------
        other: VariableCriterion
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.type == other.type
            and self.expression == other.expression
            and self.expression_value == other.expression_value
            and self.expression_value_type == other.expression_value_type
            and self.criterion == other.criterion
            and self.value == other.value
            and self.value_type == other.value_type
        )

    def __deepcopy__(self, memo) -> VariableCriterion:
        """Return deep copy of given variable criterion."""
        return VariableCriterion(
            name=self.name,
            expression=self.expression,
            expression_value=copy.deepcopy(self.expression_value),
            expression_value_type=self.expression_value_type,
            value=copy.deepcopy(self.value),
            value_type=self.value_type,
        )

    def to_dict(self) -> dict:
        """Convert an instance of the ``VariableCriterion`` class to a dictionary.

        Returns
        -------
        dict
            Dictionary input for the optiSLang server.
        """
        return {
            "First": self.name,
            "Second": {
                "lhs": "",
                "lhs_value": None,
                "need_eval": False,
                "rhs": self.expression,
                "rhs_value": Criterion._lhs_rhs_value_to_dict(
                    self.expression_value, self.expression_value_type
                ),
                "type": {"value": self.criterion.name.lower()},
                "value": Criterion._value_to_dict(self.value, self.value_type),
            },
        }

    def __str__(self) -> str:
        """Return information about the criterion."""
        return (
            f"Name: {self.name}\n"
            f"Expression: {self.expression}\n"
            f"Expression value: {self.expression_value}\n"
            f"Expression value type: {self.expression_value_type}\n"
            f"Criterion: {self.criterion}\n"
            f"Value: {self.value}\n"
            f"Value type: {self.value_type}\n"
        )


# endregion


# region DesignVariable
class DesignVariable:
    """Stores information about a design variable."""

    def __init__(
        self,
        name: str = "",
        value: Optional[Union[bool, float, complex, list, dict]] = None,
    ) -> None:
        """Create a new instance of the ``DesignVariable`` class.

        Parameters
        ----------
        name: str, optional
            Variable's name. By default ``""``.
        value: Optional[Union[bool, float, complex, list, dict]], optional
            Variable's value.
        """
        self.name = name
        self.value = value

    def __deepcopy__(self, memo) -> DesignVariable:
        """Return deep copy of an instance of the ``DesignVariable`` class."""
        return DesignVariable(self.name, copy.deepcopy(self.value))

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``DesignVariable`` class.

        Parameters
        ----------
        other: DesignVariable
            Variable for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return type(self) == type(other) and self.name == other.name and self.value == other.value

    @property
    def name(self) -> str:
        """Name of the design variable."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the design variable.

        Parameters
        ----------
        name : str
            Name of the design variable.

        Raises
        ------
        TypeError
            Raised when type of the name is invalid.
        """
        if not isinstance(name, str):
            raise TypeError(f"String was expected but type: ``{type(name)}`` was given.")
        else:
            self.__name = name

    @property
    def value(self) -> Union[bool, float, complex, list, dict, None]:
        """Value of the design variable."""
        return self.__value

    @value.setter
    def value(self, value: Union[bool, float, complex, list, dict, None]) -> None:
        """Set the value of the design variable.

        Parameters
        ----------
        value : Union[bool, float, complex, list, dict, None]
            Value of the design variable.
        """
        self.__value = value

    def __str__(self) -> str:
        """Return information about the design variable."""
        return f"Name: {self.name}\n" f"Value: {self.value}\n"


# endregion


# region Parameters
class Parameter:
    """Stores parameter data."""

    def __init__(
        self,
        name: str = "",
        reference_value: Optional[Union[bool, float, str]] = None,
        id: Optional[str] = None,
        const: bool = False,
        type_: Union[ParameterType, str] = ParameterType.DETERMINISTIC,
    ) -> None:
        """Create a new instance of ``Parameter``.

        Parameters
        ----------
        name: str, optional
            Name of the parameter. By default ``""``.
        reference_value: Optional[Union[bool, float, str]], optional
            Parameter's reference value. By default ``None``.
        id: str, optional
            Parameter's unique id. By default ``None``.
            A unique Id is automatically generated if not specified.
        const: bool, optional
            Determines whether is parameter constant. By default ``False``.
        type: Union[ParameterType, str], optional
            Parameter's type. By default ``ParameterType.DETERMINISTIC``.
        """
        self.name = name
        self.reference_value = reference_value
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        self.const = const
        if isinstance(type_, str):
            type_ = ParameterType.from_str(type_)
        if isinstance(type_, ParameterType):
            self.__type = type_
        else:
            raise TypeError(
                "Type ``Union[ParameterType, str]`` was expected, but type: "
                f"``{type(type_)}`` was given."
            )

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``Parameter`` class.

        Parameters
        ----------
        other: Parameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.id == other.id
            and self.const == other.const
            and self.type == other.type
        )

    def __deepcopy__(self, memo) -> Parameter:
        """Return deep copy of given parameter."""
        return Parameter(
            self.name,
            self.reference_value,
            self.id,
            self.const,
            self.type,
        )

    @property
    def name(self) -> str:
        """Name of the parameter."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the parameter.

        Parameters
        ----------
        name: str
            Name of the parameter.

        Raises
        ------
        TypeError
            Raised when the type of the name is invalid.
        """
        if not isinstance(name, str):
            raise TypeError(
                f"Type of ``name`` must be ``str`` but type: ``{type(name)}`` was given."
            )
        self.__name = name

    @property
    def id(self) -> str:
        """ID of the parameter."""
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        """Set the ID of the parameter.

        Parameters
        ----------
        id: str
            ID of the parameter.

        Raises
        ------
        TypeError
            Raised when the type of the ID is invalid.
        """
        if not isinstance(id, str) and not id is None:
            raise TypeError(f"Type of ``id`` must be ``str`` but type: ``{type(id)}`` was given.")
        self.__id = id

    @property
    def const(self) -> bool:
        """Whether the value for the parameter is a constant."""
        return self.__const

    @const.setter
    def const(self, is_const: bool) -> None:
        """Set whether the value for the parameter is a constant.

        Parameters
        ----------
        is_const: bool
            Whether the value for the parameter is a constant.
            Options are ``True`` and ``False``.

        Raises
        ------
        TypeError
            Raised when the type for this Boolean attribute is invalid.
        """
        if not isinstance(is_const, bool):
            raise TypeError(
                f"Type of ``is_const`` must be ``bool`` but type: ``{type(is_const)}`` was given."
            )
        self.__const = is_const

    @property
    def reference_value(
        self,
    ) -> Union[bool, float, str, None]:
        """Reference value of the parameter."""
        return self.__reference_value

    @reference_value.setter
    def reference_value(
        self,
        reference_value: Union[bool, float, str, None],
    ) -> None:
        """Set the reference value of the parameter.

        Parameters
        ----------
        reference_value: Union[bool, float, str, None]
            Reference value of the parameter.

        Raises
        ------
        TypeError
            Raised when the type for the reference value is invalid.
        """
        if type(reference_value) in [bool, int, float, str] or reference_value is None:
            self.__reference_value = reference_value
        else:
            raise TypeError(
                f"Type of ``reference_value``: ``{type(reference_value)}`` "
                "not in [bool, int, float, str]."
            )

    @property
    def type(self) -> ParameterType:
        """Type of the parameter."""
        return self.__type

    @staticmethod
    def from_dict(par_dict: dict) -> Parameter:
        """Create an instance of the ``Parameter`` class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from the optiSLang server.

        Returns
        -------
        Parameter
            Instance of the ``Parameter`` class.

        Raises
        ------
        TypeError
            Raised when an undefined type of parameter is given.
        """
        parameter_properties = __class__._extract_parameter_properties_from_dict(par_dict=par_dict)

        if parameter_properties["type"] == ParameterType.DEPENDENT:
            return DependentParameter(
                name=parameter_properties["name"],
                operation=parameter_properties["operation"],
                reference_value=parameter_properties["reference_value"],
                id=parameter_properties["id"],
                const=parameter_properties["const"],
            )
        elif parameter_properties["type"] == ParameterType.DETERMINISTIC:
            return OptimizationParameter(
                name=parameter_properties["name"],
                reference_value=parameter_properties["reference_value"],
                reference_value_type=parameter_properties["reference_value_type"],
                id=parameter_properties["id"],
                const=parameter_properties["const"],
                deterministic_resolution=parameter_properties["deterministic_resolution"],
                range=parameter_properties["range"],
            )
        elif parameter_properties["type"] == ParameterType.STOCHASTIC:
            return StochasticParameter(
                name=parameter_properties["name"],
                reference_value=parameter_properties["reference_value"],
                id=parameter_properties["id"],
                const=parameter_properties["const"],
                stochastic_resolution=parameter_properties["stochastic_resolution"],
                distribution_type=parameter_properties["distribution_type"],
                distribution_parameters=parameter_properties["distribution_parameters"],
                statistical_moments=parameter_properties["statistical_moments"],
                cov=parameter_properties["cov"],
            )
        elif parameter_properties["type"] == ParameterType.MIXED:
            return MixedParameter(
                name=parameter_properties["name"],
                reference_value=parameter_properties["reference_value"],
                id=parameter_properties["id"],
                const=parameter_properties["const"],
                deterministic_resolution=parameter_properties["deterministic_resolution"],
                range=parameter_properties["range"],
                stochastic_resolution=parameter_properties["stochastic_resolution"],
                distribution_type=parameter_properties["distribution_type"],
                distribution_parameters=parameter_properties["distribution_parameters"],
                statistical_moments=parameter_properties["statistical_moments"],
                cov=parameter_properties["cov"],
            )
        else:
            raise TypeError("Undefined type of parameter.")

    @staticmethod
    def _extract_parameter_properties_from_dict(par_dict: dict) -> dict:
        properties_dict = {
            "name": par_dict["name"],
            "reference_value": par_dict["reference_value"],
            "reference_value_type": (
                par_dict["deterministic_property"].get("domain_type", {}).get("value", None)
                if par_dict.get("deterministic_property")
                else None
            ),
            "id": par_dict["id"],
            "const": par_dict["const"],
            "type": ParameterType.from_str(par_dict["type"]["value"]),
            "operation": par_dict.get("dependency_expression", None),
            "deterministic_resolution": (
                ParameterResolution.from_str(
                    par_dict["deterministic_property"].get("kind", {}).get("value", None)
                )
                if par_dict.get("deterministic_property")
                else None
            ),
            "stochastic_resolution": (
                ParameterResolution.from_str(
                    par_dict["stochastic_property"].get("kind", {}).get("value", None)
                )
                if par_dict.get("stochastic_property")
                else None
            ),
            "distribution_type": (
                DistributionType.from_str(
                    par_dict.get("stochastic_property", {}).get("type", {}).get("value", None)
                )
                if par_dict.get("stochastic_property")
                else None
            ),
            "distribution_parameters": (
                tuple(par_dict["stochastic_property"]["distribution_parameters"])
                if par_dict.get("stochastic_property", {}).get("distribution_parameters")
                else None
            ),
            "statistical_moments": (
                tuple(par_dict["stochastic_property"]["statistical_moments"])
                if par_dict.get("stochastic_property", {}).get(
                    "statistical_moments",
                )
                else None
            ),
            "cov": par_dict.get("stochastic_property", {}).get("cov", None),
        }
        # range for continuous parameters, stored as (val1, val2)
        if properties_dict["deterministic_resolution"] == ParameterResolution.CONTINUOUS:
            properties_dict["range"] = (
                par_dict.get("deterministic_property", {}).get("lower_bound", None),
                par_dict.get("deterministic_property", {}).get("upper_bound", None),
            )
        # discrete values otherwise, stored as ([val1, val2, val3 ..])
        elif properties_dict["deterministic_resolution"] is not None:
            properties_dict["range"] = (
                tuple(par_dict.get("deterministic_property", {}).get("discrete_states", [])),
            )
        else:
            properties_dict["range"] = None
        return properties_dict


class DependentParameter(Parameter):
    """Stores dependent parameter data."""

    def __init__(
        self,
        name: str = "",
        operation: str = "0",
        reference_value: Optional[Union[bool, float, str, Tuple[Any, ParameterValueType]]] = None,
        id: Optional[str] = None,
        const: bool = False,
    ) -> None:
        """Create an instance of the ``DependentParameter`` class.

        Parameters
        ----------
        name: str, optional
            Name of the parameter. By default ``""``.
        operation: str, optional
            Mathematic expression to evaluate. By default ``"0"``.
        reference_value: Optional[Union[bool, float, str, Tuple[Any, ParameterValueType]]], optional
            Reference value of the parameter. By default ``None``.
        id: str, optional
            Unique ID of the parameter. A unique Id is automatically generated if not specified.
        const: bool, optional
            Whether the parameter is a constant. By default ``False``.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type_=ParameterType.DEPENDENT,
        )

        if not isinstance(operation, str):
            raise TypeError(f"String was expected but type: `{type(operation)}` was given.")
        else:
            self.__operation = operation

    def __eq__(self, other) -> bool:
        r"""Compare properties of two instances of the ``DependentParameter`` class.

        Parameters
        ----------
        other: DependentParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match, ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.id == other.id
            and self.const == other.const
            and self.type == other.type
            and self.operation == other.operation
        )

    def __deepcopy__(self, memo) -> DependentParameter:
        """Return a deep copy of a instance of the ``DependentParameter`` class."""
        return DependentParameter(
            name=self.name,
            reference_value=self.reference_value,
            id=self.id,
            const=self.const,
            operation=self.operation,
        )

    @property
    def operation(self) -> str:
        """Operation expression."""
        return self.__operation

    @operation.setter
    def operation(self, expression: str) -> None:
        """Set operation expression."""
        if not isinstance(expression, str):
            raise TypeError(f"String was expected but type: `{type(expression)}` was given.")
        else:
            self.__operation = expression
            self.reference_value = None

    def to_dict(self) -> dict:
        """Convert an instance of the ``DependentParameter`` class to a dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.

        """
        ret_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "dependency_expression": self.operation if self.operation is not None else "0",
            "modifiable": False,
            "name": self.name,
            "reference_value": None,
            "removable": True,
            "type": {"value": self.type.name.lower()},
            "unit": "",
        }

        if self.id is not None:
            ret_dict["id"] = self.id

        return ret_dict

    def __str__(self) -> str:
        """Return information about the parameter."""
        return (
            f"Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Reference value: {self.reference_value}\n"
            f"Const: {self.const}\n"
            f"Type: {self.type}\n"
            f"Dependency expression: {self.operation}\n"
        )


class MixedParameter(Parameter):
    """Stores mixed parameter data."""

    def __init__(
        self,
        name: str = "",
        reference_value: float = 0,
        id: Optional[str] = None,
        const: bool = False,
        deterministic_resolution: Union[ParameterResolution, str] = ParameterResolution.CONTINUOUS,
        range: Union[Sequence[float, float], Sequence[Sequence[float]]] = (-1, 1),
        stochastic_resolution: Union[
            ParameterResolution, str
        ] = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: Union[DistributionType, str] = DistributionType.NORMAL,
        distribution_parameters: Optional[Sequence[float]] = None,
        statistical_moments: Optional[Sequence[float]] = None,
        cov: Optional[float] = None,
    ) -> None:
        """Create a new instance of the ``MixedParameter`` class.

        Parameters
        ----------
        name: str, optional
            Name of the parameter. By default ``""``.
        reference_value: float, optional
            Parameter's reference value. By default ``0``.
        id: str, optional
            Parameter's unique id. A unique Id is automatically generated if not specified.
        const: bool, optional
            Determines whether is parameter constant. By default ``False``.
        deterministic_resolution: Union[ParameterResolution, str], optional
            Parameter's deterministic resolution. By default ``ParameterResolution.CONTINUOUS``.
        range: Union[Sequence[float, float], Sequence[Sequence[float]]], optional
            Either 2 values specifying range or list of discrete values. By default ``(-1, 1)``.
        stochastic_resolution: Union[ParameterResolution, str], optional
            Parameter's stochastic resolution.
            By default ``ParameterResolution.MARGINALDISTRIBUTION``.
        distribution_type: Union[DistributionType, str], optional
            Parameter's distribution type. By default ``DistributionType.NORMAL``.
        distribution_parameters: Optional[Sequence[float, ...]], optional
            Distribution's parameters. By default ``None``.
        statistical_moments: Optional[Sequence[float, ...]], optional
            Distribution's statistical moments. By default ``None``.
        cov: Optional[float], optional
            Distribution's COV. By default ``None``.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type_=ParameterType.MIXED,
        )
        self.__reference_value_type = ParameterValueType.REAL
        self.deterministic_resolution = deterministic_resolution
        self.range = range
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = (
            tuple(distribution_parameters) if distribution_parameters is not None else None
        )
        self.statistical_moments = (
            tuple(statistical_moments) if statistical_moments is not None else None
        )
        self.cov = cov

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``MixedParameter`` class.

        Parameters
        ----------
        other: MixedParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.reference_value_type == other.reference_value_type
            and self.id == other.id
            and self.const == other.const
            and self.type == other.type
            and self.deterministic_resolution == other.deterministic_resolution
            and self.range == other.range
            and self.stochastic_resolution == other.stochastic_resolution
            and self.distribution_type == other.distribution_type
            and self.distribution_parameters == other.distribution_parameters
            and self.statistical_moments == other.statistical_moments
            and self.cov == other.cov
        )

    def __deepcopy__(self, memo) -> MixedParameter:
        """Return deep copy of the instance of ``MixedParameter`` class."""
        return MixedParameter(
            name=self.name,
            reference_value=self.reference_value,
            id=self.id,
            const=self.const,
            deterministic_resolution=self.deterministic_resolution,
            range=self.range,
            stochastic_resolution=self.stochastic_resolution,
            distribution_type=self.distribution_type,
            distribution_parameters=self.distribution_parameters,
            statistical_moments=self.statistical_moments,
            cov=self.cov,
        )

    @property
    def reference_value_type(self) -> ParameterValueType:
        """Type of the reference value."""
        return self.__reference_value_type

    @property
    def deterministic_resolution(self) -> ParameterResolution:
        """Type of the deterministic resolution."""
        return self.__deterministic_resolution

    @deterministic_resolution.setter
    def deterministic_resolution(
        self, deterministic_resolution: Union[ParameterResolution, str]
    ) -> None:
        """Set the type of the deterministic resolution.

        Parameters
        ----------
        deterministic_resolution : Union[ParameterResolution, str]
            Type of the deterministic resolution.

        Raises
        ------
        TypeError
            Raised when the type of the deterministic resolution is invalid.
        """
        if isinstance(deterministic_resolution, str):
            deterministic_resolution = ParameterResolution.from_str(deterministic_resolution)
        if isinstance(deterministic_resolution, ParameterResolution):
            self.__deterministic_resolution = deterministic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(deterministic_resolution)}`` was given."
            )

    @property
    def range(self) -> Union[Tuple[float, float], Tuple[Tuple[float, ...]]]:
        """Range of the mixed parameter."""
        return self.__range

    @range.setter
    def range(self, range: Union[Sequence[float, float], Sequence[Sequence[float]]]) -> None:
        """Set the range of the mixed parameter.

        Parameters
        ----------
        range : Union[Sequence[float, float], Sequence[Sequence[float]]]
            Range of the mixed parameter.
        """
        if not isinstance(range[0], (int, float)):
            self.__range = (tuple(range[0]),)
        else:
            self.__range = tuple(range)

    @property
    def stochastic_resolution(self) -> ParameterResolution:
        """Type of the stochastic resolution."""
        return self.__stochastic_resolution

    @stochastic_resolution.setter
    def stochastic_resolution(self, stochastic_resolution: Union[ParameterResolution, str]) -> None:
        """Set the type of the stochastic resolution.

        Parameters
        ----------
        stochastic_resolution : Union[ParameterResolution, str]
            Type of the stochastic resolution.

        Raises
        ------
        TypeError
            Raised when the type of the stochastic resolution is invalid.
        """
        if isinstance(stochastic_resolution, str):
            stochastic_resolution = ParameterResolution.from_str(stochastic_resolution)
        if isinstance(stochastic_resolution, ParameterResolution):
            self.__stochastic_resolution = stochastic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(stochastic_resolution)}`` was given."
            )

    @property
    def distribution_type(self) -> DistributionType:
        """Type of the distribution."""
        return self.__distribution_type

    @distribution_type.setter
    def distribution_type(self, distribution_type: Union[DistributionType, str]) -> None:
        """Set the type of the distribution.

        Parameters
        ----------
        distribution_type : Union[DistributionType, str]
            Type of the distribution.

        Raises
        ------
        TypeError
            Raised when the type of the distribution is invalid.
        """
        if isinstance(distribution_type, str):
            distribution_type = DistributionType.from_str(distribution_type)
        if isinstance(distribution_type, DistributionType):
            self.__distribution_type = distribution_type
        else:
            raise TypeError(
                "Type Union[DistributionType, str] was expected, but type: "
                f"``{type(distribution_type)}`` was given."
            )

    @property
    def distribution_parameters(self) -> Union[Tuple[float], None]:
        """Parameters of the distribution."""
        return self.__distribution_parameters

    @distribution_parameters.setter
    def distribution_parameters(self, parameters: Union[Sequence[float], None]):
        """Set the parameters of the distribution.

        Parameters
        ----------
        parameters : Sequence[float]
            Parameters of the distribution.
        """
        if parameters is not None:
            self.__distribution_parameters = tuple(parameters)
        else:
            self.__distribution_parameters = None

    @property
    def statistical_moments(self) -> Union[Tuple[float], None]:
        """Statistical moments of the distribution."""
        return self.__statistical_moments

    @statistical_moments.setter
    def statistical_moments(self, moments: Union[Sequence[float], None]):
        """Set the statistical moments of the distribution.

        Parameters
        ----------
        moments : Sequence[float]
            Statistical moments of the distribution.
        """
        if moments is not None:
            self.__statistical_moments = tuple(moments)
        else:
            self.__statistical_moments = None

    @property
    def cov(self) -> Union[float, None]:
        """COV of the distribution."""
        return self.__cov

    @cov.setter
    def cov(self, cov: Union[float, None]):
        """Set the statistical moments of the distribution.

        Parameters
        ----------
        moments : Sequence[float]
            Statistical moments of the distribution.
        """
        self.__cov = cov

    def to_dict(self) -> dict:
        """Convert an instance of the ``MixedParameter`` class to a dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.
        """
        if len(self.range) == 1:
            range_dict = {"discrete_states": self.range[0]}
        else:
            range_dict = {
                "lower_bound": self.range[0],
                "upper_bound": self.range[1],
            }
        stochastic_property = {
            "kind": {"value": self.stochastic_resolution.name.lower()},
            "type": {"value": self.distribution_type.name.lower()},
        }
        if self.distribution_parameters is not None:
            stochastic_property["distribution_parameters"] = self.distribution_parameters
        if self.statistical_moments is not None:
            stochastic_property["statistical_moments"] = self.statistical_moments
        if self.cov is not None:
            stochastic_property["cov"] = self.cov
        output_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "deterministic_property": {
                "domain_type": {"value": self.reference_value_type.name.lower()},
                "kind": {"value": self.deterministic_resolution.name.lower()},
            },
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value if self.reference_value else 0,
            "removable": True,
            "stochastic_property": stochastic_property,
            "type": {"value": self.type.name.lower()},
            "unit": "",
        }

        if self.id is not None:
            output_dict["id"] = self.id

        output_dict["deterministic_property"].update(range_dict)
        return output_dict

    def __str__(self) -> str:
        """Return information about the parameter."""
        return (
            f"Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Reference value: {self.reference_value}\n"
            f"Reference value type: {self.reference_value_type}\n"
            f"Const: {self.const}\n"
            f"Type: {self.type}\n"
            f"Deterministic resolution: {self.deterministic_resolution}\n"
            f"Range: {self.range}\n"
            f"Stochastic_resolution: {self.stochastic_resolution}\n"
            f"Distribution type: {self.distribution_type}\n"
            f"Distribution parameters: {self.distribution_parameters}\n"
            f"Statistical moments: {self.statistical_moments}\n"
            f"COV: {self.cov}\n"
        )


class OptimizationParameter(Parameter):
    """Stores optimization parameter data."""

    def __init__(
        self,
        name: str = "",
        reference_value: Union[bool, float, str, None] = 0,
        reference_value_type: ParameterValueType = ParameterValueType.REAL,
        id: Optional[str] = None,
        const: bool = False,
        deterministic_resolution: Union[ParameterResolution, str] = ParameterResolution.CONTINUOUS,
        range: Union[Sequence[float, float], Sequence[Sequence[float]]] = (-1, 1),
    ) -> None:
        """Create a new instance of ``OptimizationParameter``.

        Parameters
        ----------
        name: str, optional
            Name of the parameter. By default ``""``.
        reference_value: Union[bool, float, str, None], optional
            Parameter's reference value. By default ``0``.
        reference_value_type: ParameterValueType, optional
            Type of the reference value. By default ``ParameterValueType.REAL``.
        id: str, optional
            Parameter's unique id. A unique Id is automatically generated if not specified.
        const: bool, optional
            Determines whether is parameter constant. By default ``False``.
        deterministic_resolution: Union[ParameterResolution, str], optional
            Parameter's deterministic resolution. By default ``ParameterResolution.CONTINUOUS``.
        range: Union[Sequence[float, float], Sequence[Sequence[float]]], optional
            Either 2 values specifying range or list of discrete values. By default ``(-1, 1)``.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type_=ParameterType.DETERMINISTIC,
        )
        self.reference_value_type = reference_value_type
        self.deterministic_resolution = deterministic_resolution
        self.range = range

    def __eq__(self, other) -> bool:
        r"""Compare properties of two instances of the ``OptimizationParameter`` class.

        Parameters
        ----------
        other: OptimizationParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.reference_value_type == other.reference_value_type
            and self.id == other.id
            and self.const == other.const
            and self.type == other.type
            and self.deterministic_resolution == other.deterministic_resolution
            and self.range == other.range
        )

    def __deepcopy__(self, memo) -> OptimizationParameter:
        """Return deep copy of the optimization parameter."""
        return OptimizationParameter(
            name=self.name,
            reference_value=self.reference_value,
            reference_value_type=self.reference_value_type,
            id=self.id,
            const=self.const,
            deterministic_resolution=self.deterministic_resolution,
            range=self.range,
        )

    @property
    def reference_value_type(self) -> ParameterValueType:
        """Type of the reference value."""
        return self.__reference_value_type

    @reference_value_type.setter
    def reference_value_type(self, type_: Union[ParameterValueType, str]) -> None:
        """Set the type of the reference value.

        Parameters
        ----------
        type_ : Union[ParameterValueType, str]
           Type of the reference value.

        Raises
        ------
        TypeError
            Raised when the type of the reference value is invalid.
        """
        if isinstance(type_, str):
            type_ = ParameterValueType.from_str(type_)
        if isinstance(type_, ParameterValueType):
            self.__reference_value_type = type_
        else:
            raise TypeError(
                "Type ``Union[ParameterValueType, str]`` was expected, but type: "
                f"``{type(type_)}`` was given."
            )

    @property
    def deterministic_resolution(self) -> ParameterResolution:
        """Type of the deterministic resolution."""
        return self.__deterministic_resolution

    @deterministic_resolution.setter
    def deterministic_resolution(
        self, deterministic_resolution: Union[ParameterResolution, str]
    ) -> None:
        """Set the type of the deterministic resolution.

        Parameters
        ----------
        deterministic_resolution : Union[ParameterResolution, str]
            Type of the deterministic resolution.

        Raises
        ------
        TypeError
            Raised when the type of the deterministic_resolution is invalid.
        """
        if isinstance(deterministic_resolution, str):
            deterministic_resolution = ParameterResolution.from_str(deterministic_resolution)
        if isinstance(deterministic_resolution, ParameterResolution):
            self.__deterministic_resolution = deterministic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(deterministic_resolution)}`` was given."
            )

    @property
    def range(self) -> Union[Tuple[float, float], Tuple[Tuple[float, ...]]]:
        """Range of the optimization parameter."""
        return self.__range

    @range.setter
    def range(self, range: Union[Sequence[float, float], Sequence[Sequence[float]]]) -> None:
        """Set the range of the optimization parameter.

        Parameters
        ----------
        range: Union[Sequence[float, float], Sequence[Sequence[float]]]
            Range of the optimization parameter.
        """
        if not isinstance(range[0], (float, int)):
            self.__range = (tuple(range[0]),)
        else:
            self.__range = tuple(range)

    def to_dict(self) -> dict:
        """Convert an instance of the ``OptimizationParameter`` to a dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.
        """
        if len(self.range) == 1:
            range_dict = {"discrete_states": self.range[0]}
        else:
            range_dict = {
                "lower_bound": self.range[0],
                "upper_bound": self.range[1],
            }
        output_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "deterministic_property": {
                "domain_type": {"value": self.reference_value_type.name.lower()},
                "kind": {"value": self.deterministic_resolution.name.lower()},
            },
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value,
            "removable": True,
            "type": {"value": self.type.name.lower()},
            "unit": "",
        }
        if self.id is not None:
            output_dict["id"] = self.id
        output_dict["deterministic_property"].update(range_dict)
        return output_dict

    def __str__(self) -> str:
        """Return information about the parameter."""
        return (
            f"Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Reference value: {self.reference_value}\n"
            f"Reference value type: {self.reference_value_type}\n"
            f"Const: {self.const}\n"
            f"Type: {self.type}\n"
            f"Deterministic resolution: {self.deterministic_resolution}\n"
            f"Range: {self.range}\n"
        )


class StochasticParameter(Parameter):
    """Stores stochastic parameter data."""

    def __init__(
        self,
        name: str = "",
        reference_value: float = 0,
        id: Optional[str] = None,
        const: bool = False,
        stochastic_resolution: Union[
            ParameterResolution, str
        ] = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: Union[DistributionType, str] = DistributionType.NORMAL,
        distribution_parameters: Optional[Sequence[float]] = None,
        statistical_moments: Optional[Sequence[float]] = None,
        cov: Optional[float] = None,
    ) -> None:
        """Create a new instance of the ``StochasticParameter`` class.

        Parameters
        ----------
        name: str, optional
            Name of the parameter. By default ``""``.
        reference_value: float, optional
            Parameter's reference value. By default ``0``.
        id: str, optional
            Parameter's unique id. A unique Id is automatically generated if not specified.
        const: bool, optional
            Determines whether is parameter constant. By default ``False``.
        stochastic_resolution: Union[ParameterResolution, str], optional
            Parameter's stochastic resolution.
            By default ``ParameterResolution.MARGINALDISTRIBUTION``.
        distribution_type: Union[DistributionType, str], optional
            Parameter's distribution type. By default ``DistributionType.NORMAL``.
        distribution_parameters: Optional[Sequence[float, ...]], optional
            Distribution's parameters. Defaults to ``None``.
        statistical_moments: Optional[Sequence[float, ...]], optional
            Distribution's statistical moments. Defaults to ``None``.
        cov: Optional[float], optional
            Distribution's COV. Defaults to ``None``.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type_=ParameterType.STOCHASTIC,
        )
        self.__reference_value_type = ParameterValueType.REAL
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = (
            tuple(distribution_parameters) if distribution_parameters is not None else None
        )
        self.statistical_moments = (
            tuple(statistical_moments) if statistical_moments is not None else None
        )
        self.cov = cov

    def __eq__(self, other) -> bool:
        r"""Compare properties of two instances of the ``StochasticParameter`` class.

        Parameters
        ----------
        other: StochasticParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.reference_value_type == other.reference_value_type
            and self.id == other.id
            and self.const == other.const
            and self.type == other.type
            and self.stochastic_resolution == other.stochastic_resolution
            and self.distribution_type == other.distribution_type
            and self.distribution_parameters == other.distribution_parameters
            and self.statistical_moments == other.statistical_moments
            and self.cov == other.cov
        )

    def __deepcopy__(self, memo) -> StochasticParameter:
        """Return deep copy of the stochastic parameter."""
        return StochasticParameter(
            name=self.name,
            reference_value=self.reference_value,
            id=self.id,
            const=self.const,
            stochastic_resolution=self.stochastic_resolution,
            distribution_type=self.distribution_type,
            distribution_parameters=self.distribution_parameters,
            statistical_moments=self.statistical_moments,
            cov=self.cov,
        )

    @property
    def reference_value_type(self) -> ParameterValueType:
        """Type of the reference value``."""
        return self.__reference_value_type

    @property
    def stochastic_resolution(self) -> ParameterResolution:
        """Type of the stochastic resolution."""
        return self.__stochastic_resolution

    @stochastic_resolution.setter
    def stochastic_resolution(self, stochastic_resolution: Union[ParameterResolution, str]) -> None:
        """Set the type of the stochastic resolution.

        Parameters
        ----------
        stochastic_resolution : Union[ParameterResolution, str]
            Type of the stochastic resolution.

        Raises
        ------
        TypeError
            Raised when the type of the stochastic resolution is invalid.
        """
        if isinstance(stochastic_resolution, str):
            stochastic_resolution = ParameterResolution.from_str(stochastic_resolution)
        if isinstance(stochastic_resolution, ParameterResolution):
            self.__stochastic_resolution = stochastic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(stochastic_resolution)}`` was given."
            )

    @property
    def distribution_type(self) -> DistributionType:
        """Type of the distribution."""
        return self.__distribution_type

    @distribution_type.setter
    def distribution_type(self, distribution_type: Union[DistributionType, str]) -> None:
        """Set the type of the distribution.

        Parameters
        ----------
        distribution_type : Union[DistributionType, str]
            Type of the distribution.

        Raises
        ------
        TypeError
            Raised when the type of the distribution is invalid.
        """
        if isinstance(distribution_type, str):
            distribution_type = DistributionType.from_str(distribution_type)
        if isinstance(distribution_type, DistributionType):
            self.__distribution_type = distribution_type
        else:
            raise TypeError(
                "Type Union[DistributionType, str] was expected, but type: "
                f"``{type(distribution_type)}`` was given."
            )

    @property
    def distribution_parameters(self) -> Union[Tuple[float], None]:
        """Parameters of the distribution."""
        return self.__distribution_parameters

    @distribution_parameters.setter
    def distribution_parameters(self, parameters: Union[Sequence[float], None]):
        """Set the parameters of the distribution.

        Parameters
        ----------
        parameters : Sequence[float]
            Parameters of the distribution.
        """
        if parameters is not None:
            self.__distribution_parameters = tuple(parameters)
        else:
            self.__distribution_parameters = None

    @property
    def statistical_moments(self) -> Union[Tuple[float], None]:
        """Statistical moments of the distribution."""
        return self.__statistical_moments

    @statistical_moments.setter
    def statistical_moments(self, moments: Union[Sequence[float], None]):
        """Set the statistical moments of the distribution.

        Parameters
        ----------
        moments : Sequence[float]
            Statistical moments of the distribution.
        """
        if moments is not None:
            self.__statistical_moments = tuple(moments)
        else:
            self.__statistical_moments = None

    @property
    def cov(self) -> Union[float, None]:
        """COV of the distribution."""
        return self.__cov

    @cov.setter
    def cov(self, cov: Union[float, None]):
        """Set the statistical moments of the distribution.

        Parameters
        ----------
        moments : Sequence[float]
            Statistical moments of the distribution.
        """
        self.__cov = cov

    def to_dict(self) -> dict:
        """Convert an instance of the ``StochasticParameter`` to dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.
        """
        stochastic_property = {
            "kind": {"value": self.stochastic_resolution.name.lower()},
            "type": {"value": self.distribution_type.name.lower()},
        }
        if self.distribution_parameters is not None:
            stochastic_property["distribution_parameters"] = self.distribution_parameters
        if self.statistical_moments is not None:
            stochastic_property["statistical_moments"] = self.statistical_moments
        if self.cov is not None:
            stochastic_property["cov"] = self.cov
        output_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value,
            "removable": True,
            "stochastic_property": stochastic_property,
            "type": {"value": self.type.name.lower()},
            "unit": "",
        }
        if self.id is not None:
            output_dict["id"] = self.id
        return output_dict

    def __str__(self) -> str:
        """Return information about the parameter."""
        return (
            f"Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Reference value: {self.reference_value}\n"
            f"Reference value type: {self.reference_value_type}\n"
            f"Const: {self.const}\n"
            f"Type: {self.type}\n"
            f"Stochastic_resolution: {self.stochastic_resolution}\n"
            f"Distribution type: {self.distribution_type}\n"
            f"Distribution parameters: {self.distribution_parameters}\n"
            f"Statistical moments: {self.statistical_moments}\n"
            f"COV: {self.cov}\n"
        )


# endregion


# region Response
class Response:
    """Stores response data."""

    def __init__(
        self,
        name: str = "",
        reference_value: Union[
            Tuple[ResponseValueType, str], bool, float, complex, list, dict, None
        ] = None,
        reference_value_type: Optional[ResponseValueType] = None,
    ) -> None:
        """Create a new instance of ``Response``.

        Parameters
        ----------
        name: str, optional
            Response name. By default ``""``.
        reference_value: Union[tuple, bool, float, complex, list, dict, None], optional
            Reference value of the response. By default ``None``.
        reference_value_type: Optional[ResponseValueType], optional
            Type of the response reference value. Defaults to ``None``.
        """
        self.name = name
        if reference_value and isinstance(reference_value_type, ResponseValueType):
            self.reference_value = (reference_value_type, reference_value)
        else:
            self.reference_value = reference_value

    def __eq__(self, other) -> bool:
        """Compare properties of two instances of the ``Response`` class.

        Parameters
        ----------
        other: Response
            Response for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.reference_value == other.reference_value
            and self.reference_value_type == other.reference_value_type
        )

    def __deepcopy__(self, memo) -> Response:
        """Return deep copy of given response."""
        return Response(
            name=self.name,
            reference_value=copy.deepcopy(self.reference_value),
            reference_value_type=self.reference_value_type,
        )

    @property
    def name(self) -> str:
        """Name of the response."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the response.

        Parameters
        ----------
        name: str
            Name of the response.

        Raises
        ------
        TypeError
            Raised when the type of the name is invalid.
        """
        if not isinstance(name, str):
            raise TypeError(
                f"Type of ``name`` must be ``str`` but type: ``{type(name)}`` was given."
            )
        self.__name = name

    @property
    def reference_value(self) -> Union[bool, float, complex, list, dict, None]:
        """Reference value of the response."""
        return self.__reference_value

    @reference_value.setter
    def reference_value(
        self,
        reference_value: Union[
            Tuple[ResponseValueType, str], bool, float, complex, list, dict, None
        ],
    ) -> None:
        """Set response reference value."""
        if isinstance(reference_value, tuple) and isinstance(reference_value[0], ResponseValueType):
            self.__reference_value = self._parse_str_to_value(
                reference_value[0], reference_value[1]
            )
            self.__reference_value_type = reference_value[0]
        else:
            self.__reference_value = reference_value
            self.__reference_value_type = self._get_reference_value_type(reference_value)

    @property
    def reference_value_type(self) -> ResponseValueType:
        """Return type of the response reference value."""
        return self.__reference_value_type

    @staticmethod
    def _get_reference_value_type(reference_value: Any) -> ResponseValueType:
        """Return type of the reference value.

        Parameters
        ----------
        reference_value: Any
            Response reference value.
        """
        if isinstance(reference_value, bool):
            return ResponseValueType.BOOL
        elif isinstance(reference_value, (float, int, complex)):
            return ResponseValueType.SCALAR
        elif reference_value == None:
            return ResponseValueType.UNINITIALIZED
        elif isinstance(reference_value, list):
            return ResponseValueType.VECTOR
        elif isinstance(reference_value, dict):
            if reference_value.get("type") == "signal":
                return ResponseValueType.SIGNAL
            elif reference_value.get("type") == "xydata":
                return ResponseValueType.XYDATA
            else:
                return ResponseValueType.UNINITIALIZED
        else:
            raise TypeError(f"Unsupported type of value: ``{reference_value}``.")

    @staticmethod
    def _parse_str_to_value(
        reference_value_type: ResponseValueType,
        reference_value: Union[dict, None, bool, float, list],
    ):
        """Parse string representation of value to value.

        Parameters
        ----------
        reference_value_type: ResponseValueType
            Type of reference_value.
        reference_value: dict
            Dictionary with stored data.
        """
        if reference_value_type == ResponseValueType.UNINITIALIZED:
            return None
        elif reference_value_type == ResponseValueType.BOOL:
            return reference_value
        elif reference_value_type == ResponseValueType.SCALAR:
            if isinstance(reference_value, dict):
                return complex(real=reference_value.get("real"), imag=reference_value.get("imag"))
            elif isinstance(reference_value, (int, float)):
                return reference_value
        elif reference_value_type == ResponseValueType.VECTOR:
            return reference_value
        elif reference_value_type in [
            ResponseValueType.SIGNAL,
            ResponseValueType.XYDATA,
        ]:
            return reference_value
        else:
            raise TypeError(f"Invalid kind of response: ``{type}``.")

    @staticmethod
    def from_dict(name: str, reference_value: Union[bool, float, complex, list, dict]) -> Response:
        """Create an instance of the ``Response`` class from optiSLang output.

        Parameters
        ----------
        name: str
            Response's name.
        reference_value: Union[bool, float, complex, list, dict]
            Response's reference value.

        Returns
        -------
        Response
            Instance of the ``Response`` class.

        Raises
        ------
        TypeError
            Raised when undefined type of response is given.
        """
        if isinstance(reference_value, dict):
            reference_value_type = ResponseValueType.from_str(reference_value["type"])
        else:
            reference_value_type = None

        return Response(
            name=name, reference_value=reference_value, reference_value_type=reference_value_type
        )

    def to_dict(self) -> dict:
        """Convert an instance of the ``Response`` class to a dictionary.

        Returns
        -------
        dict
            Input dictionary for the optiSLang server.

        """
        return {
            "name": self.name,
            "reference_value": self.reference_value,
        }

    def __str__(self) -> str:
        """Return information about the response."""
        return (
            f"Name: {self.name}\n"
            f"Reference value: {self.reference_value}\n"
            f"Reference value type: {self.reference_value_type}\n"
        )


# endregion


# region Design
class Design:
    """Stores information about the design point, exclusively for the root system.

    Parameters
    ----------
    parameters : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Parameter, DesignVariable]],
    ], optional
        Dictionary of parameters and their values {'name': value, ...}
        or an iterable of design variables or parameters. By default ``[]``.
    constraints : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[ConstraintCriterion, DesignVariable]],
    ], optional
        Dictionary of constraint criteria and their values {'name': value, ...}
        or an iterable of design variables or constraint criteria. By default ``[]``.
    limit_states : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of limit state criteria and their values {'name': value, ...}
        or an iterable of design variables or limist state criteria. By default ``[]``.
    objectives : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of objective criteria and their values {'name': value, ...}
        or an iterable of design variables or objective criteria. By default ``[]``.
    variables : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Criterion, DesignVariable]],
    ], optional
        Dictionary of variable criteria and their values {'name': value, ...}
        or an iterable of design variables or variable criteria. By default ``[]``.
    responses : Union[
        Mapping[str, Union[bool, str, float, None]],
        Iterable[Union[Response, DesignVariable]],
    ], optional
        Dictionary of responses and their values {'name': value, ...}
        or an iterable of design variables or responses. By default `[]``.
    feasibility: Optional[bool], optional
        Determines whether design is feasible, defaults to `None` (no info about feasibility).
    design_id: Optional[int], optional
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
        feasibility: Optional[bool] = None,
        design_id: Optional[int] = None,
        status: DesignStatus = DesignStatus.IDLE,
    ) -> None:
        """Initialize a new instance of the ``Design`` class."""
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
            responses=self.__reset_output_value(copy.deepcopy(self.responses)),
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
        """Reset the status and feasibility, clear output values."""
        self.__status = DesignStatus.IDLE
        self.__feasibility = None
        self.__reset_output_value(self.constraints)
        self.__reset_output_value(self.limit_states)
        self.__reset_output_value(self.objectives)
        self.__reset_output_value(self.variables)
        self.__reset_output_value(self.responses)

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
                if isinstance(response, Response):
                    value = response.reference_value
                elif isinstance(response, DesignVariable):
                    value = response.value
                else:
                    raise TypeError(f"Response type: ``{type(response)}`` is not supported.")
                responses_list.append(DesignVariable(name=response.name, value=value))
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


# endregion

# endregion
