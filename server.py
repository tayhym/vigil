import sys

from vigil_app import app, db
from vigil_app import views

def main():
    db.create_all()
    app.run(debug=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())