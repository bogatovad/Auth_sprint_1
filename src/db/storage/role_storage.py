from db.models import Device, User
from db.postgres import db


class RoleStorage:
    @staticmethod
    def create(name: str, owner: User) -> Device:
        device = Device(name=name, owner=owner)
        db.session.add(device)
        db.session.commit()
        return device