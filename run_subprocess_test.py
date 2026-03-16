import shlex
import subprocess


def main():
    command = "echo Hello subprocess test!;cd ..;cd ETLReddit;conda run -n etl_reddit_311 python run_sentiment_example.py"

    subprocess_run = subprocess.run([command], capture_output=True, shell=True)

    print(subprocess_run.stdout.decode())
    print("Result code:", subprocess_run.returncode)
    print()

    subprocess_popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while (line := subprocess_popen.stdout.readline().decode().strip()) != "":
        print(line)

    subprocess_popen.wait()
    print("Result code:", subprocess_popen.returncode)
    if subprocess_popen.returncode != 0:
        print("\nSomething went wrong!")
        while (line := subprocess_popen.stderr.readline().decode().strip()) != "":
            print(line)


if __name__ == "__main__":
    main()
