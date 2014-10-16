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
import database
import email
import string
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class LogSenderHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Recieved a message from: " + message.sender)
        # Get the body text from the e-mail
        plaintext_bodies = message.bodies('text/plain')
        html_bodies = message.bodies('text/html')

        for content_type, body in plaintext_bodies:
            logging.info("Body = %s " % body)
            body_text = body.decode().split('\n')
            logging.info("body_text = %s " % body_text)
            #str1 = body[0][1]
            #bmsg = email.message_from_string(str1)
            #logging.info(bmsg)
            # Loop through each line in the e-mail and discard a line if it is blank
            #for line in body_text:
                #logging.info(" ")
                #if line != ',':
                    #logging.info(" ".join(body_text))

                    #logging.info()
                    #values = database.Student(database.year = year)
                    #values.put()


app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
