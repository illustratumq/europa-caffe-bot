import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from app.misc.enums import UserPermEnum
from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True)
    caffe_id = sa.Column(sa.BIGINT, sa.ForeignKey('caffes.caffe_id'), nullable=True)
    full_name = sa.Column(sa.VARCHAR(255), nullable=False)
    mention = sa.Column(sa.VARCHAR(300), nullable=False)
    permission = sa.Column(ENUM(UserPermEnum), default=UserPermEnum.USER, nullable=False)
    chips = sa.Column(sa.BIGINT, nullable=False, default=1)
    voted = sa.Column(sa.INTEGER, nullable=False, default=0)
    is_friend = sa.Column(sa.BOOLEAN, nullable=False, default=False)
