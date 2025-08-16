import io
import os
import uuid
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient,
    BlobBlock,
    BlobClient,
    StandardBlobTier,
)

load_dotenv()


def main():
    files = glob.glob("files/*.jsonl")
    storage_account_url = (
        f"https://{os.environ['STORAGE_ACCOUNT_NAME']}.blob.core.windows.net"
    )

    account_url = storage_account_url
    credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    container_name = "batch-input"
    container_client = blob_service_client.get_container_client(container_name)

    for file in files:
        file_name = os.path.basename(file)
        # Upload the file to the container
        with open(file, "rb") as data:
            blob_client = container_client.upload_blob(
                name=file_name, data=data, overwrite=True
            )
        print(f"Uploaded {file_name} to {container_name} container.")


if __name__ == "__main__":
    main()
