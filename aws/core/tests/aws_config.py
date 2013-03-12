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

.. py:module:: aws.core.aws_config
'''

from aws.core import aws_config
import unittest

class AwsConfigTests(unittest.TestCase):
    '''Class that provides all test cases for checking that aws config module works as expected.'''
    
    def test_get_service_host_found(self):
        '''Test case for ensuring that hosts can be found for existing regions and services.'''
        
        host_name = aws_config.get_service_host("eu-west-1", "sqs")
        
        self.assertEqual("sqs.eu-west-1.amazonaws.com", host_name)
        
    def test_get_service_host_notfound(self):
        '''Test case for ensuring that None is returned when host can not be found.'''
        
        self.assertEqual(None, aws_config.get_service_host(None, None))
        self.assertEqual(None, aws_config.get_service_host("not found", None))
        
        self.assertEqual(None, aws_config.get_service_host("eu-west-1", None))
        self.assertEqual(None, aws_config.get_service_host("eu-west-1", "not found"))