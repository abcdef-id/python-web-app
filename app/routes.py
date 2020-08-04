from app import app

class Route():
    def __init__(self):

        from app.controllers.user import User
        User()
        from app.controllers.main import Main
        Main()