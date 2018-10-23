import sys

from vigil_app import app, db
from vigil_app import views

import os

def main():
    # db.create_all()

    # app.secret_key = os.urandom(12) # for running session with wrong password
    # app.run(debug=True, host='0.0.0.0', port=5000)
    
    app.run(debug=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
