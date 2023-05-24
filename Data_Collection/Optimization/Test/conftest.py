from datetime import datetime
import logging
import os


import boto3
import pytest

from utils import prepare_stacks, cleanup_stacks

logger = logging.getLogger(__name__)
_start_time = None


@pytest.fixture(scope='session')
def athena():
    return boto3.client('athena')


@pytest.fixture(scope='session')
def cloudformation():
    return boto3.client('cloudformation') 


@pytest.fixture(scope='session')
def s3():
    return boto3.resource('s3')


@pytest.fixture(scope='session')
def account_id():
    return boto3.client("sts").get_caller_identity()["Account"]


@pytest.fixture(scope='session')
def bucket():
    return os.environ.get('BUCKET', "aws-wa-labs-staging")


@pytest.fixture(scope='session')
def start_time():
    global _start_time
    if _start_time is None:
        _start_time = datetime.now()
    
    return _start_time


@pytest.fixture(scope='session', autouse=True)
def prepare_setup(athena, cloudformation, s3, account_id, bucket, start_time):
    yield prepare_stacks(cloudformation=cloudformation, account_id=account_id, bucket=bucket, s3=s3)
    cleanup_stacks(cloudformation=cloudformation, account_id=account_id, s3=s3, athena=athena)
