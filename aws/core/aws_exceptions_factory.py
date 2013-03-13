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
.. py:module:: aws.core.aws_exceptions_factory
'''
from aws.core.aws_exceptions import AwsGenericException

class AwsExceptionsFactory(object):
    '''This class provides an elegant way to convert an AWS json error response to a concrete exception. Each new exception
    that we want to be available to this factory must be added to it. Below you can find an example of how this is achieved:
    
    .. code-block:: python
        
        from aws.core.aws_exceptions_factory import AwsExceptionsFactory
        
        AwsExceptionsFactory.add_exception("AccessDenied", AwsAccessDenied)
        
        access_ex = AwsExceptionsFactory.get_exeception(
                                {"ErrorResponse" : 
                                    {"Error": {"Type": "Sender", 
                                               "Code": "AccessDenied", 
                                               "Message": "Access denied by AWS."}},
                                    "RequestId": "ef3aba6a-dc84-4937-91bf-cef2ddd6775a"})
    '''
    
    _EX_REGISTRY = {}
    
    @staticmethod
    def add_exception(code, ex_cls):
        '''Method used to assign an aws error code to a concrete exception class.
        
        :param code: AWS Error code.
        :type code: string
        :param ex_cls: Concrete exception class.
        :type ex_cls: type
        '''
        
        existing_ex_cls = AwsExceptionsFactory._EX_REGISTRY.get(code) 
        
        if existing_ex_cls is not None:
            raise ValueError("Error code %s is already binded to error type %s." % (code, existing_ex_cls))
        
        AwsExceptionsFactory._EX_REGISTRY[code] = ex_cls
        
    @staticmethod
    def get_exception(err_resp, http_status=None):
        '''Method used to convert a json error response to a AWS exception type.
        
        :param err_resp: JSON error response retrieved from an AWS request.
        :type err_resp: JSON
        :param http_status: The http status used in case AwsGenericException instance is retrieved.
        :type http_status: int
        :returns: A concrete AwsGenericException exception or an AwsGenericException for unknow error codes.
        :rtype: :py:class:`aws.code.aws_exceptions.AwsGenericException`
        :raises: ValueError in case there is no way to obtain an AwsGenericException instance.
        :raises: NotImplementedError in case the given json object is not amazon compatible. 
        '''
        
        if not err_resp or not err_resp.get("ErrorResponse") or not err_resp["ErrorResponse"].get("Error") or \
            not err_resp["ErrorResponse"].get("RequestId"):
            raise NotImplementedError("The given error response %s is not an aws valid error response." % err_resp)
        
        ex_content = err_resp["ErrorResponse"]["Error"]
        request_id = err_resp["ErrorResponse"]["RequestId"]
        
        ex_code = ex_content.get("Code") 
        ex_type = ex_content.get("Type")
        ex_msg = ex_content.get("Message")
        
        ex_cls = AwsExceptionsFactory._EX_REGISTRY.get(ex_code)
        
        if ex_cls:
            return ex_cls(error_type = ex_type, error_code = ex_code, error_msg = ex_msg, request_id = request_id)
        
        if http_status is None or int(http_status) < 400:
            raise ValueError("Http status code %s does not indicate an error." % http_status)
            
        return AwsGenericException(http_status = http_status, error_type = ex_type, error_code = ex_code, 
                                    error_msg = ex_msg, request_id = request_id)