# pdx-cs-ask
Source code for the "Ask the CS department a question" site at https://askcs.oregonctf.org

## Cloud Run instructions for https://askcs.oregonctf.org
* gcloud builds submit --timeout=900   --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/pdx-cs-ask
* gcloud run deploy pdx-cs-ask --image gcr.io/${GOOGLE_CLOUD_PROJECT}/pdx-cs-ask --service-account <FMI> --region=us-central1 --allow-unauthenticated --min-instances 1
* gcloud beta run domain-mappings create --service pdx-cs-ask --region us-central1 --domain askcs.oregonctf.org

## Have a GCP project?
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
