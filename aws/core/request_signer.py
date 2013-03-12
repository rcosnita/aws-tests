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

from urllib.request import quote
import binascii
import hashlib
import hmac
import time

def aws_quote(text_bytes):
    return quote(text_bytes, safe="").replace('%7E', '~')

class AWSRequestSignerV4(object):
    '''Class used to provide the methods for signing a request using v4 algorithm.'''
    
    def __init__(self, access_key, secret_key, region, service):
        self._access_key = access_key
        self._secret_key = secret_key
        self._region = region
        self._service = service
        
        self._request_scope = "aws4_request"
    
    def _get_credential_scope(self, request_date):
        '''Method used to obtain the credential scope string.'''
        
        credential_scope = "%s/%s/%s/%s/%s" % (self._access_key, request_date, self._region, self._service, self._request_scope)
        credential_scope = credential_scope
                
        return credential_scope
                
    def get_canonical_string(self, request_date, host, endpoint, params, headers, method, payload=""):
        '''Method used to obtain the canonical string used to sign the aws request.'''

        request_date_simple = request_date[:8]
        
        params['AWSAccessKeyId'] = self._access_key
        params['Timestamp'] = request_date
        params["X-Amz-Credential"] = self._get_credential_scope(request_date_simple)
        params["X-Amz-Algorithm"] = params["SignatureMethod"]
        params["X-Amz-Date"] = request_date
        
        # create canonical headers
        lowered_headers = {key.lower(): value.strip() for key, value in headers.items()}
        canonicalized_headers = [key + ":" + lowered_headers[key] for key in sorted(lowered_headers.keys())]
        canonicalized_headers = "\n".join(canonicalized_headers)
            
        # create signed headers
        canonicalized_signed_headers = [key for key in sorted(lowered_headers.keys())]
        canonicalized_signed_headers = ";".join(canonicalized_signed_headers)        
    
        params["X-Amz-SignedHeaders"] = canonicalized_signed_headers    
        
        # create canonical query
        canonicalized_query = [aws_quote(param) + '=' + aws_quote(params[param])
                                for param in sorted(params.keys())]
        canonicalized_query = '&'.join(canonicalized_query)
        
        payload_hasher = hashlib.sha256()
        payload_hasher.update(payload.encode())
        payload = binascii.hexlify(payload_hasher.digest())
        
        canonical_request = method + "\n" + endpoint + "\n" + canonicalized_query + "\n" + canonicalized_headers +  "\n\n" \
                            + canonicalized_signed_headers + "\n" + payload.decode()
        
        return canonical_request
    
    def get_string_to_sign(self, algorithm, request_date, canonical_request):
        '''Method used to obtain string to sign used for generating the signature.'''
        
        credential_scope = self._get_credential_scope(request_date[:8])
        credential_scope = credential_scope[credential_scope.find("/") + 1 : ]
        
        string_to_sign = [algorithm, request_date, credential_scope]
        
        hasher = hashlib.sha256()
        hasher.update(canonical_request.encode())
        canonical_request = binascii.hexlify(hasher.digest())
        
        string_to_sign.append(canonical_request.decode())
        
        return "\n".join(string_to_sign)
    
    def calculate_signature(self, request_date, host, endpoint, params, headers, method, payload="", time=time):
        '''Method used to calculate the aws v4 signature.'''
            
        algorithm = params["SignatureMethod"]
        
        canonical_request = self.get_canonical_string(request_date, host, endpoint, params, headers, method, payload)
        string_to_sign = self.get_string_to_sign(algorithm, request_date, canonical_request)
        
        request_date_simple = request_date[:8]
        
        digestmod = hashlib.sha256
        kdate = hmac.new(("AWS4" + self._secret_key).encode(), request_date_simple.encode(), digestmod).digest()
        kregion = hmac.new(kdate, self._region.encode(), digestmod).digest()
        kservice = hmac.new(kregion, self._service.encode(), digestmod).digest()
        ksigning = hmac.new(kservice, self._request_scope.encode(), digestmod).digest()
        
        signature = hmac.new(ksigning, string_to_sign.encode(), digestmod).digest()
        
        return binascii.hexlify(signature)
    
    def sign_request(self, host, endpoint, params, headers, method, payload="", time=time):
        '''Method used to sign a given request. It returns the signed url that can be used for http request.'''
        
        request_date = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        
        signature = self.calculate_signature(request_date, host, endpoint, params, headers, method, payload, time)
        
        canonical_query = [aws_quote(param) + '=' + aws_quote(params[param])
                                for param in sorted(params.keys())]
        canonical_query = '&'.join(canonical_query)

        
        return 'http://%s%s?%s&X-Amz-Signature=%s' % \
                (host, endpoint, canonical_query, aws_quote(signature))