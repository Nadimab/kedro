"""
This is a boilerplate pipeline 'DTW'
generated using Kedro 0.18.1
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import dtw_score_similarity_matrix, clustering_dtw

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=dtw_score_similarity_matrix,
                inputs="validated_json_dataset",
                outputs="DTW_Similarity_dataset",
                name="dtw_node",
            ),
            node(
                func=clustering_dtw,
                inputs="DTW_Similarity_dataset",
                outputs="clustering_dtw",
                name="clustering_DTW",
            )
        ]
)