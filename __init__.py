from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnevnik.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if app.debug == True:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            toolbar = DebugToolbarExtension(app)
        except:
            pass

    import admin.admin as admin
    import main.main as main

    app.register_blueprint(admin.admin, url_prefix='/admin')
    app.register_blueprint(main.main, url_prefix='/main')

    return app