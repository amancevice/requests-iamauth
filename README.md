# Requests IAMAuth

[![pypi](https://img.shields.io/pypi/v/requests-iamauth?color=yellow&logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/requests-iamauth/)
[![python](https://img.shields.io/pypi/pyversions/requests-iamauth?logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/requests-iamauth/)
[![pytest](https://img.shields.io/github/workflow/status/amancevice/requests-iamauth/pytest?logo=github&style=flat-square)](https://github.com/amancevice/requests-iamauth/actions)
[![coverage](https://img.shields.io/codeclimate/coverage/amancevice/requests-iamauth?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/requests-iamauth/test_coverage)
[![maintainability](https://img.shields.io/codeclimate/maintainability/amancevice/requests-iamauth?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/requests-iamauth/maintainability)

Use AWS SigV4 authorization with requests.

Accessing an API secured with IAM authorization in AWS API Gateway can be tricky.

This tool uses the built-in authorization strategy in `requests` to help you access your secured endpoints.

## Installation

```bash
pip install requests-iamauth
```

## Usage

### Signing Version 4

AWS [sigv4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) is the current standard for signing requests bound for AWS services.

Use `requests-iamauth` to as an authorizer for the `requests` Python library:

```python
import requests
from iamauth import Sigv4Auth

sigv4 = Sigv4Auth(
  service_name="execute-api",  # default
)

session = requests.Session()
session.auth = sigv4
session.get('https://abcdef0123.execute-api.us-east-2.amazonaws.com/my/api')
```

Override the default boto3 session by passing a custom one into the constructor for `Sigv4Auth`:

```python
import boto3

sigv4 = Sigv4Auth(
  boto3_session=boto3.Session(),
)
```

### Signing Version 4a

AWS [sigv4a](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) is an extension to the sigv4 signing process that enables signing requests bound for more than one region.

> Note — at the time of this writing, the only API Gateway API type that appears to support sigv4 are REST APIs.

Use `requests-iamauth` to as an authorizer for the `requests` Python library:


```python
import requests
from iamauth import Sigv4aAuth

sigv4a = Sigv4aAuth(
  service="execute-api",  # default
  region="*",             # default
)

session = requests.Session()
session.auth = sigv4a
session.get('https://abcdef0123.execute-api.us-east-2.amazonaws.com/my/api')
```

Override the default AWS credentials provider by passing a custom one into the constructor for `Sigv4aAuth`:

```python
from botocore.compat import awscrt

sigv4a = Sigv4aAuth(
  credentials_provider=awscrt.auth.AwsCredentialsProvider.new_default_chain(),
)
```
