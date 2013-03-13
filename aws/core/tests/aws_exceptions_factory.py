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
.. py:module:: aws.core.tests.aws_exceptions_factory

Module used to provide the test suite for aws exceptions factory.
'''
from aws.core.aws_exceptions import AwsGenericException
from aws.core.aws_exceptions_factory import AwsExceptionsFactory
import unittest

class TestEx(AwsGenericException):    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 400, error_type = error_type, error_code = "AccessDenied", 
                         error_msg = error_msg, request_id = request_id)

class AwsExceptionsFactoryTests(unittest.TestCase):
    '''Test cases for AwsExceptionFactory capabilities.'''
    
    def setUp(self):
        AwsExceptionsFactory._EX_REGISTRY.clear()
        
        self._error_response = {"ErrorResponse": 
                                    {"Error": 
                                        {"Type": "Sender",
                                         "Code": "AccessDenied",
                                         "Message": "Test message"},
                                     "RequestId": "123"}}
    
    def test_add_exception(self):
        '''Test case for add_exception method success scenario.'''
        
        AwsExceptionsFactory.add_exception("AccessDenied", TestEx)
        
        result = AwsExceptionsFactory._EX_REGISTRY.get("AccessDenied")
        
        self.assertIsNotNone(result)
        self.assertIs(TestEx, result)
        
    def test_add_exception_exist(self):
        '''Test case for add_exception method when the code is already registered in the factory.'''
        
        AwsExceptionsFactory.add_exception("AccessDenied", TestEx)
        
        self.assertRaises(ValueError, AwsExceptionsFactory.add_exception, *["AccessDenied", TestEx])
        
    def test_get_exception_concrete(self):
        '''Test case for get exception method when a concrete exception is found.'''
        
        AwsExceptionsFactory.add_exception("AccessDenied", TestEx)
        
        for code in ["AccessDenied", "Access.Denied"]:
            self._error_response["ErrorResponse"]["Error"]["Code"] = code
            ex = AwsExceptionsFactory.get_exception(self._error_response)
            
            self.assertIsInstance(ex, TestEx)
            self.assertEqual(400, ex.http_status)
            self.assertEqual("Sender", ex.error_type)
            self.assertEqual("AccessDenied", ex.error_code)
            self.assertEqual("Test message", ex.error_msg)
            self.assertEqual("123", ex.request_id)

    def test_get_exception_generic(self):
        '''Test case for get exception method when no concrete exception is found but the error response is valid.'''
        
        ex = AwsExceptionsFactory.get_exception(self._error_response, 400)
        
        self.assertIsInstance(ex, AwsGenericException)
        self.assertEqual(400, ex.http_status)
        self.assertEqual("Sender", ex.error_type)
        self.assertEqual("AccessDenied", ex.error_code)
        self.assertEqual("Test message", ex.error_msg)
        self.assertEqual("123", ex.request_id)
        
    def test_get_exception_generic_notsuported_status(self):
        '''Test case for get exception method when no concrete exception is found and http status code is invalid < 400.'''
        
        self.assertRaises(ValueError, AwsExceptionsFactory.get_exception, *(self._error_response, None))
        self.assertRaises(ValueError, AwsExceptionsFactory.get_exception, *(self._error_response, 200))
        
    def test_get_exception_generic_noaws_response(self):
        '''Test case for get exception method when the given response is not aws compliant (does not contain ErrorResponse,
        Error and RequestId keys).        
        '''
        
        for err_resp in [None, {}, {"Invalid": ""}, {"ErrorResponse": ""}, {"ErrorResponse": {"Error": ""}}]:
            self.assertRaises(NotImplementedError, AwsExceptionsFactory.get_exception, *(err_resp, 400))