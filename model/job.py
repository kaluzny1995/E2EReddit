import logging
import subprocess
import json
import datetime as dt
from pydantic import BaseModel
from typing import List

import util
from model import EJobType


class Job(BaseModel):
    phrase: str
    job_type: EJobType
    command: str
    is_failed_if_error: bool
    next_jobs: List['Job']

    class ConfigDict:
        frozen = True

    @staticmethod
    def _print_process_logs(process: subprocess.Popen, logger: logging.Logger):
        """ Prints out the specific process logs """
        line = process.stdout.readline().decode().strip()
        blank_lines_counter = 0
        while blank_lines_counter < 4:
            if line != "" or blank_lines_counter < 2:
                print(line)
                logger.info(line)
            if line == "":
                blank_lines_counter += 1
            else:
                blank_lines_counter = 0
            line = process.stdout.readline().decode().strip()

    @staticmethod
    def _print_process_errors(process: subprocess.Popen, logger: logging.Logger):
        print(f"Job encountered an error:")
        logger.error(f"Job encountered an error:")
        while (line := process.stderr.readline().decode().strip()) != "":
            print(line)
            logger.info(line)
        print()

    def run(self, logger: logging.Logger | None = None):
        """ Executes the job command """
        if logger is None:
            logger = util.setup_logger(name=f"e2e_reddits_{self.phrase}",
                                       log_file=f"logs/e2e_reddits/e2e_reddits_{self.phrase}_{dt.datetime.now().isoformat()}.log")

        print(f"Starting {self.job_type.value} job for \"{self.phrase}\".")
        logger.info(f"Starting {self.job_type.value} job for \"{self.phrase}\".")

        # run the command
        print(f"Executing command: {self.command}")
        logger.info(f"Executing command: {self.command}")
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        print(f"Job {self.job_type.value} for \"{self.phrase}\" output logs:")
        logger.info(f"Job {self.job_type.value} for \"{self.phrase}\" output logs:")

        Job._print_process_logs(process, logger=logger)
        process.wait()
        if process.returncode != 0:
            Job._print_process_errors(process, logger=logger)
            if self.is_failed_if_error:
                raise subprocess.CalledProcessError(returncode=process.returncode, cmd=self.command)

        print(f"Finished {self.job_type.value} job for \"{self.phrase}\". Return code: {process.returncode}.\n")
        logger.info(f"Finished {self.job_type.value} job for \"{self.phrase}\". Return code: {process.returncode}.")

        # run the next jobs
        for next_job in self.next_jobs:
            next_job.run(logger=logger)

    @staticmethod
    def from_config(phrase: str):
        """ Returns a Job instance from the config file """
        with open("config.json", "r") as f:
            return Job(**json.load(f)['jobs'][phrase])
