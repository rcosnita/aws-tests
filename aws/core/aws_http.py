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

.. py:module:: aws.sqs.core.aws_http

Module used to provide a smart http client that can easily execute signed requests against AWS services.
'''
import json
from aws.core.aws_exceptions_factory import AwsExceptionsFactory

class AwsHttpClient(object):
    '''Class used to provide an aws http client that can easily handle exceptions and cast them to 
    strong type exceptions.'''
    
    def __init__(self, http_module):
        self._http_module = http_module
    
    def do_request(self, url, headers, action, method="GET"):
        '''Method used to execute an aws http request. In case an exception occurs an aws strong type exception is thrown.
        Otherwise the json response is returned.
        
        :param url: The AWS SQS url we want to invoke through http.
        :type url: string
        :param headers: A dictionary containing all signed headers we want to send to aws.
        :type headers: dict
        :param action: The sqs action we are currently invoking against SQS. It is used for extracting only useful part of 
        the response.
        :type action: string
        :param method: The HTTP method used for invoking the url.
        :type method: string
        :returns: json
        :except: :py:class:`aws.core.aws_exceptions.AwsGenericException`
        '''
        
        request = self._http_module()
        resp, content = request.request(url, method, headers=headers)
        
        if resp.status >= 400:
            err_resp = json.loads(content.decode())
            
            raise AwsExceptionsFactory.get_exception(err_resp)
        
        if not content:
            return {}
        
        content = json.loads(content.decode())
        
        return content["%sResponse" % action]["%sResult" % action]