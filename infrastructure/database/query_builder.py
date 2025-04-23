from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlalchemy.sql import ColumnElement
from sqlalchemy.orm import DeclarativeMeta
from typing import Type, List, Any, Literal, Union


class ConditionGroup:
    def __init__(self, mode: Literal["and", "or"] = "and"):
        self.conditions: List[Union[ColumnElement, "ConditionGroup"]] = []
        self.mode: Literal["and", "or"] = mode

    def filter(self, condition: Union[ColumnElement, "ConditionGroup"]) -> "ConditionGroup":
        self.conditions.append(condition)
        return self
    
    def filter_all(self, *conditions: Union[ColumnElement, "ConditionGroup"]) -> "ConditionGroup":
        self.conditions.extend(conditions)
        return self

    def and_(self) -> "ConditionGroup":
        self.mode = "and"
        return self

    def or_(self) -> "ConditionGroup":
        self.mode = "or"
        return self

    def build(self):
        built_conditions = [
            cond.build() if isinstance(cond, ConditionGroup) else cond
            for cond in self.conditions
        ]
        if self.mode == "and":
            return and_(*built_conditions)
        return or_(*built_conditions)


class QueryBuilder:
    def __init__(self, model: Type[DeclarativeMeta]):
        self.model = model
        self._filters: List[Union[ColumnElement, ConditionGroup]] = []
        self._relations: List[dict[str, Any]] = []
        self._order_by: List[Any] = []
        self._limit: int | None = None
        self._offset: int | None = None

    @staticmethod
    def group(mode: Literal["and", "or"] = "and") -> ConditionGroup:
        return ConditionGroup(mode)
    
    @staticmethod
    def or_(*conditions: Union[ColumnElement, ConditionGroup]) -> ConditionGroup:
        return ConditionGroup("or").filter_all(*conditions)

    @staticmethod
    def and_(*conditions: Union[ColumnElement, ConditionGroup]) -> ConditionGroup:
        return ConditionGroup("and").filter_all(*conditions)


    def filter(self, condition: Union[ColumnElement, ConditionGroup]) -> "QueryBuilder":
        self._filters.append(condition)
        return self

    def join_relation(
        self,
        relation_attr: Any,
        related_model: Type[DeclarativeMeta],
        filter_condition: Union[ColumnElement, ConditionGroup, None] = None,
        load_relation: bool = True  # Ajout d'un paramètre pour contrôler le préchargement
    ) -> "QueryBuilder":
        if isinstance(filter_condition, ConditionGroup):
            filter_condition = filter_condition.build()

        self._relations.append({
            "relation": relation_attr,
            "model": related_model,
            "filter": filter_condition,
            "load_relation": load_relation  # Indicateur de préchargement
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
        # Requête principale
        stmt = select(self.model)

        # Filtres principaux
        for f in self._filters:
            stmt = stmt.where(f.build() if isinstance(f, ConditionGroup) else f)

        # Tri, limite, offset
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        if self._limit is not None:
            stmt = stmt.limit(self._limit)
        if self._offset is not None:
            stmt = stmt.offset(self._offset)

        # Chargement des relations avec filtres
        options = []
        for rel in self._relations:
            if rel["load_relation"]:
                options.append(selectinload(rel["relation"]))  # Précharge la relation
            if rel["filter"] is not None:
                options.append(with_loader_criteria(rel["model"], rel["filter"], include_aliases=True))


        return stmt.options(*options)
