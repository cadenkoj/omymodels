from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Column:
    name: str
    type: str
    default: Optional[str] = None
    nullable: bool = False
    size: Optional[int] = None
    primary_key: bool = False
    unique: bool = False
    references: Optional[dict] = None


@dataclass
class TableMeta:
    name: str
    columns: List[Column]
    primary_key: List[str]
    indexes: Optional[List[str]] = None
    constraints: Optional[dict] = None
    table_schema: Optional[str] = None

@dataclass
class Type:
    name: str
    base_type: str
    parents: Optional[List[str]]
    properties: Optional[dict]
    attrs: Optional[List[dict]]