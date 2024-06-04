import logging
import re

import functions_framework
from flask import Request


@functions_framework.http
def hello_http(request: Request):
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

    filename = request.files.get('files').filename
    logging.debug(f"Received a {request.method} request with {filename=}")
    client_name = filename.split("_")[0]
    args = re.findall(r"(\d+)", filename)
    print(filename)
    print(args)
    print(client_name)
    print(request.form)
    return {}
