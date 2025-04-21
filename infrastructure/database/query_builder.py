from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlalchemy.sql import ColumnElement
from sqlalchemy.orm import DeclarativeMeta
from typing import Type, List, Any


class QueryBuilder:
    def __init__(self, model: Type[DeclarativeMeta]):
        self.model = model
        self._filters: List[ColumnElement] = []
        self._relations: List[Any] = []
        self._order_by: List[Any] = []
        self._limit: int | None = None
        self._offset: int | None = None
        self._columns: List[Any] = []


    def filter(self, condition: ColumnElement) -> "QueryBuilder":
        self._filters.append(condition)
        return self

    def join_relation(
        self,
        relation_attr: Any,
        related_model: Type[DeclarativeMeta],
        filter_condition: ColumnElement = None
    ) -> "QueryBuilder":
        self._relations.append({
            "relation": relation_attr,
            "model": related_model,
            "filter": filter_condition
        })
        return self

    def order_by(self, *columns) -> "QueryBuilder":
        self._order_by.extend(columns)
        return self

    def limit(self, value: int) -> "QueryBuilder":
        self._limit = value
        return self

    def offset(self, value: int) -> "QueryBuilder":
        self._offset = value
        return self

    def build(self):

        stmt = select(self.model)

        for f in self._filters:
            stmt = stmt.where(f)

        for col in self._order_by:
            stmt = stmt.order_by(col)

        if self._limit is not None:
            stmt = stmt.limit(self._limit)

        if self._offset is not None:
            stmt = stmt.offset(self._offset)

        options = []
        for rel in self._relations:
            options.append(selectinload(rel["relation"]))
            if rel["filter"] is not None:
                options.append(with_loader_criteria(rel["model"], rel["filter"]))

        return stmt.options(*options)