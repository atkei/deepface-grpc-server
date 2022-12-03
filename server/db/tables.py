from piccolo.table import Table
from piccolo.columns import Serial, Integer, Bytea, Timestamp, SmallInt


class FaceFeatures(Table):
    feature_id = Serial(primary_key=True)
    person_id = Integer()
    feature_data = Bytea()


class FaceFeatureOperationLogs(Table):
    operation_id = Serial(primary_key=True)
    feature_id = Integer()
    operation_type = SmallInt()
    created_at = Timestamp()
