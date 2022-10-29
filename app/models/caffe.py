import sqlalchemy as sa
from app.models.base import TimedBaseModel


class Caffe(TimedBaseModel):
    caffe_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=True, index=True)
    name = sa.Column(sa.VARCHAR(255), nullable=True)
    description = sa.Column(sa.VARCHAR(1000), nullable=True)
    location = sa.Column(sa.VARCHAR(500), nullable=True)
    chips = sa.Column(sa.BIGINT, nullable=False, default=0)
    grade = sa.Column(sa.FLOAT, nullable=True, default=5)
