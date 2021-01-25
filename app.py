from apps import create_app
from flask_script import Manager


app = create_app()
manager = Manager(app=app) 

if __name__ == '__main__':
    manager.run()
