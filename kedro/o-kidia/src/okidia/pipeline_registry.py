"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from .pipelines import load_cmap_dataset as cmap

from .pipelines import heatmaps, siamese, DTW, trajectory
from .pipelines import data_viz
from .pipelines import dtw_score
from .pipelines import spectral_clustering

from .pipelines import trajectories_similarity as tsim


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    load_cmap_pipeline = cmap.create_pipeline()

    trajectories_similarity_pipeline = tsim.create_pipeline()

    heatmap_pipeline = heatmaps.create_pipeline()
    siamese_pipeline = siamese.create_pipeline()
    DTW_pipeline = DTW.create_pipeline()
    trajectory_pipeline = trajectory.create_pipeline()
    data_viz_pipeline = data_viz.create_pipeline()
    dtw_score_pipeline = dtw_score.create_pipeline()
    spectral_clustering_pipeline = spectral_clustering.create_pipeline()


    return {
        "__default__": load_cmap_pipeline + heatmap_pipeline + siamese_pipeline + DTW_pipeline + trajectory_pipeline,
        #"__default__": load_cmap_pipeline + trajectories_similarity_pipeline,
        "cmap": load_cmap_pipeline,
        "tsim" : trajectories_similarity_pipeline,
        "heatmap": heatmap_pipeline,
        "siamese": siamese_pipeline,
        "DTW": DTW_pipeline,
        "trajectory": trajectory_pipeline,
        "data_viz": data_viz_pipeline,
        "dtw_score": dtw_score_pipeline,
        "spectral_clustering": spectral_clustering_pipeline,
    }
