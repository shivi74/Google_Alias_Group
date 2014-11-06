from google.appengine.ext import db

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
