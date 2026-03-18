from typing import Literal
from pydantic import BaseModel

from model import EJobType, JobConfig


class CommandParams(BaseModel):
    limit: int | None = None  # D
    batch_size: int | None = None  # ING, ETL
    skip_missing_dates: bool = False  # ETL
    start_date: str | None = None  # D, ETL
    interval: Literal["h", "d", "m", "y"] | None = None  # D, ETL
    no_authors_download: bool = False  # D
    no_authors_load: bool = False  # ING
    include_today: bool = False  # D
    until_today: bool = False  # ETL
    no_multiprocessing: bool = False  # D, ETL
    num_processes: int | None = None  # D, ETL

    def parse_command(self, phrase: str, job_type: EJobType) -> str:
        """ Parses the command from parameters and returns the command string """
        job_config = JobConfig.from_config()

        if job_type == EJobType.DOWNLOAD:
            command = f"{job_config.download.get_command_pattern_string()} \"{phrase}\""

            if self.limit is not None:
                command += f" -l={self.limit}"
            if self.start_date is not None:
                command += f" -d=\"{self.start_date}\""
            if self.interval is not None:
                command += f" -i=\"{self.interval}\""
            if self.no_authors_download:
                command += f" --no_authors_download"
            if self.include_today:
                command += f" --include_today"
            if self.no_multiprocessing:
                command += f" --no_multiprocessing"
            if self.num_processes is not None:
                command += f" --num_processes={self.num_processes}"

        elif job_type == EJobType.INGESTION:
            command = f"{job_config.ingestion.get_command_pattern_string()} \"{phrase}\""

            if self.batch_size is not None:
                command += f" -b={self.batch_size}"
            if self.no_authors_load:
                command += f" --no_authors_load"

        else:
            command = f"{job_config.etl.get_command_pattern_string()} \"{job_type.value.lower()}\" \"{phrase}\""

            if self.batch_size is not None:
                command += f" -b={self.batch_size}"
            if self.skip_missing_dates:
                command += f" --skip_missing_dates"
            if self.start_date is not None:
                command += f" -d=\"{self.start_date}\""
            if self.interval is not None:
                command += f" -i=\"{self.interval}\""
            if self.until_today:
                command += f" --until_today"
            if self.no_multiprocessing:
                command += f" --no_multiprocessing"
            if self.num_processes is not None:
                command += f" --num_processes={self.num_processes}"

        return command