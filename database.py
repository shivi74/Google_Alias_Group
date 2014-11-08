from google.appengine.ext import db
from oauth2client.appengine import CredentialsProperty

Query = db.Query

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
