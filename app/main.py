from flask import Flask, render_template
from session import verifySessionHasUser, generateSessionForUsers

app = Flask(__name__, static_url_path='')

@app.route('/session/<sessionid>/<userid>')
def session(sessionid, userid):
  another_end_userid = verifySessionHasUser(sessionid, userid)
  if another_end_userid != str(False):
    return render_template('session.html', userid=userid, another_end_userid=another_end_userid)
  else:
    return "Invalid session"

@app.route('/session/generate/<userid1>/<userid2>')
def getSessionUrl(userid1, userid2):
  sessionid = generateSessionForUsers(userid1, userid2)
  return 'https://192.168.0.52:5000/session/' + sessionid + '/' + userid1

if __name__ == "__main__":
  context = ('static/server.crt', 'static/server.key')
  app.run(host='0.0.0.0', ssl_context=context, debug=True)