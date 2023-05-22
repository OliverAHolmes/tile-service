import os
from osgeo import gdal
import boto3
import urllib.request

# gdal.SetConfigOption('AWS_REGION', 'ap-southeast-2')
# gdal.SetConfigOption('AWS_ACCESS_KEY_ID', '4H0AFGBWJTWR82RWIWJA')
# gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', '8qeBzEJlNZWhzl9771nY3dl7sibFR2v8RrjD5XUG')
# gdal.SetConfigOption('AWS_S3_ENDPOINT', 'https://s3.ap-southeast-2.wasabisys.com') 

session = boto3.Session(
    aws_access_key_id='4H0AFGBWJTWR82RWIWJA',
    aws_secret_access_key='8qeBzEJlNZWhzl9771nY3dl7sibFR2v8RrjD5XUG',
    region_name='ap-southeast-2'
)

# Create S3 client with the desired endpoint
s3_client = session.client('s3', endpoint_url='https://s3.ap-southeast-2.wasabisys.com')


# Specify the S3 bucket and file path
bucket_name = 'anditi-docs'
file_path = 'output_cog_test.tif'

# Generate a pre-signed URL for the file
presigned_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': file_path},
    ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
)

vsicurl_url = '/vsicurl_streaming/{}'.format(presigned_url)


# Read the stream with GDAL
open_file = gdal.Open(vsicurl_url, gdal.GA_ReadOnly)

# # Open the file from S3 for reading
# open_file = gdal.Open(s3_uri, gdal.GA_ReadOnly)

# Perform operations on the opened file
# ...

# Close the file
open_file = None

#"/vsicurl/http://s3.eu-central-1.wasabisys.com/eumap/lcv/lcv_landcover.hcl_lucas.corine.rf_p_30m_0..0cm_2019_eumap_epsg3035_v0.1.tif"

# from osgeo import gdal
# import numpy as np

# # These only need to be set if they're not already in the environment,
# # ~/.aws/config, or you're running on an EC2 instance with an IAM role.
# gdal.SetConfigOption('AWS_S3_ENDPOINT', 'https://s3.ap-southeast-2.wasabisys.com') 
# gdal.SetConfigOption('AWS_REGION', 'ap-southeast-2')
# gdal.SetConfigOption('AWS_ACCESS_KEY_ID', '4H0AFGBWJTWR82RWIWJA')
# gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', '8qeBzEJlNZWhzl9771nY3dl7sibFR2v8RrjD5XUG')


# # 'sentinel-pds' is the S3 bucket name
# path = '/vsicurl_streaming/https://s3.ap-southeast-2.wasabisys.com/anditi-docs/output_cog_test.tif'
# ds = gdal.Open(path)