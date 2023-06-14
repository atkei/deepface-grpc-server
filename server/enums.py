import sys
from typing import List

from enum import IntEnum, Enum

import numpy as np


class FeatureOperationType(IntEnum):
    ADD = 0
    REMOVE = 1


class SimilarityMetricsType(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    EUCLIDEAN_L2 = "euclidean_l2"

    @classmethod
    def of(cls, target_value: str):
        for e in SimilarityMetricsType:
            if e.value == target_value:
                return e
        raise ValueError("Invalid value: " + target_value)

    def get_min_sim(self) -> float:
        match self:
            case SimilarityMetricsType.COSINE:
                return -sys.float_info.max
            case SimilarityMetricsType.EUCLIDEAN | SimilarityMetricsType.EUCLIDEAN_L2:
                return sys.float_info.max
            case _:
                raise ValueError("Invalid metrics type: " + self.value)

    def get_sim(self, v1: List[float], v2: List[float]) -> float:
        match self:
            case SimilarityMetricsType.COSINE:
                return np.dot(v1, v2) / (np.linalg.norm(v1) * (np.linalg.norm(v2)))
            case SimilarityMetricsType.EUCLIDEAN:
                return np.linalg.norm(np.array(v1) - np.array(v2), ord=2)
            case SimilarityMetricsType.EUCLIDEAN_L2:
                a = v1 / np.sqrt(np.sum(np.multiply(v1, v1)))
                b = v2 / np.sqrt(np.sum(np.multiply(v2, v2)))
                return np.linalg.norm(a - b, ord=2)
            case _:
                raise Exception('Invalid metrics')

    def is_more_sim(self, cur_sim: float, new_sim: float) -> bool:
        match self:
            case SimilarityMetricsType.COSINE:
                return cur_sim < new_sim
            case SimilarityMetricsType.EUCLIDEAN | SimilarityMetricsType.EUCLIDEAN_L2:
                return cur_sim > new_sim
            case _:
                raise Exception('Invalid metrics')


class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"

    @classmethod
    def of(cls, target_value: str):
        for e in LogLevel:
            if e.value == target_value:
                return e
        raise ValueError("Invalid value: " + target_value)


class FeatureModel(Enum):
    Facenet = "Facenet"
    VGC_Face = "VGG-Face"
    Facenet512 = "Facenet512"
    ArcFace = "ArcFace"
    OpenFace = "OpenFace"
    # Dlib = "Dlib"
    # SFace = "SFace"

    @classmethod
    def of(cls, target_value: str):
        for e in FeatureModel:
            if e.value == target_value:
                return e
        raise ValueError("Invalid value: " + target_value)


class DetectorBackend(Enum):
    opencv = "opencv"
    ssd = "ssd"
    # dlib = "dlib"
    mtcnn = "mtcnn"
    retinaface = "retinaface"
    # mediapipe = "mediapipe"

    @classmethod
    def of(cls, target_value: str):
        for e in DetectorBackend:
            if e.value == target_value:
                return e
        raise ValueError("Invalid value: " + target_value)
