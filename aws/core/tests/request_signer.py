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

.. py:module:: aws.core.request_signer
'''

from aws.core.request_signer import AWSRequestSignerV4
import unittest

class RequestSignerTests(unittest.TestCase):
    '''Class used to provide all test cases for aws request signer v4.'''
    
    def setUp(self):
        self._request_date = "20130311T065530Z"
        self._aws_access_key = "AKIDEXAMPLE"
        self._aws_secret_key = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"

        self._signer = AWSRequestSignerV4(self._aws_access_key, self._aws_secret_key, "eu-west-1", "sqs")
        
    def test_get_canonical_request(self):
        '''Test case for making sure that canonical request is calculated correctly.'''
        
        expected_result = """\
GET
/083512914311/test-email-queue/
AWSAccessKeyId=AKIDEXAMPLE&Action=ReceiveMessage&SignatureMethod=AWS4-HMAC-SHA256&SignatureVersion=4&Timestamp=20130311T065530Z&Version=2012-11-05&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIDEXAMPLE%2F20130311%2Feu-west-1%2Fsqs%2Faws4_request&X-Amz-Date=20130311T065530Z&X-Amz-SignedHeaders=accept%3Bcontent-type%3Bhost
accept:application/json
content-type:application/json
host:sqs.eu-west-1.amazonaws.com

accept;content-type;host
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""
        
        host = "sqs.eu-west-1.amazonaws.com"
        uri = "/083512914311/test-email-queue/"
        
        params = {"Action": "ReceiveMessage",
                  "Version": "2012-11-05",
                  "SignatureMethod": "AWS4-HMAC-SHA256",
                  "SignatureVersion": "4"}
        
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                   "Host": host}
                
        result = self._signer.get_canonical_string(self._request_date, host, uri, params, headers, "GET", "")
        
        self.assertEqual(expected_result, result)
        
    def test_get_string_to_sign(self):
        '''Test case for get string to sign method.'''
        
        expected_result = """\
AWS4-HMAC-SHA256
20130311T065530Z
20130311/eu-west-1/sqs/aws4_request
5053172eccdced5d2111bddacf11d0a2903d8d26625677039e72bdd92073dd48"""

        canonical_request = """\
GET
/083512914311/test-email-queue/
AWSAccessKeyId=AKIDEXAMPLE&Action=ReceiveMessage&SignatureMethod=AWS4-HMAC-SHA256&SignatureVersion=4&Timestamp=20130311T065530Z&Version=2012-11-05&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIDEXAMPLE%2F20130311%2Feu-west-1%2Fsqs%2Faws4_request&X-Amz-Date=20130311T065530Z&X-Amz-SignedHeaders=accept%3Bcontent-type%3Bhost
accept:application/json
content-type:application/json
host:sqs.eu-west-1.amazonaws.com

accept;content-type;host
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""

        algorithm = "AWS4-HMAC-SHA256"
        request_date = self._request_date
        
        result = self._signer.get_string_to_sign(algorithm, request_date, canonical_request)        
        
        self.assertEqual(expected_result, result)