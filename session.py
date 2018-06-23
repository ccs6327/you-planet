import uuid

session = {}
joinedSession = {}

def sessionDebug():
  return session

def generateSessionForUsers(userid1, userid2):
  sessionid = str(uuid.uuid4())
  session[sessionid] = [userid1, userid2]
  return sessionid

def verifySessionHasUser(sessionid, userid):
  logger.info("sessionid:" + sessionid + " userid:" + userid)
  logger.info(session)
  if sessionid in session and userid in session[sessionid]:
    user_index = session[sessionid].index(userid)
    return session[sessionid][1] if user_index == 0 else session[sessionid][0]
  return str(False)

def sessionJoin(sessionid, userid):
  if sessionid in session and userid in session[sessionid]:
    if sessionid in joinedSession:
      joinedSession[sessionid].append(userid)
    else:
      joinedSession[sessionid] = [userid]
    return "Success"
  else:
    return "Failed"

def sessionLeave(sessionid, userid):
  if sessionid in session and userid in session[sessionid]:
    if sessionid in joinedSession and userid in joinedSession[sessionid]:
      del joinedSession[sessionid][joinedSession[sessionid].index(userid)]
      return "Success"
    else:
      return "Failed"
  else:
    return "Failed" 

def sessionAnotherEndReady(sessionid, userid):
  if sessionid in session and userid in session[sessionid]:
    user_index = session[sessionid].index(userid)
    another_end_user = session[sessionid][1] if user_index == 0 else session[sessionid][0]
    return "Ready" if sessionid in joinedSession and another_end_user in joinedSession[sessionid] else "Not Ready"
  else:
    return "Not Ready"
