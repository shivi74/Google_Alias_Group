#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import webapp2
import os
import database
import email
import string
#import gdata.apps.multidomain.client;
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import users
from google.appengine.ext import db


class LogSenderHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Recieved a message from: " + message.sender)
        # Get the body text from the e-mail
        bodies = message.bodies('text/plain') # generator
        body_text = [body for body in bodies]
        student = database.Student()
        logging.info(body_text[0][1].decode())
        for values in body_text[0][1].decode().split('\n'):
          logging.info(values)
          if not values:
            break
          key, value = values.split(':')
          logging.info(key)
          logging.info(value)
          setattr(student, key, value)
        student.put()
        self.redirect('/main')

        #check for already existing student
        #que=db.Query(Student).filter("email=",email)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        firstname = self.request.get('firstname')
        logging.info("firstname = %s" % firstname)
        lastname = self.request.get('lastname')
        branch = self.request.get('branch')
        year = self.request.get('year')
        college = self.request.get('college')
        course = self.request.get('course')
        email = self.request.get('email')

        q = GqlQuery("SELECT * FROM database.Student")
        for student in q.run():
            logging.info(student)


app = webapp2.WSGIApplication([
        (LogSenderHandler.mapping()),
        ('/main',MainPageHandler)
    ],debug=True)



