import boto3
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']
        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Delete snapshot has id {snapshot_id} because of not attaching to any volumes")
        else:
            try:
                volume = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Delete snapshot has id {snapshot_id} because the volume attached is not attaching to any instance")
            except ec2.exceptions.ClientError as error:
                if error.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted snapshot has id {snapshot_id} because of not finding out any volume id is {volume_id}")
    