from app.misc.enums import UserPermEnum
from app.models import *
from app.models.caffe import Caffe
from app.services.db_ctx import BaseRepo


class UserRepo(BaseRepo[User]):
    model = User

    async def get_user(self, user_id: int) -> User:
        model = self.model
        return await self.get_one(model.user_id == user_id)

    async def update_user(self, user_id: int, **kwargs) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def get_baristas(self):
        return await self.get_all(self.model.permission == UserPermEnum.ROOT)

    async def get_user_by_full_name(self, full_name: str):
        return await self.get_one(self.model.full_name == full_name)

    @property
    async def voted(self):
        result = len(await self.get_all(self.model.voted > 0))
        if result == 0:
            return 1
        else:
            return result + 1


class CaffeRepo(BaseRepo[Caffe]):
    model = Caffe

    async def get_caffe(self, caffe_id: int) -> Caffe:
        model = self.model
        return await self.get_one(model.caffe_id == caffe_id)

    async def update_caffe(self, caffe_id: int, **kwargs) -> None:
        return await self.update(self.model.caffe_id == caffe_id, **kwargs)

    async def get_caffe_by_name(self, name: str):
        return await self.get_one(self.model.name == name)


__all__ = (
    'UserRepo',
    'CaffeRepo'
)
