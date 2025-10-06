import numpy as np
import cv2
import requests
import requests
import boto3
import uuid
from io import BytesIO
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from pathlib import Path
import os
from botocore import config

S3_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME', 'diymod')
S3_REGION = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
S3_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
S3_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


# def convert_image_to_opencv_from_url(image_url):
#     '''This method should take an image URL and convert it to a format.'''
#     try:
#         response = requests.get(image_url)
#         image_array = np.frombuffer(response.content, np.uint8)
#         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
#         return image
#     except Exception as e:
#         return None

# def convert_opencv_to_url(image, file_name):
#     '''This method should take an OpenCV object and convert it to an image.'''
#     try:
#         _, image_encoded = cv2.imencode('.jpg', image)
#         image_data = BytesIO(image_encoded.tobytes())
#         # Upload the image to S3
#         s3_client.upload_fileobj(
#             image_data,
#             S3_BUCKET,
#             file_name,
#             ExtraArgs={"ContentType": "image/jpeg"}
#         )
#         s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
#         return s3_url
    
    # except Exception as e:
    #     return None

class ImageConverterFromURL(ABC):
    @abstractmethod
    def convert(self, image_url):
        pass

class ImageConverterToURL(ABC):
    @abstractmethod
    def convert(self, image, file_name):
        pass

class OpenCVImageConverterFromURL(ImageConverterFromURL):
    def convert(self, image_url):
        '''This method should take an image URL and convert it to a format.'''
        try:
            response = requests.get(image_url)
            image_array = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            return None

class OpenCVImageConverterToURL(ImageConverterToURL):
    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client(
            "s3",
            region_name=S3_REGION,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )
    def convert(self, image, file_name):
        '''This method should take an OpenCV object and convert it to an image.'''
        try:
            _, image_encoded = cv2.imencode('.jpg', image)
            image_data = BytesIO(image_encoded.tobytes())
            # Upload the image to S3
            self.s3_client.upload_fileobj(
                image_data,
                S3_BUCKET,
                file_name,
                ExtraArgs={"ContentType": "image/jpeg"}
            )
            s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
            return s3_url
        
        except Exception as e:
            return None