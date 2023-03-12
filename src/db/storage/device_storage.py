from __future__ import annotations

from db.models import Device
from db.models import User
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
        return db.session.execute(
            db.Query(Device).filter(
                Device.name == name,
                Device.owner == owner,
            ),
        )

    @staticmethod
    def get_or_create(**kwargs):
        instance = db.session.query(Device).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = Device(**kwargs)
            db.session.add(instance)
            db.session.commit()
        return instance
