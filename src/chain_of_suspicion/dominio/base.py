from pydantic import BaseModel, ConfigDict


class ModeloBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
