from enum import Enum


class EJobType(str, Enum):
    DOWNLOAD = "DOWNLOAD"
    INGESTION = "INGESTION"
    ETL_POPULARITY = "ETL_POPULARITY"
    ETL_SENTIMENT = "ETL_SENTIMENT"
