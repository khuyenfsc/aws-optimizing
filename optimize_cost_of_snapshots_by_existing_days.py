import boto3
from datetime import datetime, timezone
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']
        now = datetime.now(timezone.utc)
        days = (now - start_time).days
        if(days > 30):
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot has id is {snapshot_id} because of being over 30 days")
