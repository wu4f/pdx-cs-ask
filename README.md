# pdx-cs-ask
Source code for the "Ask the CS department a question" site at https://ask.oregonctf.org

## Cloud Run instructions for https://ask.oregonctf.org
* gcloud builds submit --timeout=900   --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/pdx-cs-ask
* gcloud run deploy pdx-cs-ask --image gcr.io/${GOOGLE_CLOUD_PROJECT}/pdx-cs-ask --service-account <FMI> --region=us-central1 --allow-unauthenticated --min-instances 1
* gcloud beta run domain-mappings create --service pdx-cs-ask --region us-central1 --domain ask.oregonctf.org
