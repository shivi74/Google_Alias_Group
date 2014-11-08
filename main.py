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
import pickle
import httplib2
import urllib
import urllib2
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import users
from google.appengine.ext import db
from oauth2client import appengine
from oauth2client import client
from apiclient import discovery

auth_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo'

client_id='172132883861-67fq6c7stn1pfm2sqe064s3hrt96c4be.apps.googleusercontent.com'
client_secret='r7SjpDxALT_Jo0qrZfSECfyv'
scope='https://www.googleapis.com/auth/calendar'
redirect_uri='http://alias-group.appspot.com/oauth2callback'
response_type="code"
access_type=offline

service = build('directory','v1',http=http_auth)


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

        #Google Alias Creation
        #url_1 = 'https://www.googleapis.com/admin/directory/v1/users/userKey/aliases'
        #values = dict(userKey=user_email)
        #data = urllib.urlencode(values)
        #request = urllib2.Request(url_1,data)
        #response = urllib2.urlopen(request)
        #content = response.read()

        #logging.info(response)

class GoogleAuthHandler(BaseHandler):

  def get_tokens(self):
        """
        Return tokens (access_token / refresh_token) and token_type as a dict.
        """
        args = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=self.request.get("code"),
            redirect_uri=redirect_uri,
            grant_type="authorization_code"
        )
        request = urllib2.Request(
            self.token_url,
            urllib.urlencode(args),
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response = urllib2.urlopen(request)
        output = json.loads(response.read())
        response.close()
        return output

  def get(self):
      credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/admin.directory.user')
      http = credentials.authorize(httplib2.Http(memcache))
      service = build('directory','v1',http=http_auth)
      code = self.request.get("code")
      state = self.request.get("state")
      if code and state == self.session["token"]:
          logging.info("match found")
          output = self.get_tokens()
          access_token = output["access_token"]
          loggin.info(access_token)
      else:
          logging.info("match not found")
      encode_args = '?' + urllib.urlencode(decorator)
      self.redirect(auth_url + encode_args)


app = webapp2.WSGIApplication([
        (LogSenderHandler.mapping()),
        ('/google',GoogleAuthHandler),
        (decorator.callback_path, decorator.callback_handler()),
    ],debug=True)
