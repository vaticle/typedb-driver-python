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
from typing import Iterator, Any, TYPE_CHECKING

from typedb.api.concept.thing.relation import Relation
from typedb.api.concept.type.role_type import RoleType
from typedb.common.streamer import Streamer
from typedb.concept.thing.thing import _Thing
from typedb.concept.type.relation_type import _RelationType
from typedb.concept.type.role_type import _RoleType
from typedb.typedb_client_python import relation_get_type, relation_add_role_player, relation_remove_role_player, \
    relation_get_players_by_role_type, relation_get_role_players, role_player_get_role_type, \
    role_player_get_player, relation_get_relating, concept_iterator_next, role_player_iterator_next

if TYPE_CHECKING:
    from typedb.api.concept.thing.thing import Thing
    from typedb.connection.transaction import _Transaction


class _Relation(Relation, _Thing):

    def get_type(self) -> _RelationType:
        return _RelationType(relation_get_type(self.native_object))

    def add_player(self, transaction: _Transaction, role_type: _RoleType, player: _Thing) -> None:
        relation_add_role_player(self.native_transaction(transaction), self.native_object,
                                 role_type.native_object, player.native_object)

    def remove_player(self, transaction: _Transaction, role_type: _RoleType, player: _Thing) -> None:
        relation_remove_role_player(self.native_transaction(transaction), self.native_object,
                                    role_type.native_object, player.native_object)

    def get_players_by_role_type(self, transaction: _Transaction, *role_types: _RoleType) -> Iterator[Any]:
        native_role_types = [rt.native_object for rt in role_types]
        return (_Thing.of(item) for item in Streamer(relation_get_players_by_role_type(self.native_transaction(transaction),
                                                                                       self.native_object, native_role_types), concept_iterator_next))

    def get_players(self, transaction: _Transaction) -> dict[RoleType, list[Thing]]:
        role_players = {}
        for role_player in Streamer(relation_get_role_players(self.native_transaction(transaction), self.native_object), role_player_iterator_next):
            role = _RoleType(role_player_get_role_type(role_player))
            player = _Thing.of(role_player_get_player(role_player))
            role_players.setdefault(role, [])
            role_players[role].append(player)
        return role_players

    def get_relating(self, transaction: _Transaction) -> Iterator[_RoleType]:
        return (_RoleType(item) for item in Streamer(relation_get_relating(self.native_transaction(transaction), self.native_object), concept_iterator_next))
