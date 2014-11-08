from google.appengine.ext import db
from oauth2client.appengine import CredentialsProperty

Query = db.Query

class Student(db.Model):
  firstname = db.StringProperty()
  lastname = db.StringProperty()
  branch = db.StringProperty()
  year = db.StringProperty()
  college = db.StringProperty()
  course = db.StringProperty()
  email = db.StringProperty()
  identity = db.StringProperty()

class CredentialsModel(db.Model):
  credentials = CredentialsProperty()

class Information(db.Model):
  alias_id = db.StringProperty()
  group_id = db.StringProperty()
