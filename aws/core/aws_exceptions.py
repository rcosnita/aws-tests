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
.. py:module:: aws.core.aws_exceptions
'''

class AwsGenericException(Exception):
    '''This is the base class for every exception thrown by AWS services. It is recommended to work with concrete
    exceptions rather than this.
    
    .. code-block:: python
    
        # let's imagine we want to obtain a queue name in our code and we want to handle only access denied exceptions.
        from aws.sqs.sqs_client import SqsClient
        
        try:
            sqs_client = SqsClient("eu-west-1")
            queue_name = sqs_client.get_queue_url("test-queue")
        except AwsAccessDeniedException as ex:
            # handle your exception in here.
    ''' 
    
    def __init__(self, http_status, error_type, error_code, error_msg, request_id):
        self.http_status = http_status
        self.error_type = error_type
        self.error_code = error_code
        self.error_msg = error_msg
        self.request_id = request_id
        
class AwsAccessDeniedException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when authentication failed.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 403, error_code = "AccessDenied", error_msg = error_msg, request_id = request_id)
        
class AwsAuthFailureException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when authentication failed.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 401, error_code = "AuthFailure", error_msg = error_msg, request_id = request_id)
        
class AwsConflictingQueryParameterException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when some query parameters are mutual exclusive.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 400, error_code = "ConflictingQueryParameter", error_msg = error_msg, 
                         request_id = request_id)
        
class AwsInternalErrorException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when an internal server error occured.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 500, error_code = "InternalError", error_msg = error_msg, 
                         request_id = request_id)
        
class AwsInvalidAccessKeyIdException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when an invalid access key was provided.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 401, error_code = "InvalidAccessKeyId", error_msg = error_msg, 
                         request_id = request_id)
        
class AwsInvalidActionException(AwsGenericException):
    '''This is a generic AWS exception thrown by all services when an invalid action was specified.'''
    
    def __init__(self, error_type, error_msg, request_id):
        super().__init__(http_status = 400, error_code = "InvalidAction", error_msg = error_msg, 
                         request_id = request_id)