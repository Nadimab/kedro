"""
This is a boilerplate pipeline 'kmeans_clustering'
generated using Kedro 0.18.0
"""

from xml.sax.xmlreader import InputSource
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import data_preparation, kmeans, export_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=data_preparation,
                inputs="features_dataset",
                outputs="matrix_features",
                name="datapreparation_node",
            ),
            node(
                func=kmeans,
                inputs="matrix_features",
                outputs="clusters",
                name="kmeans_node",
            ),
            node(
                func=export_data,
                inputs="clusters",
                outputs="CSV_sheet",
                name="export_node",
            )
        ]
    )
