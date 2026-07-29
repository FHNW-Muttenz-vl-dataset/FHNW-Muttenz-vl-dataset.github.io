"""
Utilities for converting camera poses and relative orientations between
camera coordinate conventions (e.g. photogrammetric <-> computer vision).

File formats expected (as documented on the dataset page):

poses.json
    {
        "<image_filename>": [16 floats, row-major flattened 4x4 T_cam^world],
        ...
    }

camera_system.json
    {
        "camera_system_description": "...",
        "camera_system_acronym": "...",
        "cameras": [
            {
                "camera_name": "camera_0",
                "width": ...,
                "height": ...,
                "focal_length_px": ...,
                "T_cam0_cam0": [16 floats, row-major flattened 4x4]
            },
            {
                "camera_name": "camera_1",
                ...
                "T_cam1_cam0": [16 floats, row-major flattened 4x4]
            },
            ...
        ]
    }
"""

import json
from pathlib import Path
from typing import Union

import numpy as np

PathLike = Union[str, Path]

# Photogrammetric <-> computer vision convention flip (self-inverse)
CAM_PH_TO_CAM_CV = np.array(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)


def flat_to_matrix(flat: list[float]) -> np.ndarray:
    """Convert a row-major flattened list of 16 values into a 4x4 matrix."""
    return np.array(flat, dtype=np.float64).reshape(4, 4)


def matrix_to_flat(matrix: np.ndarray) -> list[float]:
    """Convert a 4x4 matrix back into a row-major flattened list of 16 values."""
    return matrix.reshape(-1).tolist()


def convert_pose(
    pose: np.ndarray, transformation_matrix: np.ndarray
) -> np.ndarray:
    """
    Convert an image pose (camera-to-world transform) from one camera
    coordinate convention to another, e.g. photogrammetric -> computer vision.

    Since the world frame is unaffected by the camera convention, only the
    camera-side (input) needs remapping:
        T_cam_new^world = T_cam_old^world @ T_cam_new^cam_old

    Parameters
    ----------
    pose : np.ndarray, shape (4, 4)
        Camera-to-world transform in the original convention (T_cam_old^world).
    transformation_matrix : np.ndarray, shape (4, 4)
        Conversion matrix from the new convention to the old one (T_cam_new^cam_old).

    Returns
    -------
    np.ndarray, shape (4, 4)
        Camera-to-world transform in the new camera convention.
    """
    return pose @ transformation_matrix


def convert_poses(
    poses: dict[str, np.ndarray], transformation_matrix: np.ndarray
) -> dict[str, np.ndarray]:
    """
    Convert a whole set of image poses (as loaded by load_poses) from one
    camera coordinate convention to another.

    This is a thin batch wrapper around convert_pose and can be used
    independently of convert_dataset_convention, e.g. on poses already
    loaded/held in memory.

    Parameters
    ----------
    poses : dict[str, np.ndarray]
        Mapping of image filename -> 4x4 camera-to-world pose matrix,
        in the original camera convention.
    transformation_matrix : np.ndarray, shape (4, 4)
        Conversion matrix from the new convention to the old one (T_cam_new^cam_old).

    Returns
    -------
    dict[str, np.ndarray]
        Mapping of image filename -> 4x4 pose matrix in the new camera convention.
    """
    return {
        image_name: convert_pose(pose, transformation_matrix)
        for image_name, pose in poses.items()
    }


def convert_relative_orientation(
    relative_orientation: np.ndarray, transformation_matrix: np.ndarray
) -> np.ndarray:
    """
    Convert a relative orientation (camX-to-cam0 transform) from one camera
    coordinate convention to another.

    Both endpoints (camX and cam0) are camera frames, so both sides are remapped:
        T_camX_new^cam0_new = T_cam_old^cam_new @ T_camX_old^cam0_old @ T_cam_new^cam_old

    Note: T_cam_old^cam_new is the inverse of transformation_matrix.

    Parameters
    ----------
    relative_orientation : np.ndarray, shape (4, 4)
        CamX-to-cam0 transform in the original convention (T_camX_old^cam0_old).
    transformation_matrix : np.ndarray, shape (4, 4)
        Conversion matrix from the new convention to the old one (T_cam_new^cam_old).

    Returns
    -------
    np.ndarray, shape (4, 4)
        CamX-to-cam0 transform in the new camera convention.
    """
    return (
        np.linalg.inv(transformation_matrix)
        @ relative_orientation
        @ transformation_matrix
    )


