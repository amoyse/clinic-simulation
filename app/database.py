from app import db, create_app
from app.models import User

app = create_app()
app.app_context().push()  # Binds the app context
db.create_all()  # Creates the tables
