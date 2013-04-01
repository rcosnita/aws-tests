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

.. py:module:: aws.sqs.tests.itest_sqs_client

Module used to provide sqs integration tests.
'''
from aws.core import aws_config
from aws.core.request_signer import AWSRequestSignerV4
from aws.sqs.sqs_client import SqsClient
from aws.sqs.sqs_domain import QueueMessage
import unittest
from nose.plugins.skip import SkipTest

class SqsClientSanityCheck(unittest.TestCase):
    '''This class provides the test cases that ensure that sqs client works correctly.'''

    SERVICE = "sqs"
    QUEUE_NAME = "dmsmart-integration-tests"
    QUEUE_URL = None
    QUEUE_REGION = "eu-west-1"
    REQUEST_SIGNER = AWSRequestSignerV4(aws_config.AWS_ACCESS_KEY, aws_config.AWS_SECRET_KEY, aws_config.AWS_REGION, SERVICE) 
    
    @classmethod
    def setUpClass(cls):
        '''Method used to setup global dependencies for test cases.'''
        
        if aws_config.AWS_ACCESS_KEY == "Put your access key in here" or \
            aws_config.AWS_SECRET_KEY == "Put your secret key in here":
            raise SkipTest("This will be executed only if you provide valid AWS access / secret keys.")
        
        sqs_client = SqsClient(cls.QUEUE_REGION)
        
        cls.QUEUE_URL = sqs_client.get_queue_url(cls.QUEUE_NAME)
        
        host = aws_config.get_service_host(cls.QUEUE_REGION, cls.SERVICE)
        
        assert cls.QUEUE_URL is not None
        assert not cls.QUEUE_URL.startswith("http://%s" % host)
        assert cls.QUEUE_URL.endswith(cls.QUEUE_NAME)
    
    def setUp(self):
        '''Method invoked automatically in order to set up all test cases dependencies.'''
        
        self._sqs_client = SqsClient(SqsClientSanityCheck.QUEUE_REGION)
        
    def test_sqs_create_message(self):
        '''Test case that checks new messages can be created using sqs client.'''
        
        message_body = {"message1": {"name": "Test", "body": "Junk"}}
        message = QueueMessage(body = message_body, 
                               queue_url = SqsClientSanityCheck.QUEUE_URL)
        
        self._sqs_client.create_message(message)
        
        self.assertIsNotNone(message.msg_id)
    
    def test_sqs_receive_message(self):
        '''Test case that checks messages retrieval from the queue.'''
        
        num_messages = 2
        
        added_messages = []
        
        message_body = {"message1": {"name": "Test", "body": "Junk"}}
        
        # push a number of messages to the queue.
        for i in range(0, num_messages):
            message = QueueMessage(body = message_body, 
                                   queue_url = SqsClientSanityCheck.QUEUE_URL)
         
            self._sqs_client.create_message(message)
            
            added_messages.append(message.msg_id)
        
        # retrieve first two messages added
        # we request 3 messages done because one message belongs to create_message success test.
        messages = self._sqs_client.get_messages(SqsClientSanityCheck.QUEUE_URL, num_messages) 
        
        self.assertEqual(len(messages), num_messages)
                
    def test_sqs_delete_message(self):
        '''Test case that checks messages deletion from the queue.'''
        
        num_messages = 2
        
        added_messages = []
        
        message_body = {"message1": {"name": "Test", "body": "Junk"}}
        
        # push a number of messages to the queue.
        for i in range(0, num_messages):
            message = QueueMessage(body = message_body, 
                                   queue_url = SqsClientSanityCheck.QUEUE_URL)
         
            self._sqs_client.create_message(message)
            added_messages.append(message.msg_id)
        
        messages = self._sqs_client.get_messages(SqsClientSanityCheck.QUEUE_URL, num_messages)

        self.assertGreater(len(messages), 0)
        
        deleted_messages = self._sqs_client.delete_messages(SqsClientSanityCheck.QUEUE_URL, messages)
        
        self.assertEqual(len(messages), len(deleted_messages))