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
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        bodies = message.bodies('text/html')

        allBodies = u"";

        for body in bodies:
            try:
                allBodies = allBodies + unicode(errors="ignore")
            except:
                pass

        if not allBodies:
            bodies = message.bodies('text/plain')
            for body in bodies:
                try:
                    allBodies = allBodies + unicode(errors="ignore")
                except:
                    pass

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
