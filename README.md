# Cloud Functions for uploading data files to Google Cloud Storage

### Description
This repository presente the code for the cloud functions `UploadGenderSorting` and `UploadAcitivtyReports`.
These function are expected to receive a http `POST` request from Ewon with an attached `file` to be uploaded 
to the right place in the right bucket.


### Set up the repo
For local development and testing, clone the repo and then run:
```
python -m venv venv
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
functions-framework --target {upload_activity_reports or upload_gender_sorting} --debug 
```

# usage:
### The elements listed below are required for the both functions to run correctly:
- API method set to `POST`
- file attached to the form-data section of the API request
- the key of the attached file is "file"
- a valid API key passed in the query params with key "apikey"
- the endpoint's path is `HOST/{clientID}/{machineID}/{dd-mm-yyyy}/?apikey=YOUR_API_KEY` (example: `HOST/3328/PMAX-C02913/21-02-2024/?apikey=dzdaq3fescrr43vr54bf12`)


# TODOs
- analyse the date
- set up de l envoi cote Ewon
