import boto3
import functools
from src.cloudhive.logger import Logger

logger = Logger.get_logger(f"cloud{__file__}")
logger.set_level("debug")

FORCE = False

class CustomException(Exception):
    """Base exception class."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.body = message
        self.statusCode = status_code

    def dispatch(self) -> dict:
        return {"statusCode": self.statusCode, "body": self.body}


class ArgumentMissingError(CustomException):
    def __init__(self, message):
        super().__init__(message)


def retry_with_fallback(client=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
                return response
            except Exception as e:
                logger.debug(f"Falling into the fallback client for the '{func.__name__}'")
                return getattr(client, func.__name__)(*args, **kwargs)

        return wrapper

    return decorator


def missing_args_error(msg="Some Argument are missing from the function."):
    logger.error(msg)
    if not FORCE:
        raise ArgumentMissingError(msg)
    return None

class BaseS3client:
    _fallback_client = boto3.client("s3")

    def __init__(self):
        self._client = boto3.client("ec2")

    @retry_with_fallback(_fallback_client)
    def list_objects_v2(self, Bucket, Prefix):
        return self._client.list_objects_v2(Bucket=Bucket, Prefix=Prefix)

    @retry_with_fallback(_fallback_client)
    def upload_file(self, file_path, dest_bucket, dest_file):
        return self._client.upload_file(file_path, dest_bucket, dest_file)

    @retry_with_fallback(_fallback_client)
    def download_file(self, bucket: str, key: str, output_file: str):
        return self._client.download_file(bucket, key, output_file)


class S3Util(BaseS3client):
    def download(self, bucket, key, output_file):
        if not all([bucket, key, output_file]):
            return missing_args_error()

        return super().download_file(bucket, key, output_file)

    def list_object(self, bucket=None, prefix=None):
        if not bucket:
            return missing_args_error()

        if not prefix:
            prefix = ""

        response = super().list_objects_v2(Bucket=bucket, Prefix=prefix)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("The request is not done successfully!")

        if 'Contents' not in response:
            logger.debug(f"No files found in {bucket}/{prefix}")
            return []

        return response['Contents']

    def upload(self, file, bucket, dest_file):
        if not all([file, bucket, dest_file]):
            return missing_args_error()

        return super().upload_file(file, bucket, dest_file)

"""
>>> bc = S3Util()
>>> obj = bc.list_object()
>>> print(obj)

"""
