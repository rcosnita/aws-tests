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

.. py:module:: aws.core.tests.iaws_config
'''

from aws.core import aws_exceptions
from aws.core import aws_config

import unittest
import inspect
from aws.core.aws_exceptions_factory import AwsExceptionsFactory

class AwsConfigIntegrationTests(unittest.TestCase):
    '''Class used to provide a suite of test cases used to check aws config correct resources wiring
    (e.g aws specific exceptions).'''
        
    def setUp(self):
        AwsExceptionsFactory._EX_REGISTRY.clear()
        
    def test_register_exceptions_from_module(self):
        '''Test case for checking that exceptions from a given module are registered correctly.'''        
        
        expected_exceptions = inspect.getmembers(aws_exceptions, 
                                                   lambda obj: inspect.isclass(obj) and 
                                                            issubclass(obj, aws_exceptions.AwsGenericException) and
                                                            obj != aws_exceptions.AwsGenericException)
        
        self.assertGreater(len(expected_exceptions), 0, "aws_exceptions module must contain all common aws exceptions.")
        
        aws_config.register_exceptions(aws_exceptions)
        
        self.assertEqual(len(expected_exceptions), len(AwsExceptionsFactory._EX_REGISTRY.keys()))

        err_resp = {"ErrorResponse": {"Error": {"Type": "Sender", "Message": "Test", "Code": "AccessDenied"},
                                      "RequestId": "123"}}
        
        ex = AwsExceptionsFactory.get_exception(err_resp)
        
        self.assertEqual(403, ex.http_status)
        self.assertEqual("Test", ex.error_msg)
        self.assertEqual("Sender", ex.error_type)
        self.assertEqual("123", ex.request_id)