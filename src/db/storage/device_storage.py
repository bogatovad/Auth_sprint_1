from db.models import Device, User
from db.postgres import db


class DeviceStorage:
    @staticmethod
    def create(name: str, owner: User) -> Device:
        device = Device(name=name, owner=owner)
        db.session.add(device)
        db.session.commit()
        return device

    @staticmethod
    def get(name: str, owner: User) -> bool:
        return Device.query.filter_by(name=name, owner=owner).first()

    def filter(self, name: str, owner: User):
        return db.session.execute(db.Query(Device).filter(Device.name == name, Device.owner == owner))