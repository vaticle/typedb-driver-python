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
from abc import ABC, abstractmethod

from grakn.api.concept.thing.entity import Entity
from grakn.api.concept.type.thing_type import ThingType, RemoteThingType
from grakn.api.transaction import GraknTransaction


class EntityType(ThingType, ABC):

    def is_entity_type(self):
        return True

    @abstractmethod
    def as_remote(self, transaction: GraknTransaction) -> "RemoteEntityType":
        pass


class RemoteEntityType(RemoteThingType, EntityType, ABC):

    def create(self) -> Entity:
        pass