def convert_relative_orientations(
    relative_orientations: dict[str, np.ndarray],
    transformation_matrix: np.ndarray,
) -> dict[str, np.ndarray]:
    """
    Convert a whole set of relative orientations (as loaded by
    load_camera_system) from one camera coordinate convention to another.

    This is a thin batch wrapper around convert_relative_orientation and can
    be used independently of convert_dataset_convention, e.g. on relative
    orientations already loaded/held in memory.

    Parameters
    ----------
    relative_orientations : dict[str, np.ndarray]
        Mapping of "T_camX_cam0" key -> 4x4 camX-to-cam0 matrix,
        in the original camera convention.
    transformation_matrix : np.ndarray, shape (4, 4)
        Conversion matrix from the new convention to the old one (T_cam_new^cam_old).

    Returns
    -------
    dict[str, np.ndarray]
        Mapping of "T_camX_cam0" key -> 4x4 matrix in the new camera convention.
    """
    return {
        key: convert_relative_orientation(
            relative_orientation, transformation_matrix
        )
        for key, relative_orientation in relative_orientations.items()
    }


def load_poses(poses_path: PathLike) -> dict[str, np.ndarray]:
    """
    Load poses.json and return a dict mapping image filename -> 4x4 pose matrix.
    """
    with open(poses_path, "r") as f:
        raw = json.load(f)
    return {
        image_name: flat_to_matrix(flat) for image_name, flat in raw.items()
    }


def save_poses(poses: dict[str, np.ndarray], output_path: PathLike) -> None:
    """
    Write a dict mapping image filename -> 4x4 pose matrix to a poses.json file.
    """
    raw = {
        image_name: matrix_to_flat(matrix)
        for image_name, matrix in poses.items()
    }
    with open(output_path, "w") as f:
        json.dump(raw, f, indent=4)


def load_camera_system(camera_system_path: PathLike) -> dict[str, np.ndarray]:
    """
    Load camera_system.json and return a dict mapping the relative-orientation
    key (e.g. "T_cam1_cam0") -> 4x4 matrix.
    """
    with open(camera_system_path, "r") as f:
        raw = json.load(f)

    relative_orientations = {}
    for camera in raw["cameras"]:
        # The relative-orientation key is whichever field starts with "T_cam"
        key = next(k for k in camera if k.startswith("T_cam"))
        relative_orientations[key] = flat_to_matrix(camera[key])
    return relative_orientations


def save_camera_system(
    relative_orientations: dict[str, np.ndarray],
    camera_system_path: PathLike,
    output_path: PathLike,
) -> None:
    """
    Write converted relative orientations back into a camera_system.json file,
    preserving all other metadata (camera_name, width, height, focal_length_px, ...)
    from the original file at camera_system_path.
    """
    with open(camera_system_path, "r") as f:
        raw = json.load(f)

    for camera in raw["cameras"]:
        key = next(k for k in camera if k.startswith("T_cam"))
        camera[key] = matrix_to_flat(relative_orientations[key])

    with open(output_path, "w") as f:
        json.dump(raw, f, indent=4)


def convert_dataset_convention(
    poses_path: PathLike,
    camera_system_path: PathLike,
    transformation_matrix: np.ndarray,
    output_poses_path: PathLike = None,
    output_camera_system_path: PathLike = None,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """
    Read poses.json and camera_system.json, convert all image poses and
    relative orientations to a new camera coordinate convention, and
    (optionally) write the converted files back out.

    Parameters
    ----------
    poses_path : PathLike
        Path to the input poses.json file.
    camera_system_path : PathLike
        Path to the input camera_system.json file.
    transformation_matrix : np.ndarray, shape (4, 4)
        Conversion matrix from the new convention to the old one
        (T_cam_new^cam_old), e.g. CAM_PH_TO_CAM_CV.
    output_poses_path : PathLike, optional
        If given, write the converted poses to this path.
    output_camera_system_path : PathLike, optional
        If given, write the converted camera system to this path
        (all non-pose metadata is copied over from camera_system_path).

    Returns
    -------
    (converted_poses, converted_relative_orientations) : tuple of dicts
        converted_poses: image filename -> converted 4x4 pose matrix
        converted_relative_orientations: "T_camX_cam0" key -> converted 4x4 matrix
    """
    poses = load_poses(poses_path)
    relative_orientations = load_camera_system(camera_system_path)

    converted_poses = convert_poses(poses, transformation_matrix)
    converted_relative_orientations = convert_relative_orientations(
        relative_orientations, transformation_matrix
    )

    if output_poses_path is not None:
        save_poses(converted_poses, output_poses_path)
    if output_camera_system_path is not None:
        save_camera_system(
            converted_relative_orientations,
            camera_system_path,
            output_camera_system_path,
        )

    return converted_poses, converted_relative_orientations
