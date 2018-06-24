from flask import Flask, render_template, request, redirect, url_for
from session import Session
from werkzeug.utils import secure_filename
import subprocess
import sys
import os
import json
import logging
from audioAnalysis import featureExtractionFileWrapper
from model import predict
import urllib
import audiotranscode

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 100000
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/getSession')
def getSessionDebug():
  return json.dumps(Session().sessionDebug())

@app.route('/getJoinedSession')
def getSessionJoinedDebug():
  return json.dumps(Session().sessionJoinedDebug())

@app.route('/session/<sessionid>/<userid>')
def session(sessionid, userid):
  another_end_userid = Session().verifySessionHasUser(sessionid, userid)
  if another_end_userid != str(False):
    return render_template('session.html', userid=userid, another_end_userid=another_end_userid)
  else:
    return another_end_userid

@app.route('/session/generate/<userid1>/<userid2>')
def getSessionUrl(userid1, userid2):
  sessionid = Session().generateSessionForUsers(userid1, userid2)
  # return 'https://localhost:5000/session/' + sessionid + '/' + userid1
  return json.dumps({
      "messages": [
        {"text": 'https://you-planet.herokuapp.com/session/' + sessionid + '/' + userid1},
      ]
    })

@app.route('/session/join/<sessionid>/<userid>')
def joinSession(sessionid, userid):
  return Session().sessionJoin(sessionid, userid)

@app.route('/session/leave/<sessionid>/<userid>')
def leaveSession(sessionid, userid):
  return Session().sessionLeave(sessionid, userid)

@app.route('/session/anotherEndReady/<sessionid>/<userid>')
def anotherEndUserReady(sessionid, userid):
  return Session().sessionAnotherEndReady(sessionid, userid)  

@app.route('/session/clear')
def clearSession():
  return Session().sessionClear() 

@app.route('/sessionTherapist/<userid>')
def sessionForTherapist(userid):
  sessionid = Session().sessionTherapist(userid)
  return redirect('https://you-planet.herokuapp.com/session/' + sessionid + '/' + userid)

@app.route('/screen/<url>', methods=['GET', 'POST'])
def screen(url):
  AAC_FILE = "a.aac"
  if os.path.isfile(AAC_FILE):
    os.remove(AAC_FILE)
  urllib.urlretrieve (url, AAC_FILE)
  return ''

@app.route('/prescreening/<filename>', methods=['GET', 'POST'])
def prescreening(filename):
  # cleanfile = filename.replace(".wav", "_clean.wav")
  # noisefile = filename.replace(".wav", "_noise.wav")
  ## If file exists, delete it ##
  # if os.path.isfile(cleanfile):
  #   os.remove(cleanfile)
  ## If file exists, delete it ##
  # if os.path.isfile(noisefile):
  #   os.remove(noisefile)  
  # subprocess.Popen("ffmpeg -i " + filename + " -vn -ss 00:00:00 -t 00:00:01 " + noisefile, stdout=subprocess.PIPE).stdout.read()
  # subprocess.Popen("sox " + noisefile + " -n noiseprof noise.prof", stdout=subprocess.PIPE).stdout.read()
  # subprocess.Popen("sox " + filename + " " + cleanfile + " noisered noise.prof 0.21", stdout=subprocess.PIPE).stdout.read()
  # subprocess.Popen("python audioAnalysis.py featureExtractionFile -i " + cleanfile + " -mw 1.0 -ms 1.0 -sw 0.050 -ss 0.050 -o " + cleanfile, stdout=subprocess.PIPE).stdout.read()
  # output = subprocess.Popen("python model.py " + cleanfile + "_st.csv", stdout=subprocess.PIPE).stdout.read()  
  featureExtractionFileWrapper(filename, filename, 1.0, 1.0, 0.050, 0.050)
  output = predict(filename + "_st.csv")
  #print subprocess.Popen("python audioAnalysis.py featureExtractionFile -i " + filename + " -mw 1.0 -ms 1.0 -sw 0.050 -ss 0.050 -o " + filename, stdout=subprocess.PIPE).stdout.read()
  #output = subprocess.Popen("python model.py " + filename + "_st.csv", stdout=subprocess.PIPE).stdout.read()  
  sys.stdout.flush()
  return output

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        # print(request.files)
        if 'file' not in request.files:
            print 'No file part'
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print 'No selected file'
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return prescreening(filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/debug')
def debug():
    return 'hi'

if __name__ == "__main__":
  # context = ('static/server.crt', 'static/server.key')
  # app.run(host='0.0.0.0', ssl_context=context, debug=True)
  app.run()
  