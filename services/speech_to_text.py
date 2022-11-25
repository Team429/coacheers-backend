from google.cloud import storage


def create_bucket():
    # Instantiates a client
    storage_client = storage.Client()

    # The name for the new bucket
    bucket_name = "hello-from-zz3n"

    # Creates the new bucket
    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created.")
