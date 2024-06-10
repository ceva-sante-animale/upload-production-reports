import logging
import os
import time
from functools import lru_cache
from typing import List

import functions_framework
import google.cloud.storage
from flask import Request
from google.cloud import firestore
from google.cloud.storage import Client

is_production = bool(os.environ.get("PORT"))

if not is_production:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
BUCKET_NAME = "ecat_id_test"
bucket = Client().bucket(BUCKET_NAME)


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


# cache will be updated once in an hour
@lru_cache()
def get_api_keys(ttl_hash=None) -> List[str]:
    logging.debug(f"Loading api keys from Firestore and cache it for one hour ...")
    store = firestore.Client()
    ref = store.collection("apikey")
    return [doc.get().get("apikey") for doc in ref.list_documents()]


@functions_framework.http
def upload_file(request: Request):
    """HTTP Cloud Function that takes care of uploading Gender Sorting feature files to GC storage
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    keys = get_api_keys(ttl_hash=get_ttl_hash())
    apikey = request.args.get('apikey')
    if apikey not in keys:
        error = f"Received a {request.method=} request with a missing or incorrect api key..."
        logging.error(error)
        return {"error": error}, 401

    file = request.files.get('file')
    if request.method.lower() != "post":
        error = f"Received a {request.method} request, but we only accept POST requests"
        logging.error(error)
        return {"error": error}, 405

    if not file:
        error = f"Received a {request.method} request with no file attached..."
        logging.error(error)
        return {"error": error}, 400

    metadata = [name for name in request.path.split("/") if name]
    if len(metadata) != 3 or len(metadata[-1].split("-")) != 3:
        error = (
            f"The request url must include exactly the client id, machine code and date following this format "
            f"'/client_id/machine_code/date[dd-mm-yyyy]/' (/3328/PMXA-C32432/22-05-2024/) "
            f"but the provided path is {request.path}"
        )
        logging.error(error)
        return {"error": error}, 400

    [client_id, machine_code, date] = metadata
    [d, m, y] = date.split("-")
    try:
        blob: google.cloud.storage.Blob = bucket.blob(f"{client_id}/{machine_code}/{y}/{m}/{d}/{file.filename}")
        blob.upload_from_file(file)
        logging.debug(
            f"Successfully upload file {file.filename=} ({blob.size=} bytes) for {client_id=} {machine_code=} {date=}"
        )
        return {"success": True}, 201
    except Exception as exc:
        logging.error(
            f"Not able to upload file {file.filename=} for {client_id=} {machine_code=} {date=}"
        )
        logging.error(f"Error returned by GC storage: {str(exc)}")
        return {"success": False}, 400
