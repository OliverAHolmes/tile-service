import logging, io, os
import boto3
import cv2
import numpy as np
from botocore.exceptions import ClientError
from PIL import Image
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.resource(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def enhance_image(image):
    """Function for balancing a tile image using a histogram equalization."""
    # Convert byte stream to byte array and load the image from the byte array
    arr = np.frombuffer(image.getvalue(), np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)  # Keep all color channels

    # Check if the image has an alpha channel
    if image.shape[2] == 4:
        # Split the image into color and alpha channels
        bgr = image[:, :, :3]  # Get the BGR channels
        alpha = image[:, :, 3]  # Get the alpha channel
    else:
        bgr = image

    # Convert the image to YUV color space
    image_yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)

    # Apply histogram equalization to the Y channel
    image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])

    # Convert the image back to BGR color space
    equalized_bgr = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

    # Convert BGR to RGBcv
    equalized_rgb = cv2.cvtColor(equalized_bgr, cv2.COLOR_BGR2RGB)

    # If there was an alpha channel, add it back to the result
    if image.shape[2] == 4:
        # Split equalized_image into three single channels
        r, g, b = cv2.split(equalized_rgb)
        # Merge the three single channels and the alpha channel
        equalized_image = cv2.merge([r, g, b, alpha])

        return_img = Image.fromarray(equalized_image, "RGBA")
    else:
        return_img = Image.fromarray(equalized_rgb, "RGB")

    # Open the image using Pillow
    return return_img


def upload_image(key_name, bucket_name, file_obj):
    """Function for uploading a tile image."""
    try:
        # Get bucket object
        s3.Bucket(bucket_name).put_object(Key=key_name, Body=file_obj)
    except ClientError as client_error:
        logging.error(client_error)
        return False
    return True


def download_image(key_name, bucket_name, enhance=False, overlay=False):
    """Function for downloading a tile image."""
    base_image = None
    overlay_image = Image.open("GeoNotesOverlay.png") if overlay else None

    try:
        byte_stream = io.BytesIO()
        s3.Bucket(bucket_name).download_fileobj(key_name, byte_stream)
        byte_stream.seek(0)  # Ensure you're at the start of the stream

        base_image = Image.open(byte_stream)
        if enhance:
            base_image = enhance_image(byte_stream)

    except ClientError as _e:
        base_image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    if base_image and overlay:
        base_image.paste(overlay_image, (0, 0), overlay_image)

    return base_image


def test_if_tile_exists(key_name, bucket_name):
    """Test if a tile image for key exists in the data store."""
    try:
        s3.Object(bucket_name, key_name).load()
    except ClientError as _client_error:
        return False
    else:
        return True
