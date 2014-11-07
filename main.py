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
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import users
from google.appengine.ext import db
import urllib
import urllib2
import cookielib
import httplib
import re


class LogSenderHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Recieved a message from: " + message.sender)
        # Get the body text from the e-mail

        user_email = ""
        user_branch = ""
        user_year = ""

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
          if key == 'year':
            user_year = value

          if key == 'email':
            user_email = value


          if key == 'branch':
            user_branch = value

        student.put()

        alias_list =[]
        alias_list.append(user_email)
        alias_list.append(user_branch)
        alias_list.append(user_year)
        alias_list.append('@gnu.ac.in')

        logging.info("Users new alias:"+"_".join(alias_list))

        url_1 = 'https://www.googleapis.com/admin/directory/v1/users/userKey/aliases'
        values = dict(userKey=user_email)
        data = urllib.urlencode(values)
        request = urllib2.Request(url_1,data)
        response = urllib2.urlopen(request)
        content = response.read()

        logging.info(response)





app = webapp2.WSGIApplication([
        (LogSenderHandler.mapping())
    ],debug=True)
