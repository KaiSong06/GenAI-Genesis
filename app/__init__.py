from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='../templates')

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    return app