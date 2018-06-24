import uuid

class Session:
  session = {}
  joinedSession = {}

  def sessionDebug(self):
    return Session.session

  def generateSessionForUsers(self, userid1, userid2):
    sessionid = str(uuid.uuid4())
    Session.session[sessionid] = [userid1, userid2]
    print(Session.session)
    return sessionid

  def verifySessionHasUser(self, sessionid, userid):
    if sessionid in Session.session and userid in Session.session[sessionid]:
      user_index = Session.session[sessionid].index(userid)
      return Session.session[sessionid][1] if user_index == 0 else Session.session[sessionid][0]
    return str(False)

  def sessionJoin(self, sessionid, userid):
    if sessionid in session and userid in session[sessionid]:
      if sessionid in Session.joinedSession:
        Session.joinedSession[sessionid].append(userid)
      else:
        Session.joinedSession[sessionid] = [userid]
      return "Success"
    else:
      return "Failed"

  def sessionLeave(self, sessionid, userid):
    if sessionid in session and userid in session[sessionid]:
      if sessionid in Session.joinedSession and userid in Session.joinedSession[sessionid]:
        del Session.joinedSession[sessionid][Session.joinedSession[sessionid].index(userid)]
        return "Success"
      else:
        return "Failed"
    else:
      return "Failed" 

  def sessionAnotherEndReady(self, sessionid, userid):
    if sessionid in Session.session and userid in Session.session[sessionid]:
      user_index = Session.session[sessionid].index(userid)
      another_end_user = Session.session[sessionid][1] if user_index == 0 else Session.session[sessionid][0]
      return "Ready" if sessionid in Session.joinedSession and another_end_user in Session.joinedSession[sessionid] else "Not Ready"
    else:
      return "Not Ready"
