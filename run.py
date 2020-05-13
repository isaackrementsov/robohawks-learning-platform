from src import app

app.run(host='127.0.0.1', port=app.LOCAL_CONFIG['run_port'], debug=True)
