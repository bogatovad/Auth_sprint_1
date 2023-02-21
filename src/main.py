from db.postgres import init_db, db
from services.application import create_app


app = create_app()

init_db(app)
app.app_context().push()
db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

