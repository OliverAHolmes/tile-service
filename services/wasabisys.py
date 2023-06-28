import logging, io
import boto3
import cv2
import numpy as np
from botocore.exceptions import ClientError
from PIL import Image

s3 = boto3.resource(
    "s3",
    endpoint_url="https://s3.ap-southeast-2.wasabisys.com",
    aws_access_key_id="2P801GRW1DVXZXRTE6NY",
    aws_secret_access_key="XuDYIb8rdl3fGH4SeKvBCyM7QDEzmebXukpqlNFK",
)


def enhance_image(image):
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
    try:
        # Get bucket object
        s3.Bucket(bucket_name).put_object(Key=key_name, Body=file_obj)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_image(key_name, bucket_name, enhance=False, overlay=False):
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
    try:
        s3.Object(bucket_name, key_name).load()
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("The object does not exist.")
        else:
            return False
    else:
        return True
