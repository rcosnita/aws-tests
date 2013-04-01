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

.. py:module:: aws.sqs.core.tests.config

Module used to hold authentication data for aws development api.
'''
from aws.core import aws_exceptions
from aws.core.aws_exceptions_factory import AwsExceptionsFactory
import inspect
import re

#AWS_ACCESS_KEY = "Put your access key in here"
#AWS_SECRET_KEY = "Put your secret key in here"

AWS_ACCESS_KEY = "Put your access key in here"
AWS_SECRET_KEY = "Put your access key in here"
AWS_REGION = "eu-west-1"
AWS_HOSTS = {"eu-west-1": 
                {"sqs": "sqs.eu-west-1.amazonaws.com"}}

def get_service_host(region, service):
    '''Method used to return the host name for a given region and service.
    
    :param region: The amazon region for which we want to obtain the hosts.
    :type region: string
    :param service: Amazon service name for which we want to obtain the host.
    :type service: string
    :returns: The hostname found or none.'''
    
    hosts = AWS_HOSTS.get(region)
    
    if not hosts:
        return
    
    hosts = hosts.get(service)
    
    return hosts

def register_exceptions(module_obj):
    '''Method used to register all AwsGenericException subclasses.
    
    :param module_obj: Module object from which we want to import all exceptions.
    :type module_obj: module    
    '''
    
    exceptions = inspect.getmembers(aws_exceptions, 
                                   lambda obj: inspect.isclass(obj) and 
                                            issubclass(obj, aws_exceptions.AwsGenericException) and
                                            obj != aws_exceptions.AwsGenericException)    
    
    errcode_pattern = "Aws(.*)Exception"
    
    for name, ex_class in exceptions:
        err_code = re.findall(errcode_pattern, name)
        
        if len(err_code) == 0:
            continue
        
        AwsExceptionsFactory._EX_REGISTRY[err_code[0]] = ex_class