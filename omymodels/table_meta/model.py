from pydantic import field_validator, model_validator, ConfigDict, BaseModel, Field
from typing import List, Optional, Union, Dict, Tuple


class ColumnBase(BaseModel):
    name: str
    type: str
    size: Optional[Union[str, int, Tuple]] = None


class HQLProperties(BaseModel):

    clustered_by: Optional[List] = None
    location: Optional[str] = None
    external: Optional[bool] = None
    row_format: Optional[str] = None
    fields_terminated_by: Optional[str] = None
    lines_terminated_by: Optional[str] = None
    map_keys_terminated_by: Optional[str] = None
    collection_items_terminated_by: Optional[str] = None
    stored_as: Optional[str] = None


class TableProperties(HQLProperties):

    indexes: Optional[List] = None
    alter: Optional[List] = None
    tablespace: Optional[str] = None
    partitioned_by: Optional[List[ColumnBase]] = None
    if_not_exists: Optional[bool] = None


class Column(ColumnBase):

    primary_key: bool = False
    unique: bool = False
    default: Optional[str] = None
    nullable: bool = True
    identifier: Optional[bool] = None
    generated_as: Optional[str] = None
    properties: Optional[Dict] = None
    references: Optional[Dict] = None
    foreign_key: Optional[str] = None
    comment: Optional[str] = None

    @field_validator("size")
    @classmethod
    def size_must_contain_space(cls, v):
        if isinstance(v, str) and v.isnumeric():
            return int(v)
        return v


class TableMeta(BaseModel):
    name: str = Field(alias="table_name")
    field_schema: Optional[str] = Field(None, alias="schema")
    dataset: Optional[str] = None
    columns: List[Column]
    indexes: Optional[List[Dict]] = Field(None, alias="index")
    alter: Optional[Dict] = {}
    checks: Optional[List[Dict]] = None
    properties: Optional[TableProperties] = None
    primary_key: List
    parents: Optional[List[str]] = None
    project: Optional[str] = None

    @property
    def table_schema(self):
        return self.field_schema or self.dataset

    @model_validator(mode="before")
    @classmethod
    def set_properties(cls, values: Dict):
        properties = {}
        for key, value in values.items():
            if key not in TableMeta.model_fields:
                properties[key] = value
        if not values.get("properties"):
            values["properties"] = {}
        values["properties"].update(properties)

        return values
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Type(BaseModel):
    name: str = Field(alias="type_name")
    base_type: str
    parents: Optional[List[str]] = None
    properties: Optional[Dict] = None
    attrs: Optional[List[Dict]] = None