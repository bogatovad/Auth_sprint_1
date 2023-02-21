def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    return instance


def update_permissions(session, model, role, permissions_list):
    for item in permissions_list:
        endpoint, method = item[0], item[1]
        permission = get_or_create(session, model, resource=endpoint, method=method)
        role.add_permission(permission)
