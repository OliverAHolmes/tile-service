from pathlib import Path

from uuid import uuid4
GDAL_DATASET = gdal.Dataset
import boto3
from pydantic import BaseSettings
from osgeo import gdal

class S3Configuration(BaseSettings):
    """
    S3 configuration class
    """
    s3_access_key_id: str = ''
    s3_secret_access_key: str = ''
    s3_region_name: str = ''
    s3_endpoint_url: str = ''
    s3_bucket_name: str = ''
    s3_use: bool = False

S3_CONF = S3Configuration()
S3_STR = 's3'
S3_SESSION = boto3.session.Session()
S3 = S3_SESSION.resource(
    service_name=S3_STR,
    aws_access_key_id=S3_CONF.s3_access_key_id,
    aws_secret_access_key=S3_CONF.s3_secret_access_key,
    endpoint_url=S3_CONF.s3_endpoint_url,
    region_name=S3_CONF.s3_region_name,
    use_ssl=True,
    verify=True,
)
BUCKET = S3_CONF.s3_bucket_name
ZIP_EXT = '.zip'


def get_gdal_data(file_path: Path, s3_use: S3_CONF.s3_use) -> GDAL_DATASET:
    """
    Retrieves the tif content with gdal from the passed file_path. Do so either locally or from S3
    """
    if s3_use:
        return get_in_memory_tile(get_s3_object(file_path))
    return get_tif_tile(file_path)


def get_s3_object(file_path: Path) -> bytes:
    """
    Retrieve as bytes the content associated to the passed file_path
    """
    return S3.Object(bucket_name=BUCKET, key=forge_key(file_path)).get()['Body'].read()


def forge_key(file_path: Path) -> str:
    """
    Edit this code at your convenience to forge the bucket key out of the passed file_path
    """
    return str(file_path.relative_to(*file_path.parts[:2]))


def get_tif_tile(file_path):
    """
    Retrieves tif content with gdal from local file
    """
    return gdal.Open(str(file_path))

def get_in_memory_tile(in_memory_data: bytes):
    """
     Retrieves tif content with gdal from vsimem
    """
    filename = _in_memory_filename()
    gdal.FileFromMemBuffer(filename, in_memory_data)
    tile = gdal.Open(filename)
    unlinked = gdal.Unlink(filename)
    return tile

def _in_memory_filename():
    """
    Generate a random unique name to avoid concurrent accesses if multiple reading from vsimem
    """
    return f'/vsimem/{get_new_uuid()}'


def get_new_uuid() -> str:
    """
    Generate uuid4 strings
    """
    return str(uuid4())