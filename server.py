import time
import random

from flask import Flask, render_template

from src import fpl

app = Flask(__name__)

@app.route('/')
def index():
    current_info = fpl.get_current_state()
    return render_template(
        'index.html',
        teams=current_info.managers,
        gameweek=current_info.gameweek)

@app.errorhandler(404)
def catch_all(path):
    time.sleep(random.randint(10, 30))

    current_info = fpl.get_current_state()
    return render_template(
        'index.html',
        teams=current_info.managers,
        gameweek=current_info.gameweek)

if __name__ == '__main__':
    import os
    if os.environ.get('FLASK_ENV', 'development') == 'production':
        app.run(host='0.0.0.0', port=8080)
    else:
        app.run()
