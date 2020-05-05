from src import app
import json


local_config = json.load(open('local_config.json', 'r'))

app.run(host='127.0.0.1', port=local_config['run_port'], debug=True)
