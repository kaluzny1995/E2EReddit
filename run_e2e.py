import argparse
import datetime as dt

import util
from model import Job


def parse_args() -> argparse.Namespace:
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Reddits E2E process Python 3.11 application.")
    parser.add_argument("phrase", type=str, help="phrase to run the E2E process for")

    return parser.parse_args()


def main():
    args = parse_args()

    logger = util.setup_logger(name=f"e2e_{args.phrase}",
                               log_file=f"logs/e2e/{args.phrase}/e2e_{args.phrase}_{dt.datetime.now().isoformat()}.log")

    main_job = Job.from_config(args.phrase)
    main_job.run(logger=logger)


if __name__ == '__main__':
    main()
