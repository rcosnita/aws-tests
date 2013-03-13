# AWS Tests

Currently this project contains a set of modules written in python 3 that is aiming to provide clients for AWS services.
I was quite dissapointed with Amazon decision not to provide an AWS python 3 sdk so I decide to do my best to contribute
with assets that other Python lovers can use to develop AWS empowered applications.

## License

Please read the [LICENSE](https://github.com/rcosnita/aws-tests/blob/master/LICENSE) file distributed with this software.

## Current status

The current version of this project allows to:

	* Sign aws requests using AWS Version 4 signatures [Signing spec V4](http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html)		
	* SQS simple client that allows you to:
		* Obtain a given queue url
		* Create a new message
		* Retrieve queue messages (without long polling)
		* Delete queue messages
		* See [SQS Integration tests](https://github.com/rcosnita/aws-tests/blob/master/aws/sqs/tests/itest_sqs_client.py)
	* Only json requests / responses are supported.

## Get started

In order to use client modules from this project you must:

	* Add your AWS access key / secret key into [AWS Config](https://github.com/rcosnita/aws-tests/blob/master/aws/core/aws_config.py)
	* For running SQS integration tests you must create a queue names dmsmart-integration-tests with visibility timeout set to 2 seconds.
	
## Future plan

In the near future I intend to:

	* Add a hierarchy of AWS exceptions that can be handled into code.
	* Add a generic http client so that each new client implements only the core logic for the service.
	* Add AWS S3 support.
	* Add AWS Route 53 support.
	
## Contribute

I am pretty sure many Python lovers want to use AWS into their application. If you want to contribute to this project please
feel free to do so. This is an open source project and will always remain an open source project.