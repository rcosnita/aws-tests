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

.. py:module:: aws.sqs.sqs_exceptions

Module used to provide sqs custom exceptions.
'''
from aws.core.aws_exceptions import AwsGenericException

class AwsSqsInternalError(AwsGenericException):
    '''This is an error raised whenever SQS services return internal server error.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 500, error_type = error_type, 
                         error_code = "AWS.SimpleQueueService.InternalError", error_msg = error_msg, 
                         request_id = request_id)
        
class AwsSqsNonExistentQueue(AwsGenericException):
    '''This is an error raised whenever we try to access a non existent queue.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 400, error_type = error_type, 
                         error_code = "AWS.SimpleQueueService.NonExistentQueue", error_msg = error_msg, 
                         request_id = request_id)