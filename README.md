# pdx-cs-ask
Source code for the Portland State chatbot that scrapes the Drupal site at https://www.pdx.edu for content based on a path given to it.  The 'computer-science' version is currently running https://askcs.oregonctf.org.  The site relies on Google's embedding and large-language models to operate.  You must have a valid GOOGLE_API_KEY with access to Gemini APIs in order to build and run the service.

## Container building instructions

 1.  Set the PATH_NAME environment variable.  This is required for targeting the chatbot to a particular path within the site.  In the example below, we set it to 'computer-science' to crawl URLs with 'computer-science' in them.
`export PATH_NAME="computer-science"`
 2.  Set the GOOGLE_API_KEY environment variable.  This is required for building the container in order to embed the documents into the vector database.
`export GOOGLE_API_KEY="..."`
 3. Build the container.  `gcloud builds submit` does not support passing environment variables in the build so use the Docker CLI to pass the API key in as an environment variable upon building.  Note that this is a multi-stage build and the key is only used to construct the    database.  The final database is copied to the final container, but not the key.
`docker build --build-arg PATH_NAME=$PATH_NAME --build-arg GOOGLE_API_KEY=$GOOGLE_API_KEY -f Dockerfile -t wuchangfeng/pdx-cs-ask .`   
 4. Login to DockerHub
 `docker login`
 5. Push container image
 `docker push wuchangfeng/pdx-cs-ask`

## Container deployment instructions
### Local deployment
`docker run -it --rm -p 8000:8000 -e PORT=8000 -e GOOGLE_API_KEY=${GOOGLE_API_KEY} wuchangfeng/pdx-cs-ask`

### Cloud Run deployment

 1. Deploy container
`gcloud run deploy pdx-cs-ask --image wuchangfeng/pdx-cs-ask --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY}" --region=us-central1 --allow-unauthenticated --min-instances 1`
 2. Create mapping for the site
`gcloud beta run domain-mappings create --service pdx-cs-ask --region us-central1 --domain askcs.oregonctf.org`

## Have a GCP project?
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
