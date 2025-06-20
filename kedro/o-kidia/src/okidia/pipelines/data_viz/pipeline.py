"""
This is a boilerplate pipeline 'data_viz'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import plot_game_session

def create_pipeline(**kwargs) -> Pipeline:
        return pipeline(
        [
            node(
                func=plot_game_session,
                inputs="validated_json_dataset",
                outputs="challenges_plot",
                name="viz_node",
            ),
        ]
    )
