from flask import Flask, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
  return send_from_directory('static', 'index.html')

if __name__ == "__main__":
  context = ('static/server.crt', 'static/server.key')
  app.run(host='0.0.0.0', ssl_context=context, debug=True)