import boto3
from datetime import datetime, timezone, timedelta

# Initialize the S3 client
s3 = boto3.client('s3')

# Bucket name
BUCKET_NAME = 'your-bucket-name'

# Time delta for 30 days
DAYS_OLD = 30
now = datetime.now(timezone.utc)
cutoff_date = now - timedelta(days=DAYS_OLD)

def delete_old_objects():
    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("No objects found in the bucket.")
        return

    deleted_objects = []

    for obj in response['Contents']:
        # Get the object's LastModified time
        last_modified = obj['LastModified']

        # If the object is older than the cutoff date
        if last_modified < cutoff_date:
            print(f"Deleting object: {obj['Key']}")
            s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            deleted_objects.append(obj['Key'])

    # Log the names of deleted objects
    if deleted_objects:
        print(f"Deleted objects: {deleted_objects}")
    else:
        print("No objects older than 30 days found.")

if __name__ == "__main__":
    delete_old_objects()

