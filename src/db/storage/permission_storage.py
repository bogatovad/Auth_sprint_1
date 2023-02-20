from db.models import Permission, Role
from db.postgres import db


class RoleStorage:

    def create(self) -> Role:
        p1 = Permission(name='test_p1', resource='/api/v1/auth', method='POST')
        p2 = Permission(name='test_p2', resource='/api/v1/signup', method='POST')
        p3 = Permission(name='test_p3', resource='/api/v1/logout', method='POST')

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)

        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()

        # map permissions to role

        role.permissions = [p1, p2, p3]

        db.session.commit()

        return role
