import kedro.extras.datasets.json
from kedro.io import PartitionedDataSet

from src.utils.definitions import S3_SERVER_ENDPOINT


class PipelineTestDataset(PartitionedDataSet):
    """Subclass of kedro PartitionedDataSet that connects to our O-Kidia
    S3 server (given as endpoint_url, key and secret in the filesystem
    arguments) and can be called to list all elements that:
        - are found under path
        - finished with extension filename_suffix
    """
    def __init__(self, key: str, secret: str):
        super().__init__(
            path="s3://archives/TestData/S3 files/",
            dataset=kedro.extras.datasets.json.JSONDataSet,
            filename_suffix=".json",
            fs_args={
                "key": key,
                "secret": secret,
                "client_kwargs": {
                    "endpoint_url": S3_SERVER_ENDPOINT,
                },
            },
        )