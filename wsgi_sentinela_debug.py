import os

os.environ['DEBUG'] = '1'

from sentinela.app import app

if __name__ == '__main__':
    app.run()
