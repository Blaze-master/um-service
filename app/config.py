from pydantic_settings import BaseSettings
from pathlib import Path
import json


class Settings(BaseSettings):

    model_api_key : str
    model_name : str
    model_provider : str
    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def intervention_ids(self):
        pathm = Path("app/data/intervention_ids.json")
        with open(pathm, "r") as f:
            return json.load(f)




def get_settings():
    return Settings()