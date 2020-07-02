# run.py
import os
from project import app

@app.route('/<name>')
def hello_name(name):
    return f'Hello {name}'


port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)