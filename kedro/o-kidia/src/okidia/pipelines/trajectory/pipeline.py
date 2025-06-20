"""
This is a boilerplate pipeline 'trajectory'
generated using Kedro 0.18.1
"""
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import trajectory_segmentation, calc_dis_Hausdorff, apply_DBSCAN, clustering_analysis

#help: https://kedro.readthedocs.io/en/stable/nodes_and_pipelines/nodes.html
def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=trajectory_segmentation,
                inputs= "validated_json_dataset",
                outputs="reduced_points",
                name = "reduction",
            ),
            node(
                func=calc_dis_Hausdorff,
                inputs="reduced_points",
                outputs="matrix_dis",
                tags= "Hausdorff_tag"
            ),
            node(
                func=apply_DBSCAN,
                inputs="matrix_dis",
                outputs=["ep", "num_clusters"],
            ),
            node(
                func=clustering_analysis,
                inputs=["ep", "num_clusters"],
                outputs="clustering_trajectory",
            ),
        ]
    )
