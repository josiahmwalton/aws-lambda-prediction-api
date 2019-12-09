import base64
import boto3
import json
import os
import random

# Instantiate the Kinesis Data Stream client
kinesis_client = boto3.client('kinesis')

# Instantiant the Comprehend Medical client
comprehend_medical_client = boto3.client('comprehendmedical')

# Get the Kinesis stream name defined in the serverless.yml
kinesis_stream_name = os.environ['kinesisStreamName']


def write_kinesis_record(record, stream_name, partition_key):
    """Function to write a record to a kinesis data stream.
    
    Arguments:
        record (dict): Dictionary to key: value pairs
        stream_name (str): String representing an existing Kinesis Data Stream to write to
        partition_key (str): String value to represent the Kinesis partition key value.

    Returns:
        None
    
    """
    put_response = kinesis_client.put_record(
        StreamName = stream_name,
        Data = json.dumps(record),
        PartitionKey = partition_key
    )

def detect_entities(event, context):
    """Detect the medical entities in free form medical text"""

    # Define the initial lambda response body, providing the input request
    body = {
        "message": "",
        "input": event,
        "output": {}
    }

    # Extract the GET request parameters
    try:
        data = event["queryStringParameters"]
    except KeyError:
        body["message"] = "queryStringParameters not provided in request"
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }

        # Write to kinesis
        kinesis_record = {
            "message": body["message"],
            "event": event,
        }
        put_response = kinesis_client.put_record(
            StreamName = kinesis_stream_name,
            Data = json.dumps(kinesis_record),
            PartitionKey = "key1"
        )

        return response
        
    # Extract the diagnosis code
    try:
        notes = data["notes"]
    except KeyError:
        body["message"] = "Medical notes not provided"
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }

        # Write to kinesis
        kinesis_record = {
            "message": body["message"],
            "event": event
        }
        put_response = kinesis_client.put_record(
            StreamName = kinesis_stream_name,
            Data = json.dumps(kinesis_record),
            PartitionKey = "key1"
        )

        return response
        

    # Perform entity recognition on the free-form medical text
    # using Comprehend Medical
    result = comprehend_medical_client.detect_entities(Text = str(notes))
    entities = result['Entities']
    entities_list = [entity for entity in entities]

    # Generate the response body with the prediction
    body["message"] == "Function complete"
    body["output"] = {
        "notes": notes,
        "entities": entities_list
    }

    # Write to kinesis
    kinesis_record = {
        "message": body["message"],
        "event": event,
        "prediction": body["output"]
    }
    put_response = kinesis_client.put_record(
        StreamName = kinesis_stream_name,
        Data = json.dumps(kinesis_record),
        PartitionKey = "key1"
    )

    # Create the return response
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response