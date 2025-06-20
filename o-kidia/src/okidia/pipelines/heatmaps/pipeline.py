"""
This is a boilerplate pipeline 'heatmaps'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_heatmap, vgg19

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_heatmap,
                inputs="validated_json_dataset",
                outputs="heatmap_img_dataset",
                name="heatmap_node",
            ),
            node(
                func=vgg19,
                inputs="heatmap_img_dataset",
                outputs="features_dataset",
                name="vgg_node",
            ),
            
        ]
    )
