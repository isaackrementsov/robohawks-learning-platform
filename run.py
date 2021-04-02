from app import app
from config import LOCAL_CONFIG

app.run(host='127.0.0.1', port=LOCAL_CONFIG['run_port'], debug=False)
