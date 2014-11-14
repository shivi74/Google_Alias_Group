from google.appengine.ext import ndb


<<<<<<< HEAD
class Student(db.Model):
  firstname = db.StringProperty()
  lastname = db.StringProperty()
  identity = db.StringProperty()
  branch = db.StringProperty()
  year = db.StringProperty()
  college = db.StringProperty()
  course = db.StringProperty()
  email = db.StringProperty()
<<<<<<< HEAD

=======
  identity = db.StringProperty()

class CredentialsModel(db.Model):
  credentials = CredentialsProperty()
>>>>>>> 6e5db01c4b63e21acaf88400d2fed78f5949339d
=======
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
>>>>>>> 64b40b1b79c0b3b444a37ebb1784e30c89436273
