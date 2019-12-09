import base64
import boto3
import json
import os
import random

# Instantiate the Kinesis Data Stream client
kinesis_client = boto3.client('kinesis')

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

def procedure_code(event, context):
    """Predict the procedure code for a diagnosis code."""

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
        dxcode = data["dxcode"]
    except KeyError:
        body["message"] = "Diagnosis code (dxcode) parameter not provided"
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
        

    # Generate a random procedure code
    random_proc_code = random.choices(["proc1", "proc2", "proc3"])

    # Generate the response body with the prediction
    body["message"] == "Function complete"
    body["output"] = {
        "dxcode": dxcode,
        "prcode": random_proc_code
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