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

```python
import requests
from iamauth import IAMAuth

session = requests.Session()
session.auth = IAMAuth()
session.get('https://abcdef0123.execute-api.us-east-2.amazonaws.com/my/api')
```

Override the default boto3 session by passing a custom one into the constructor for `IAMAuth`:

```python
import boto3

boto3_session = boto3.Session()
session.auth = IAMAuth(boto3_session)
```
