from flask import Flask, render_template
from session import verifySessionHasUser, generateSessionForUsers
import subprocess
import os

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

@app.route('/prescreening/<filename>')
def prescreening(filename):
  cleanfile = filename.replace(".wav", "_clean.wav")
  noisefile = filename.replace(".wav", "_noise.wav")
  ## If file exists, delete it ##
  if os.path.isfile(cleanfile):
    os.remove(cleanfile)
  ## If file exists, delete it ##
  if os.path.isfile(noisefile):
    os.remove(noisefile)  
  subprocess.Popen("ffmpeg -i " + filename + " -vn -ss 00:00:00 -t 00:00:01 " + noisefile, stdout=subprocess.PIPE).stdout.read()
  subprocess.Popen("sox " + noisefile + " -n noiseprof noise.prof", stdout=subprocess.PIPE).stdout.read()
  subprocess.Popen("sox " + filename + " " + cleanfile + " noisered noise.prof 0.21", stdout=subprocess.PIPE).stdout.read()
  subprocess.Popen("python audioAnalysis.py featureExtractionFile -i " + cleanfile + " -mw 1.0 -ms 1.0 -sw 0.050 -ss 0.050 -o " + cleanfile, stdout=subprocess.PIPE).stdout.read()
  output = subprocess.Popen("python model.py " + cleanfile + "_st.csv", stdout=subprocess.PIPE).stdout.read()  
  return output

if __name__ == "__main__":
  context = ('static/server.crt', 'static/server.key')
  app.run(host='0.0.0.0', ssl_context=context, debug=True)