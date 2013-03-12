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

.. py:module:: aws.sqs.sqs_domain

Module that provides the SQS domain objects.
'''
import json

class QueueMessage(object):
    '''This object is used to define how a queue message looks like. It is used in communication with AWS SQS service.'''
    
    def __init__(self, msg_id=None, receipt_handle=None, body=None, queue_url=None):
        self.msg_id = msg_id
        self.receipt_handle = receipt_handle       
        self.body = body
        self.queue_url = queue_url
    
    @staticmethod
    def cast_aws_message(message):
        '''Method used to cast an aws message from the api to a strong type queue message.'''
        
        return QueueMessage(msg_id = message["MessageId"],
                            receipt_handle = message["ReceiptHandle"],
                            body = json.loads(message["Body"]))
            
    def __str__(self):
        return json.dumps(self.body)