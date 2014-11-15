from google.appengine.ext import ndb

class Student(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    branch = ndb.StringProperty()
    year = ndb.StringProperty()
    college = ndb.StringProperty()
    course = ndb.StringProperty()
    email = ndb.StringProperty()
    identity = ndb.StringProperty()


class Tokens(ndb.Model):
    """Stores token information."""
    access_token = ndb.StringProperty(required=True)
    refresh_token = ndb.StringProperty(required=True)
