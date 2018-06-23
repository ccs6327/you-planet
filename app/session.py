import uuid

session = {}

def generateSessionForUsers(userid1, userid2):
  sessionid = str(uuid.uuid4())
  session[sessionid] = [userid1, userid2]
  return sessionid

def verifySessionHasUser(sessionid, userid):
  if sessionid in session and userid in session[sessionid]:
    user_index = session[sessionid].index(userid)
    return session[sessionid][1] if user_index == 0 else session[sessionid][0]
  return str(False)