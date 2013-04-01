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

.. py:module:: aws.sqs.core.tests.aws_http
'''
from aws.core.aws_exceptions import AwsGenericException
from aws.core.aws_exceptions_factory import AwsExceptionsFactory
from aws.core.aws_http import AwsHttpClient
from mock import Mock
import json
import unittest

class TestEx(AwsGenericException):
    '''Just a mocked exception used in unit tests.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 403, error_type = error_type, error_code = "TestEx", 
                         error_msg = error_msg, request_id = request_id)    

class AwsHttpClientTests(unittest.TestCase):
    '''Class used to provide all test cases for aws http client.'''
    
    def setUp(self):
        AwsExceptionsFactory._EX_REGISTRY.clear()
        
        AwsExceptionsFactory.add_exception("TestEx", TestEx)
        
        self._http_cls = Mock()
        self._http_module = Mock(return_value=self._http_cls)
        self._http_client = AwsHttpClient(self._http_module)
        
    def test_do_request_exception(self):
        '''Test case for checking that an http error response is correctly converted to a strong type exception.'''
        
        url = "/aws/test"
        headers = {"Content-Type": "application/json"}
        action = "TestAction"
      
        resp = Mock()
        resp.status = 403
        
        content = {"ErrorResponse": {"Error": 
                                            {"Code": "TestEx", "Type": "Sender", "Message": "Test"}, 
                                          "RequestId": "123"}}
        
        self._http_cls.request = lambda url, method, headers: (resp, json.dumps(content).encode())
        
        self.assertRaises(TestEx, self._http_client.do_request, *[url, headers, action, "GET"])
        
    def test_do_request_no_ex(self):
        '''Test case for checking that a response is correctly retrieved when no error occurs.'''
        
        url = "/aws/test"
        headers = {"Content-Type": "application/json"}
        action = "Simple"
        
        resp = Mock()
        resp.status = 200
        
        content = {"SimpleResponse": {"SimpleResult": "Cool stuff"}}
        
        self._http_cls.request = lambda url, method, headers: (resp, json.dumps(content).encode())
        
        response = self._http_client.do_request(url, headers, action)
        
        self.assertIsNotNone(response)
        self.assertEquals("Cool stuff", response)
        
    def test_do_request_no_body(self):
        '''Test case for checking that a response is correctly retrieved when no body is returned.'''
        
        url = "/aws/test"
        headers = {"Content-Type": "application/json"}
        action = "TestAction"
        
        resp = Mock()
        resp.status = 201

        self._http_cls.request = lambda url, method, headers: (resp, None)
        
        response = self._http_client.do_request(url, headers, action, "POST")
        
        self.assertIsNotNone(response)
        self.assertEquals({}, response)