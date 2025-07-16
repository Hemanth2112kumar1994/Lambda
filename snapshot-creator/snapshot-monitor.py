
import boto3
import os
import logging
import datetime
import json

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    delete_flag = os.environ.get('DELETE_SNAPSHOTS', 'No')
    bucket_name = os.environ.get("S3_BUCKET_NAME", "lambda-snapshot-logs-2112")
    log_entries = []

    logger.info("Manual trigger or test run. Listing all snapshots.")

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    for snap in snapshots:
        snapshot_id = snap['SnapshotId']
        volume_id = snap.get('VolumeId', 'N/A')
        start_time = snap['StartTime']
        log_line = f"{snapshot_id} - Volume: {volume_id} - Time: {start_time}"
        log_entries.append(log_line)
        logger.info(log_line)

        if delete_flag.lower() == 'yes':
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                del_msg = f"🗑️ Deleted snapshot {snapshot_id}"
                log_entries.append(del_msg)
                logger.info(del_msg)
            except Exception as e:
                err_msg = f"❌ Failed to delete snapshot {snapshot_id}: {str(e)}"
                log_entries.append(err_msg)
                logger.error(err_msg)

    if delete_flag.lower() != 'yes':
        skip_msg = "Deletion skipped (DELETE_SNAPSHOTS=No)"
        log_entries.append(skip_msg)
        logger.info(skip_msg)

    # Upload logs to S3
    try:
        key = f"logs/snapshot-check-{context.aws_request_id}.txt"
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body="\n".join(log_entries).encode('utf-8')
        )
        logger.info(f"Logs uploaded to s3://{bucket_name}/{key}")
    except Exception as e:
        logger.error(f"❌ Failed to upload logs to S3: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps("Completed.")
    }
