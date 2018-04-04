# run.py
from Asset_Management_App import app
from Asset_Management_App import db

if __name__ == 'main':
    db.init_app(app)
    app.run()

