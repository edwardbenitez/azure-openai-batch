# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import argparse
import json
import logging
import os

load_dotenv()
# configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--batch_folder", dest='batch_folder', help="Batch ID to process", type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args

def read_results(result: str):
    if result is None or result.strip() == "":
        return
    obj_result = json.loads(result)
    if obj_result is not None:
        if "response" in obj_result:
            for choice in obj_result["response"]["body"]["choices"]:
                if "message" in choice and "content" in choice["message"]:
                    print(f"{obj_result['custom_id']} : {choice['message']['content']}")
                    return
    logger.debug("No responses found in the result.")


def download_file(batch) -> str:
    """Downloads a file from Azure Blob Storage and returns the file path."""
    # Define storage account and container information
    storage_account_name = os.environ['STORAGE_ACCOUNT_NAME'] # replace with your storage account name
    container_name = "batch-output"

    # Define the blob paths to download
    blob_paths = [
        f"{batch}/results.jsonl",
    ]

    credential = DefaultAzureCredential()
    account_url = f"https://{storage_account_name}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=credential
    )
    container_client = blob_service_client.get_container_client(container_name)

    for blob_path in blob_paths:
        blob_client = container_client.get_blob_client(blob_path)

        file_name = f".tmp/{blob_path.split('/')[-1]}"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        logger.info(f"Downloading {file_name}...")
        with open(file_name, "wb") as file:
            download_stream = blob_client.download_blob()
            file.write(download_stream.readall())
        logger.info(f"Downloaded {file_name} successfully!")
        return file_name


def main():
    args=parse_args()
    file_path = download_file(args.batch_folder)
    with open(file_path) as f:
        line = f.readline()
        read_results(line)
        while line:
            line = f.readline()
            read_results(line)


if __name__ == "__main__":
    main()
