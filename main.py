import logging
import re
import os
from functools import cache

import functions_framework
from flask import Request
from google.cloud.storage import Client


@cache
def get_gcs_client() -> Client:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    return Client()


BUCKET_NAME = "ecat_id_test"
storage = get_gcs_client()
bucket = storage.bucket(BUCKET_NAME)


@functions_framework.http
def upload_file(request: Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    if not request.files.get('files'):
        logging.error(f"Received a {request.method} request with no file attached...")

    file = request.files.get('files')
    filename = file.filename
    logging.debug(f"Received a {request.method} request with {filename=}")
    client_name = filename.split("_")[0]
    args = re.findall(r"(\d+)", filename)
    upload_to_bucket(file)
    print(filename)
    print(args)
    print(client_name)
    print(request.form)

    return {}


def upload_to_bucket(file):
    """ Upload data to a bucket"""
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
