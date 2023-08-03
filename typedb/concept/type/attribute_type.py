#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import annotations
from datetime import datetime
from typing import Optional, Iterator, TYPE_CHECKING, Union, Any

from typedb.api.concept.type.attribute_type import AttributeType
from typedb.api.concept.value.value import ValueType
from typedb.common.label import Label
from typedb.common.streamer import Streamer
from typedb.common.transitivity import Transitivity
from typedb.concept.thing import attribute
from typedb.concept.type.thing_type import _ThingType
from typedb.concept.value.value import _Value

from typedb.typedb_client_python import attribute_type_set_supertype, attribute_type_get_supertype, \
    attribute_type_get_supertypes, attribute_type_get_subtypes, attribute_type_get_subtypes_with_value_type, \
    attribute_type_get_instances, attribute_type_get_owners, attribute_type_put, \
    attribute_type_get, attribute_type_get_regex, attribute_type_set_regex, attribute_type_unset_regex, \
    attribute_type_get_value_type, concept_iterator_next

if TYPE_CHECKING:
    from typedb.api.concept.thing.attribute import Attribute
    from typedb.api.concept.type.annotation import Annotation
    from typedb.api.concept.value.value import Value
    from typedb.connection.transaction import _Transaction


class _AttributeType(AttributeType, _ThingType):

    ROOT_LABEL = Label.of("attribute")

    def get_value_type(self) -> ValueType:
        return ValueType.of(attribute_type_get_value_type(self.native_object))

    def __eq__(self, other):
        if other is self:
            return True
        # root "attribute" should always be equal to itself regardless of which value class it holds
        if not other or not isinstance(other, _AttributeType):
            return False
        return self.get_label() == other.get_label()

    def __hash__(self):
        return super(_AttributeType, self).__hash__()

    def set_supertype(self, transaction: _Transaction, attribute_type: _AttributeType) -> None:
        attribute_type_set_supertype(self.native_transaction(transaction), self.native_object,
                                     attribute_type.native_object)

    def get_supertype(self, transaction: _Transaction) -> Optional[_AttributeType]:
        if res := attribute_type_get_supertype(self.native_transaction(transaction), self.native_object):
            return _AttributeType(res)
        return None

    def get_supertypes(self, transaction: _Transaction) -> Iterator[_AttributeType]:
        return (_AttributeType(item) for item in
                Streamer(attribute_type_get_supertypes(self.native_transaction(transaction), self.native_object),
                         concept_iterator_next))

    def get_subtypes(self, transaction: _Transaction) -> Iterator[_AttributeType]:
        return (_AttributeType(item) for item in
                Streamer(attribute_type_get_subtypes(self.native_transaction(transaction), self.native_object,
                                                     Transitivity.Transitive.value), concept_iterator_next))

    def get_subtypes_with_value_type(self, transaction: _Transaction, value_type: ValueType) -> Iterator[_AttributeType]:
        return (_AttributeType(item) for item in
                Streamer(attribute_type_get_subtypes_with_value_type(self.native_transaction(transaction), self.native_object,
                                                                     value_type.native_object,
                                                                     Transitivity.Transitive.value), concept_iterator_next))

    def get_subtypes_explicit(self, transaction: _Transaction) -> Iterator[_AttributeType]:
        return (_AttributeType(item) for item in
                Streamer(attribute_type_get_subtypes(self.native_transaction(transaction), self.native_object,
                                                     Transitivity.Explicit.value), concept_iterator_next))

    def get_instances(self, transaction: _Transaction) -> Iterator[attribute._Attribute]:
        return (attribute._Attribute(item) for item in
                Streamer(attribute_type_get_instances(self.native_transaction(transaction), self.native_object,
                                                      Transitivity.Transitive.value), concept_iterator_next))

    def get_instances_explicit(self, transaction: _Transaction) -> Iterator[attribute._Attribute]:
        return (attribute._Attribute(item) for item in
                Streamer(attribute_type_get_instances(self.native_transaction(transaction), self.native_object,
                                                      Transitivity.Explicit.value), concept_iterator_next))

    def get_owners(self, transaction: _Transaction,
                   annotations: Optional[set[Annotation]] = None) -> Iterator[Any]:
        annotations_array = [anno.native_object for anno in annotations] if annotations else []
        return (_ThingType.of(item) for item in Streamer(attribute_type_get_owners(
            self.native_transaction(transaction),
            self.native_object,
            Transitivity.Transitive.value,
            annotations_array,
        ), concept_iterator_next))

    def get_owners_explicit(self, transaction: _Transaction,
                            annotations: Optional[set[Annotation]] = None) -> Iterator[Any]:
        annotations_array = [anno.native_object for anno in annotations] if annotations else []
        return (_ThingType.of(item) for item in Streamer(attribute_type_get_owners(
            self.native_transaction(transaction),
            self.native_object,
            Transitivity.Explicit.value,
            annotations_array,
        ), concept_iterator_next))

    def put(self, transaction: _Transaction, value: Union[Value, bool, int, float, str, datetime]) -> Attribute:
        return attribute._Attribute(attribute_type_put(self.native_transaction(transaction), self.native_object,
                                                       _Value.of(value).native_object))

    def get(self, transaction: _Transaction, value: Union[Value, bool, int, float, str, datetime]) -> Optional[Attribute]:
        print(f"get: {self}, {value}, {_Value.of(value)}")
        print(attribute_type_get(self.native_transaction(transaction), self.native_object, _Value.of(value).native_object), flush=True)
        if res := attribute_type_get(self.native_transaction(transaction), self.native_object, _Value.of(value).native_object):
            return attribute._Attribute(res)
        return None

    def get_regex(self, transaction: _Transaction) -> str:
        return attribute_type_get_regex(self.native_transaction(transaction), self.native_object)

    def set_regex(self, transaction: _Transaction, regex: str) -> None:
        attribute_type_set_regex(self.native_transaction(transaction), self.native_object, regex)

    def unset_regex(self, transaction: _Transaction) -> None:
        attribute_type_unset_regex(self.native_transaction(transaction), self.native_object)
