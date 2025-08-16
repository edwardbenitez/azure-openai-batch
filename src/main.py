from datetime import datetime
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
import time
import datetime
load_dotenv()

def main():
    storage_account_url = (
        f"https://{os.environ['STORAGE_ACCOUNT_NAME']}.blob.core.windows.net"
    )
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview",
    )
    batch_response = client.batches.create(
        input_file_id=None,
        endpoint="/chat/completions",
        completion_window="24h",
        extra_body={
            "input_blob": f"{storage_account_url}/batch-input/data.jsonl",
            "output_folder": {
                "url": f"{storage_account_url}/batch-output",
            },
        },
    )

    batch_id = batch_response.id
    print(batch_response.model_dump_json(indent=2))

    status = "validating"
    while status not in ("completed", "failed", "canceled"):
        time.sleep(30)  # Wait for 30 seconds before checking the status again
        batch_response = client.batches.retrieve(batch_id)
        status = batch_response.status
        print(f"{datetime.datetime.now()} Batch Id: {batch_id},  Status: {status}")

    if batch_response.status == "failed":
        for error in batch_response.errors.data:
            print(f"Error code {error.code} Message {error.message}")


if __name__ == "__main__":
    main()
