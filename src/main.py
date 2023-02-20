from db.postgres import db, init_db
from services.application import create_app

app = create_app()


def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run(host='0.0.0.0', port=5555, debug=True)


if __name__ == "__main__":
    main()