'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>
.. py:module:: aws.ses.itest_ses_smtp
'''

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from smtplib import SMTP
import os
from email.mime.text import MIMEText

class AwsSmtpProvider(object):
    '''Method used to provide an email provider for aws smtp interface.'''
    
    HOST = 'email-smtp.us-east-1.amazonaws.com'
    PORT = 25
    
    USERNAME = 'Put your smtp username'
    PASSWORD = 'Put your smtp password'
    
    def __init__(self):
        self._smtp = SMTP()
    
    def _build_html_message(self, from_addr, to_addr, subject, body):
        '''Method used to build a html message object that also contains attachments.'''
        
        assert type(to_addr) == list
        
        msg = MIMEMultipart("alternative")
        msg["From"] = from_addr
        msg["To"] = COMMASPACE.join(to_addr)
        msg["Date"] = formatdate(localtime = True)
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "html"))
                
        return msg        
    
    def _build_raw_message(self, from_addr, to_addr, subject, body, files):
        '''Method used to build a message object that also contains attachments.'''
        
        assert type(to_addr) == list
        assert type(files) == list
        
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = COMMASPACE.join(to_addr)
        msg["Date"] = formatdate(localtime = True)
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body))
        
        for file in files:
            part = MIMEBase("application", "octet-stream")
            
            with open(file, "rb") as f: 
                part.set_payload(f.read())
                
            encoders.encode_base64(part)
            
            part.add_header("Content-Disposition", "attachment; filename=%s" % os.path.basename(file))
            
            msg.attach(part)
        
        return msg
        
    def send_mail(self):
        '''Method used to send a dummy mail through aws smtp interface.'''
        
        files = ["/home/rcosnita/tmp/photos/100_users_2min_rampup.png"]
        from_addr = "radu.cosnita@gmail.com"
        to_addr = ["radu.cosnita@gmail.com"]
        subject = "Non html message"
        body = """\
<html>
    <head></head>
    
    <body>
        <h1>Simple body that also has attached files.</h1>
    </body>
</html>"""
        
        try:
            self._smtp.connect(AwsSmtpProvider.HOST, AwsSmtpProvider.PORT)
            self._smtp.starttls()
            self._smtp.login(AwsSmtpProvider.USERNAME, AwsSmtpProvider.PASSWORD)
            
            msg = self._build_html_message(from_addr, to_addr, subject, body)
            
            self._smtp.sendmail(from_addr, to_addr, msg.as_string())
        finally:        
            self._smtp.quit()

if __name__ == "__main__":
    email_provider = AwsSmtpProvider()
    
    email_provider.send_mail()