# udacity-cs253
CS253 Web Development revamp

## Homework 1

* Google App Engine project name: [milanoid-cs253](https://console.cloud.google.com/iam-admin/iam/project?project=milanoid-cs253)
* Google Cloud deploy url: https://milanoid-cs253.appspot.com/
* Github: https://github.com/milanoid/udacity-cs253

### Yak shaving

1. install Ubuntu version of [Google Cloud SKD](https://cloud.google.com/sdk/docs/#deb)
2. initialize Google Cloud: `sudo gcloud --project=milanoid-cs253 init`
3. test run the app locally: `gunicorn main:app` 
4. deploy the app to Google Cloud: `sudo gcloud app deploy`


