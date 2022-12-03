from dataclasses import dataclass
from datetime import datetime

from enums import FeatureOperationType


@dataclass
class FeatureEntity:
    feature_id: int
    person_id: int
    feature_data: bytes


@dataclass
class FeatureOperationLogEntity:
    operation_id: int
    feature_id: int
    operation_type: FeatureOperationType
    created_at: datetime
