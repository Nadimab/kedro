"""
This is a boilerplate pipeline 'load_cmap_dataset'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import validate_json


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=validate_json,
                inputs="local_json_dataset",
                outputs="validated_json_dataset",
                name="validation_node",
            ),
        ]
    )
