# aws-lambda-prediction-api

Code relating to the creation of a API to make predictions for procedure code, based on a diagnosis code. 

API will be created using a combination of a couple of AWS services:

* AWS Lambda: lambda functions to perform standard RESTful API calls
* AWS API Gateway: creation of externally-accessible URLs to make HTTP requests against
* AWS S3: robust object/file storage service to store our predictive model
* AWS Kinesis: streaming service to capture all predictions that were made/requested

## Getting Started 
------------------

