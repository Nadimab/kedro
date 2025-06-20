"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from .pipelines import load_cmap_dataset as cmap
from .pipelines import heatmaps, kmeans_clustering


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    load_cmap_pipeline = cmap.create_pipeline()
    heatmap_pipeline = heatmaps.create_pipeline()
    kmeans_pipeline = kmeans_clustering.create_pipeline()

    return {
        "__default__": load_cmap_pipeline,
        "cmap": load_cmap_pipeline,
        "heatmap": heatmap_pipeline,
        "kmeans" : kmeans_pipeline,
    }
