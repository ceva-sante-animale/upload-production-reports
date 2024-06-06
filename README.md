### Set up the CF that handles uploading sexage files from Ewon to GC storage
For local development and testing, clone the repo and then run:
```
python -m venv venv
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
functions-framework --target upload_file --debug 
```

## CF usage:
### The elements listed below are required for the CF to run correctly:
- API method set to POST
- file attached to the form-data section of the API request
- the key of the attached file is "file"
- a valid API key passed in the query params with key "apikey"
- the endpoint's path is `HOST/{clientID}/{machineID}/{dd-mm-yyyy}/` (example: `HOST/3328/PMAX-C02913/21-02-2024/`)


## TODOs
- check API and validate
- return http status
- link github with CF deployment
- logs
- le bon bucket
- analyse the date
- set up de l envoi cote Ewon
- 
