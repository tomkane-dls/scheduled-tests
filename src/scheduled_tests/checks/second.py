import os


def test_second():
    print(f"second check, job {os.environ.get('JOB_NAME', 'local')}")
