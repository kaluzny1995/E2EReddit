import pytest

from model import EJobType, CommandParams


@pytest.mark.parametrize("command, phrase, job_type, expected_command_string", [
    (CommandParams(), "corgi", EJobType.DOWNLOAD,
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\""),
    (CommandParams(start_date="2020-01-01", interval="y"), "corgi", EJobType.DOWNLOAD,
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\" -d=\"2020-01-01\" -i=\"y\""),
    (CommandParams(start_date="2020-01-01", interval="y", include_today=True, num_processes=4), "corgi", EJobType.DOWNLOAD,
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\" -d=\"2020-01-01\" -i=\"y\" --include_today --num_processes=4"),
    (CommandParams(), "corgi", EJobType.INGESTION,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_ingestion.py \"corgi\""),
    (CommandParams(batch_size=100, no_authors_load=True), "corgi", EJobType.INGESTION,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_ingestion.py \"corgi\" -b=100 --no_authors_load"),
    (CommandParams(), "corgi", EJobType.ETL_POPULARITY,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\""),
    (CommandParams(no_multiprocessing=True), "corgi", EJobType.ETL_POPULARITY,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\" --no_multiprocessing"),
    (CommandParams(skip_missing_dates=True, start_date="2020-01-01", interval="y", until_today=True), "corgi", EJobType.ETL_POPULARITY,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\" --skip_missing_dates -d=\"2020-01-01\" -i=\"y\" --until_today"),
    (CommandParams(), "corgi", EJobType.ETL_SENTIMENT,
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"sentiment\" \"corgi\"")
])
def test_parse_command(command: CommandParams, phrase: str, job_type: EJobType, expected_command_string: str) -> None:
    # Arrange
    # Act
    command_string = command.parse_command(phrase, job_type)

    # Assert
    assert command_string == expected_command_string
