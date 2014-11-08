import database
import json
import logging
import urllib
import urllib2
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
ALIAS_URL = 'https://www.googleapis.com/admin/directory/v1/users/'

CID = (
    '172132883861-67fq6c7stn1pfm2sqe064s3hrt96c4be.apps.googleusercontent.com')
CS = 'r7SjpDxALT_Jo0qrZfSECfyv'


class LogSenderHandler(InboundMailHandler):

    def receive(self, message):
        logging.info("Recieved a message from: " + message.sender)
        # Get the body text from the e-mail

        user_email = ""
        user_branch = ""
        user_year = ""

        bodies = message.bodies('text/plain')  # generator
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

        alias_list = []
        alias_list.append(user_email)
        alias_list.append(user_branch)
        alias_list.append(user_year)
        alias_list.append('@gnu.ac.in')

        logging.info("Users new alias:"+"_".join(alias_list))

        # Google Alias Creation
        # url_1 = (
        #   'https
        # ://www.googleapis.com/admin/directory/v1/users/userKey/aliases')
        # values = dict(userKey=user_email)
        # data = urllib.urlencode(values)
        # request = urllib2.Request(url_1, data)
        # response = urllib2.urlopen(request)
        # content = response.read()

        # logging.info(response)


class AliasHandler(webapp2.RequestHandler):

    def get(self):
        access_token = GoogleAuthHandler.get_access_token()
        args = urllib.urlencode(
            dict(access_token=access_token, alias="love@gnu.ac.in")
        )
        logging.info(args)
        response = urllib2.urlopen(
            ALIAS_URL + 'love.sharma.87@gmail.com/aliases' + '?' + args)
        aliase_info = json.loads(response.read())
        response.close()
        self.response.out.write(aliase_info)


class GoogleAuthHandler(webapp2.RequestHandler):

    @staticmethod
    def get_access_token():
        """
        Returns fresh access_token from refresh_token.
        """
        token = database.Tokens.query().get()
        args = dict(
            refresh_token=token.refresh_token,
            client_id=CID,
            client_secret=CS,
            grant_type='refresh_token'
        )
        request = urllib2.Request(
            TOKEN_URL,
            urllib.urlencode(args),
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response = urllib2.urlopen(request)
        output = json.loads(response.read())
        response.close()
        logging.info(output)
        return output['access_token']

    def get_tokens(self):
        """
        Return tokens (access_token / refresh_token) and token_type as a dict.
        """
        args = dict(
            client_id=CID,
            client_secret=CS,
            code=self.request.get("code"),
            redirect_uri=self.request.path_url,
            grant_type="authorization_code"
        )
        request = urllib2.Request(
            TOKEN_URL,
            urllib.urlencode(args),
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response = urllib2.urlopen(request)
        output = json.loads(response.read())
        response.close()
        return output

    def get(self):
        code = self.request.get("code")
        logging.info(self.request.path_url)
        if code:
            tokens = self.get_tokens()
            logging.info(tokens)
            logging.info(tokens['access_token'])
            logging.info(tokens['refresh_token'])
            token_obj = database.Tokens(access_token=tokens['access_token'],
                                        refresh_token=tokens['refresh_token'])
            token_obj.put()
            self.response.out.write('success')
        else:
            args = dict(
                client_id=CID,
                redirect_uri=self.request.path_url,
                response_type="code",
                scope="https://www.googleapis.com/auth/admin.directory.user",
                access_type='offline'
            )
            encode_args = '?' + urllib.urlencode(args)
            self.redirect(AUTH_URL + encode_args)


app = webapp2.WSGIApplication([
    (LogSenderHandler.mapping()),
    ('/oauth2callback', GoogleAuthHandler),
    ('/aliase', AliasHandler),
], debug=True)
