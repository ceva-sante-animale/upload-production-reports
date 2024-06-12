import logging
import os
import time
from functools import lru_cache
from typing import List

from google.cloud.firestore import Client as Store
from google.cloud.storage import Client

is_production = bool(os.environ.get("PORT"))

if not is_production:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

PRODUCTION_REPORTS_BUCKET_NAME = "ecat_id_activity_report"
GENDER_SORTING_BUCKET_NAME = "ecat_id_test"
pr_bucket = Client().bucket(PRODUCTION_REPORTS_BUCKET_NAME)
gs_bucket = Client().bucket(GENDER_SORTING_BUCKET_NAME)


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


# cache will be updated once in an hour
@lru_cache()
def get_api_keys(ttl_hash=None) -> List[str]:
    logging.debug(f"Loading api keys from Firestore and cache it for one hour ...")
    store = Store()
    ref = store.collection("apikey")
    return [doc.get().get("apikey") for doc in ref.list_documents()]


def get_all_api_keys():
    return get_api_keys(ttl_hash=get_ttl_hash())


def validate_request(request):
    keys = get_all_api_keys()
    apikey = request.args.get('apikey')
    if apikey not in keys:
        error = f"Received a {request.method=} request with a missing or incorrect api key..."
        logging.error(error)
        return {"error": error}, 401
    if request.method.lower() != "post":
        error = f"Received a {request.method} request, but we only accept POST requests"
        logging.error(error)
        return {"error": error}, 405

    if not request.files.get('file'):
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
    return None, None
