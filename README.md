# OpenAI Batch processing

The following project is an example of how to work with Azure Open AI Batch.

## IAC

To run the Infrastructure as code (IaC)

go to iac/development.tfvars and replace the values with yours

run the corresponding terraform commands

```bash
# terminal running inside iac folder
terraform init
terraform plan -var-file="development.tfvars" -out oai-plan
terraform apply oai-plan
```

## DATA

OpenAI requires a jsonl file with all the queries to be processed in batch.
so go to the data/files/data.jsonl and update the questions if you want
once you have updated the data.jsonl file with your questions upload the data.jsonl file by running the following command.

```bash
# terminal running inside data folder
uv sync
uv run main.py
```

## SRC

Once you have uploaded the jsonl file containing your queries it is time to start the batch process. For that run the following command.

```bash
# terminal running inside src folder
uv sync
uv run main.py
```

> Information!
>
> The script will wait review the status of the batch process every 30 seconds until the process finish or fail.

To get the results

```bash
# terminal running inside src folder
uv run results.py --batch_folder xxxxxxxxxxxxxxxxxxxxxxxxxx
```
