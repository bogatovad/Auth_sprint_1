from db.models import User
from db.postgres import db, init_db
from services.application import create_app

app = create_app()


def main():
    init_db(app)

    app.app_context().push()
    db.create_all()
    # user = User.query.filter_by(login='admin').first()
    # user1 = User.query.filter_by(login='admin2').first()

    # print(user, user1)

    app.run(host='0.0.0.0', port=5555, debug=True)


if __name__ == '__main__':
    main()
