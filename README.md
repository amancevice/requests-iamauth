# Requests IAMAuth

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
