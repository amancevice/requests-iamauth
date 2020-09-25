"""
AWS IAM Authorizer.
"""
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.compat import (parse_qsl, urlparse)


class IAMAuth(requests.auth.AuthBase):
    """
    AWS IAM authorizer.

    :param boto3.Session session: Optional boto3 Session object
    :param str service_name: Optional AWS service name

    :Example:

    >>> IAMAuth()
    >>> IAMAuth(boto3.Session(), 'execute-api')
    """
    def __init__(self, boto3_session=None, service_name='execute-api'):
        self.boto3_session = boto3_session or boto3.Session()
        self.sigv4 = SigV4Auth(
            credentials=self.boto3_session.get_credentials(),
            service_name=service_name,
            region_name=self.boto3_session.region_name,
        )

    def __call__(self, request):
        # Parse request URL
        url = urlparse(request.url)

        # Prepare AWS request
        awsrequest = AWSRequest(
            method=request.method,
            url=f'{url.scheme}://{url.netloc}{url.path}',
            data=request.body,
            params=dict(parse_qsl(url.query)),
        )

        # Sign request
        self.sigv4.add_auth(awsrequest)

        # Re-add original headers
        for key, val in request.headers.items():
            if key not in awsrequest.headers:
                awsrequest.headers[key] = val

        # Return prepared request
        return awsrequest.prepare()
