"""
This is a boilerplate pipeline 'siamese'
generated using Kedro 0.18.1
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import siamese_network_fun, data_preparation, clustering_siamese


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=data_preparation,
                inputs="validated_json_dataset",
                outputs="trajectory_dataset",
                name="data_preparation_node",
            ),
            node(
                func=siamese_network_fun,
                inputs="trajectory_dataset",
                outputs="siamese_matrix",
                name="siamese_network",
                ),
            node(
                func=clustering_siamese,
                inputs="siamese_matrix",
                outputs="clustering_siamese",
                name="clustering_siamese",
            ),

        ]
    )