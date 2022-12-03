from datetime import datetime
from typing import Optional, Tuple, List

from db.tables import FaceFeatures, FaceFeatureOperationLogs
from enums import FeatureOperationType
from entities import FeatureEntity, FeatureOperationLogEntity

from logger_factory import LoggerFactory
logger = LoggerFactory.get_logger(__name__)


async def insert_feature(person_id: int, feature_data: bytes) -> int:
    inserted = await FaceFeatures.insert(
        FaceFeatures(person_id=person_id, feature_data=feature_data)
    ).run()
    feature_id = inserted[0]['feature_id']
    return feature_id


async def insert_feature_operation_log(feature_id: int, operation_type: FeatureOperationType) -> int:
    now = datetime.now()
    inserted = await FaceFeatureOperationLogs.insert(
        FaceFeatureOperationLogs(feature_id=feature_id, operation_type=int(operation_type), created_at=now)
    ).run()
    operation_id = inserted[0]['operation_id']
    return operation_id


async def insert_feature_transaction(person_id: int, feature_data: bytes) -> Tuple[int, int]:
    async with FaceFeatures._meta.db.transaction():
        feature_id = await insert_feature(person_id=person_id, feature_data=feature_data)
        operation_id = await insert_feature_operation_log(
            feature_id=feature_id,
            operation_type=FeatureOperationType.ADD
        )
    return feature_id, operation_id


async def fetch_feature_by_id(feature_id: int) -> Optional[FeatureEntity]:
    fetched = await FaceFeatures.select().where(FaceFeatures.feature_id == feature_id).run()
    return FeatureEntity(
        feature_id=feature_id,
        person_id=fetched[0]['person_id'],
        feature_data=fetched[0]['feature_data']
    ) if len(fetched) > 0 else None


async def fetch_feature_ids_by_person_id(person_id: int) -> List[int]:
    fetched = await FaceFeatures.select().where(FaceFeatures.person_id == person_id).run()
    return [e['feature_id'] for e in fetched]


async def fetch_last_operation_id(now: datetime) -> int:
    last_operation = await FaceFeatureOperationLogs.select(
        FaceFeatureOperationLogs.operation_id
    ).where(FaceFeatureOperationLogs.created_at >= now).limit(1).run()

    if len(last_operation) == 1:
        return last_operation[0]['operation_id']
    else:
        last_operation = await FaceFeatureOperationLogs.select(
            FaceFeatureOperationLogs.operation_id
        ).where().limit(1).order_by(FaceFeatureOperationLogs.operation_id, ascending=False).run()
        return last_operation[0]['operation_id'] if len(last_operation) == 1 else 0


async def load_pending_operations(last_operation_id: int, limit: int) -> List[FeatureOperationLogEntity]:
    pending_ops = await FaceFeatureOperationLogs.select().where(
        FaceFeatureOperationLogs.operation_id > last_operation_id
    ).limit(limit).run()
    return [FeatureOperationLogEntity(**o) for o in pending_ops]


async def fetch_features(offset: int, limit: int) -> List[FeatureEntity]:
    fetched = await FaceFeatures.select().offset(offset).limit(limit).run()
    return [
        FeatureEntity(
            feature_id=f['feature_id'],
            person_id=f['person_id'],
            feature_data=f['feature_data']
        ) for f in fetched
    ]


async def delete_feature(feature_id: int):
    await FaceFeatures.delete().where(FaceFeatures.feature_id == feature_id).run()


async def delete_feature_transaction(feature_id: int) -> Tuple[int, int]:
    async with FaceFeatures._meta.db.transaction():
        operation_id = await insert_feature_operation_log(
            feature_id=feature_id,
            operation_type=FeatureOperationType.REMOVE
        )
        await delete_feature(feature_id=feature_id)
    return feature_id, operation_id
