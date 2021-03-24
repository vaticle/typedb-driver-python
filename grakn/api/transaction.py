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

import enum
from abc import ABC, abstractmethod
from typing import Iterator

import grakn_protocol.common.transaction_pb2 as transaction_proto

from grakn.api.concept.concept_manager import ConceptManager
from grakn.api.logic.logic_manager import LogicManager
from grakn.api.options import GraknOptions
from grakn.api.query.future import QueryFuture
from grakn.api.query.query_manager import QueryManager


class GraknTransaction(ABC):

    @abstractmethod
    def is_open(self) -> bool:
        pass

    @abstractmethod
    def transaction_type(self) -> "Type":
        pass

    @abstractmethod
    def options(self) -> GraknOptions:
        pass

    @abstractmethod
    def concepts(self) -> ConceptManager:
        pass

    @abstractmethod
    def logic(self) -> LogicManager:
        pass

    @abstractmethod
    def query(self) -> QueryManager:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    class Type(enum.Enum):
        READ = 0
        WRITE = 1

        def is_read(self):
            return self is GraknTransaction.Type.READ

        def is_write(self):
            return self is GraknTransaction.Type.WRITE

        def proto(self):
            return transaction_proto.Transaction.Type.Value(self.name)


class _GraknTransactionExtended(GraknTransaction, ABC):

    @abstractmethod
    def execute(self, request: transaction_proto.Transaction.Req) -> transaction_proto.Transaction.Res:
        pass

    @abstractmethod
    def run_query(self, request: transaction_proto.Transaction.Req) -> QueryFuture[transaction_proto.Transaction.Res]:
        pass

    @abstractmethod
    def stream(self, request: transaction_proto.Transaction.Req) -> Iterator[transaction_proto.Transaction.ResPart]:
        pass
