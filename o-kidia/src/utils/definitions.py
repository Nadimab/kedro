"""Declarations and definitions across the whole project.
"""
from pathlib import Path

# C-MAP
CMAP_ROOT_DIR = Path("/home/o-kidia/C-MAP_DATA/").resolve()
CMAP_TARGET_DIR = CMAP_ROOT_DIR.joinpath("decrypted_videos")
CMAP_FEATURES_DIR = CMAP_ROOT_DIR.joinpath("processed_data")
CMAP_LOGS_DIR = CMAP_ROOT_DIR.joinpath("S3 files", "logs")
CMAP_VIDEOS_DIR = CMAP_ROOT_DIR.joinpath("S3 files", "videos")
CMAP_CORRESPONDENCE_TABLE = CMAP_ROOT_DIR.joinpath(
    "Videos keys", "video_keys_id.csv"
)
CMAP_LABELS_LOC = CMAP_ROOT_DIR.joinpath("20220302_cmap_vdv_labels.csv")

# External resources
TRAINED_MODELS_LOC = Path("./external_resources/trained_models/").resolve()

# Super project constants
PROJECT_ROOT_DIR = Path("/home/PycharmProjects/o-kidia").resolve()
