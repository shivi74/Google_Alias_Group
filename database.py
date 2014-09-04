from google.appengine.ext import db

Query = db.Query

class Student(db.Model):
  firstname = db.StringProperty(required = True)
  lastname = db.StringProperty(required = True)
  email = db.StringProperty(required = True)
  course = db.StringProperty(required = True)
  branch = db.StringProperty(required = True)
  year = db.StringProperty(required = True)
  clgname = db.StringProperty(required = True)
