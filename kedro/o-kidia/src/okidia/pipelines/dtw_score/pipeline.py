"""
This is a boilerplate pipeline 'dtw_score'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import dtw_score_similarity_matrix

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=dtw_score_similarity_matrix,
                inputs="validated_json_dataset",
                outputs="DTW_Similarity_dataset",
                name="dtw_node",
            ),
        ]
)

