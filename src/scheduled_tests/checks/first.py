import os


def test_first():
    print(f"first check, job {os.environ.get('JOB_NAME', 'local')}")
