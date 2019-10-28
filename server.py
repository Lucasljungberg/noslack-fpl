import time
import random

from flask import Flask, render_template

from lib import fpl

app = Flask(__name__)

@app.route('/')
def index():
    manager_data = fpl.get_current_state()
    return render_template(
        'index.html',
        teams=manager_data,
        gameweek=fpl.GAMEWEEK)

@app.errorhandler(404)
def catch_all(path):
    time.sleep(random.randint(2, 6))

    manager_data = fpl.get_current_state()
    return render_template(
        'index.html',
        teams=manager_data,
        gameweek=fpl.GAMEWEEK), 500

if __name__ == '__main__':
    import os
    if os.environ.get('FLASK_ENV', 'development') == 'production':
        app.run(host='0.0.0.0', port=8080)
    else:
        app.run()
