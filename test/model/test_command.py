import pytest

from model import EJobType, Command


@pytest.mark.parametrize("command, expected_command_string", [
    (Command(phrase="corgi", job_type=EJobType.DOWNLOAD),
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\""),
    (Command(phrase="corgi", job_type=EJobType.DOWNLOAD, start_date="2020-01-01", interval="y"),
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\" -d=\"2020-01-01\" -i=\"y\""),
    (Command(phrase="corgi", job_type=EJobType.DOWNLOAD, start_date="2020-01-01", interval="y", include_today=True, num_processes=4),
     "cd ..;cd DownloadReddit;conda run -n download_reddit_311 python run_download_reddits.py \"corgi\" -d=\"2020-01-01\" -i=\"y\" --include_today --num_processes=4"),
    (Command(phrase="corgi", job_type=EJobType.INGESTION),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_ingestion.py \"corgi\""),
    (Command(phrase="corgi", job_type=EJobType.INGESTION, batch_size=100, no_authors_load=True),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_ingestion.py \"corgi\" -b=100 --no_authors_load"),
    (Command(phrase="corgi", job_type=EJobType.ETL_POPULARITY),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\""),
    (Command(phrase="corgi", job_type=EJobType.ETL_POPULARITY, no_multiprocessing=True),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\" --no_multiprocessing"),
    (Command(phrase="corgi", job_type=EJobType.ETL_POPULARITY, skip_missing_dates=True, start_date="2020-01-01", interval="y", until_today=True),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"popularity\" \"corgi\" --skip_missing_dates -d=\"2020-01-01\" -i=\"y\" --until_today"),
    (Command(phrase="corgi", job_type=EJobType.ETL_SENTIMENT),
     "cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_etl.py \"sentiment\" \"corgi\"")
])
def test_parse_command(command: Command, expected_command_string: str) -> None:
    # Arrange
    # Act
    command_string = command.parse_command()

    # Assert
    assert command_string == expected_command_string
