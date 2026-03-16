import json
from typing import List
from pydantic import BaseModel


class CeleryTask(BaseModel):
    phrase: str
    hour: int
    minute: int
    name: str

class CeleryAppConfig(BaseModel):
    name: str
    username: str
    password: str
    host: str
    port: int
    tasks: List[CeleryTask]

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_config():
        """ Returns a CeleryAppConfig instance from the config file """
        with open("config.json", "r") as f:
            return CeleryAppConfig(**json.load(f)['celery_app'])

    def get_rabbitmq_broker_string(self) -> str:
        """ Returns a broker string of RabbitMQ service """
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}//"
