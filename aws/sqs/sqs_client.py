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

.. py:module:: aws.sqs.sqs_client

Module used to provide the client for amazon Simple Queue Service api.
'''
from aws.core import aws_config
from aws.core.aws_http import AwsHttpClient
from aws.core.request_signer import AWSRequestSignerV4
from aws.sqs.sqs_domain import QueueMessage
import httplib2

class SqsClient(object):
    '''Class used to provide the OOP client for SQS service.'''
    
    SQS_API_VERSION = "2012-11-05" 
    SQS_SERVICE_NAME = "sqs"
    
    def __init__(self, region, http_client=AwsHttpClient):
        self._region = region
        self._sqs_service_host = aws_config.get_service_host(region, SqsClient.SQS_SERVICE_NAME)
        self._request_signer = AWSRequestSignerV4(aws_config.AWS_ACCESS_KEY, aws_config.AWS_SECRET_KEY, region, 
                                                  SqsClient.SQS_SERVICE_NAME)
        self._http_client = http_client(httplib2.Http)
    
    def _get_generic_headers(self):
        '''Method used to return the generic headers for sns http requests.'''
        
        return {"Cache-Control": "no-cache",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json",
                "Host": self._sqs_service_host}
        
    def _get_generic_params(self):
        '''Method used to return the generic parameters for sns requests.'''
        
        return {"Version": SqsClient.SQS_API_VERSION,
                "SignatureMethod": "AWS4-HMAC-SHA256",
                "SignatureVersion": "4"} 
    
    def get_queue_url(self, queue_name):
        '''Method used to obtain the queue url for a given queue name. If the queue name does not exist None is returned.'''
        
        action = "GetQueueUrl"
        
        params = self._get_generic_params()
        params["Action"] = action
        params["QueueName"] = queue_name
        
        headers = self._get_generic_headers()
        
        url = self._request_signer.sign_request(self._sqs_service_host, "/", params, headers, "GET")
        
        content = self._http_client.do_request(url, headers, action)
        
        return content["QueueUrl"].replace("http://%s" %self._sqs_service_host, "")
    
    def create_message(self, message):
        '''Method used to create a new message into a specified queue.
        
        :param message: The JSON message we want to push to the queue.
        :type message: :py:class:`aws.sqs.sqs_domain.QueueMessage`
        :returns: The newly created message id appended to the original message.'''
        
        action = "SendMessage"
        
        params = self._get_generic_params()
        params["Action"] = action
        params["MessageBody"] = str(message)
        
        headers = self._get_generic_headers()
        
        url = self._request_signer.sign_request(self._sqs_service_host, message.queue_url, params, headers, "POST")
        
        content = self._http_client.do_request(url, headers, action, "POST")
        
        message.msg_id = content["MessageId"]
    
    def get_messages(self, queue_url, max_messages=10):
        '''Method used to retrieve a number of messages from a given queue or None if no more messages are available.
        
        :param queue_url: The queue url from where we want to retrieve messages.
        :type queue_url: string
        :param max_messages: The maximum number of messages we want to retrieve from the queue. It mustn't be larger than 10.
        :type max_messages: int
        :returns: A list of messages from the queue.'''
        
        action = "ReceiveMessage"
        
        params = self._get_generic_params()
        params["Action"] = action
        params["MaxNumberOfMessages"] = str(max_messages)
        
        headers = self._get_generic_headers()
        
        url = self._request_signer.sign_request(self._sqs_service_host, queue_url, params, headers, "GET")
        
        result = []
        
        content = self._http_client.do_request(url, headers, action)
            
        messages = content["messages"]            
        
        for message in messages:                
            msg = QueueMessage.cast_aws_message(message)
            msg.queue_url = queue_url
            
            result.append(msg)
                
        return result
        
    def delete_messages(self, queue_url, messages):
        '''Method used to delete a given set of messages from a given queue. It returns a list of message ids that were deleted.'''
        
        action = "DeleteMessageBatch"
        
        params = self._get_generic_params()
        params["Action"] = action
        
        for i in range(len(messages)):
            message = messages[i]
            msg_key = "DeleteMessageBatchRequestEntry.%s" % (i + 1)
            
            params["%s.Id" % msg_key] = str(i+1)
            params["%s.ReceiptHandle" % msg_key] = message.receipt_handle
            
        headers = self._get_generic_headers()
        
        url = self._request_signer.sign_request(self._sqs_service_host, queue_url, params, headers, "DELETE")
        
        deleted_messages = []
        
        content = self._http_client.do_request(url, headers, action, "DELETE")
        
        content = content["Successful"]
        
        for entry in content:
            deleted_messages.append(entry["Id"])
            
        return deleted_messages