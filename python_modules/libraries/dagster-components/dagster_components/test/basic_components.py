"""Sample local components for testing validation. Paired with test cases
in integration_tests/components/validation.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from dagster._core.definitions.definitions_class import Definitions
from pydantic import BaseModel, ConfigDict

from dagster_components import Component, DSLSchema, ResolvableFromSchema
from dagster_components.core.component import ComponentLoadContext


def _inner_error():
    raise Exception("boom")


def _error():
    _inner_error()


class MyComponentSchema(DSLSchema):
    a_string: str
    an_int: int


@dataclass
class MyComponent(Component, ResolvableFromSchema[MyComponentSchema]):
    a_string: str
    an_int: int

    def build_defs(self, context: ComponentLoadContext) -> Definitions:
        return Definitions()

    @classmethod
    def get_additional_scope(cls) -> Mapping[str, Any]:
        return {
            "error": _error,
        }


class MyNestedModel(BaseModel):
    a_string: str
    an_int: int

    model_config = ConfigDict(extra="forbid")


class MyNestedComponentSchema(BaseModel):
    nested: dict[str, MyNestedModel]

    model_config = ConfigDict(extra="forbid")


class MyNestedComponent(Component):
    @classmethod
    def get_schema(cls) -> type[MyNestedComponentSchema]:
        return MyNestedComponentSchema

    def build_defs(self, context: ComponentLoadContext) -> Definitions:
        return Definitions()
