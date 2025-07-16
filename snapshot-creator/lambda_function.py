# This function creates EBS snapshots for all volumes and stores logs in: s3://Snapshot-creation/

import boto3
import datetime
import logging
import os
import json

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    log_entries = []
    volumes = ec2.describe_volumes()['Volumes']

    for volume in volumes:
        vol_id = volume['VolumeId']
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')
        description = f"Snapshot created by Lambda at {timestamp}"

        try:
            snapshot = ec2.create_snapshot(
                VolumeId=vol_id,
                Description=description,
                TagSpecifications=[
                    {
                        'ResourceType': 'snapshot',
                        'Tags': [
                            {'Key': 'CreatedBy', 'Value': 'Lambda'},
                            {'Key': 'VolumeId', 'Value': vol_id}
                        ]
                    }
                ]
            )
            msg = f"✅ Snapshot {snapshot['SnapshotId']} created for volume {vol_id}"
            log_entries.append(msg)
            logger.info(msg)

        except Exception as e:
            error_msg = f"❌ Failed to create snapshot for {vol_id}: {str(e)}"
            log_entries.append(error_msg)
            logger.error(error_msg)

    # Upload logs to S3
    try:
        bucket_name = os.environ.get("S3_BUCKET_NAME", "lambda-snapshot-logs-2112")
        key_name = f"Snapshot-creation/snapshot-creator-{context.aws_request_id}.log"
        s3.put_object(
            Bucket=bucket_name,
            Key=key_name,
            Body="\n".join(log_entries).encode('utf-8')
        )
        logger.info(f"Logs successfully uploaded to s3://{bucket_name}/{key_name}")
    except Exception as e:
        logger.error(f"❌ Failed to upload logs to S3: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Snapshot creation complete.')
    }
