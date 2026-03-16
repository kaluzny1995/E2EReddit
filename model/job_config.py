import json
from pydantic import BaseModel


class JobTypeConfig(BaseModel):
    folder_name: str
    conda_env: str
    python_script: str

    def get_command_pattern_string(self) -> str:
        return f"cd ..;cd {self.folder_name};conda run -n {self.conda_env} python {self.python_script}"


class JobConfig(BaseModel):
    max_checked_blank_lines: int
    max_logged_blank_lines: int
    download: JobTypeConfig
    ingestion: JobTypeConfig
    etl: JobTypeConfig

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_config():
        """ Returns a JobConfig instance from the config file """
        with open("config.json", "r") as f:
            return JobConfig(**json.load(f)['job'])
