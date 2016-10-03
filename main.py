from collections import namedtuple

import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('settings.py')

api_base = 'https://api.uptimerobot.com'
api_key = app.config['UPTIMEROBOT_API_KEY']
page_name = app.config.get('PAGE_NAME', 'UptimeRobot')
status_down = ['8', '9']
status_paused = ['0', '1']

Monitor = namedtuple('Monitor', ['id', 'name', 'uptime', 'status'])


@app.route('/')
def hello():
    r = requests.get(api_base + '/getMonitors', params={
        'format': 'json',
        'noJsonCallback': 1,
        'apiKey': api_key
    }).json()
    if r['stat'] != 'ok':
        raise Exception('{eid}: {emsg}'.format(eid=r['id'], emsg='message'))
    monitors = r['monitors']['monitor']
    monitors_formatted = []
    for monitor in monitors:
        status_raw = monitor['status']
        if status_raw in status_down:
            status = 'danger'
        elif status_raw in status_paused:
            status = 'warning'
        else:
            status = 'success'
        monitors_formatted.append(Monitor(
            id=monitor['id'], name=monitor['friendlyname'],
            uptime=int(float(monitor['alltimeuptimeratio'])),
            status=status
        ))
    return render_template('index.html', monitors=monitors_formatted,
                           page_name=page_name)

if __name__ == '__main__':
    app.run()
