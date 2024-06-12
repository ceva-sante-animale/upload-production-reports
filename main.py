import logging

import functions_framework
from flask import Request
from google.cloud.storage import Blob

from utils import validate_request, pr_bucket, gs_bucket

logging.basicConfig(level=logging.DEBUG)


@functions_framework.http
def upload_activity_reports(request: Request):
    """HTTP Cloud Function that takes care of uploading activity reports files to GC storage
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    error, code = validate_request(request=request)
    if error is not None and code is not None:
        return error, code

    [client_id, machine_code, date] = [name for name in request.path.split("/") if name]
    [d, m, y] = date.split("-")
    file = request.files.get('file')
    try:
        blob: Blob = pr_bucket.blob(f"{client_id}/{machine_code}/{y}/{m}/{d}/{file.filename}")
        blob.upload_from_file(file)
        logging.debug(
            f"Successfully upload file {file.filename=} (bytes) for {client_id=} {machine_code=} {date=}"
        )
        return {"success": True}, 201
    except Exception as exc:
        logging.error(
            f"Not able to upload file {file.filename=} for {client_id=} {machine_code=} {date=}"
        )
        logging.error(f"Error returned by GC storage: {str(exc)}")
        return {"success": False}, 400


@functions_framework.http
def upload_gender_sorting(request: Request):
    """HTTP Cloud Function that takes care of uploading Gender Sorting files to GC storage
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    error, code = validate_request(request=request)
    if error is not None and code is not None:
        return error, code

    [client_id, machine_code, date] = [name for name in request.path.split("/") if name]
    [d, m, y] = date.split("-")
    file = request.files.get('file')
    try:
        blob: Blob = gs_bucket.blob(f"{client_id}/{machine_code}/{y}/{m}/{d}/{file.filename}")
        blob.upload_from_file(file)
        logging.debug(
            f"Successfully upload file {file.filename=} (bytes) for {client_id=} {machine_code=} {date=}"
        )
        return {"success": True, "url": blob.public_url}, 201
    except Exception as exc:
        logging.error(
            f"Not able to upload file {file.filename=} for {client_id=} {machine_code=} {date=}"
        )
        logging.error(f"Error returned by GC storage: {str(exc)}")
        return {"success": False}, 400
