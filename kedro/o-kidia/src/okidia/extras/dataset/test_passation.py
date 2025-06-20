from typing import Dict, Any

from fs_s3fs import S3FS
from kedro.io import AbstractDataSet
from kedro.io.core import get_protocol_and_path


class TestPassation(AbstractDataSet):
    """Subclass of AbstractDataSet to represent one sample of data in the
    PipelineTestDataset.
    TODO implement _load, and eventually _save, _describe or
     PipelineTestDataset._load() to work with this class.
    """
    def __init__(
            self,
            filepath: str,
            fs_args: Dict[str, Any] = None,
    ):
        super().__init__()

        self._fs = S3FS(
            bucket_name="",
            aws_access_key_id=fs_args["key"],
            aws_secret_access_key=fs_args["secret"],
            endpoint_url=fs_args["client_kwargs"]["endpoint_url"],
        )
        _, self._filepath = get_protocol_and_path(filepath)

    def _load(self) -> Any:
        ...

    def _save(self, data: Any) -> None:
        ...

    def _describe(self) -> Dict[str, Any]:
        ...