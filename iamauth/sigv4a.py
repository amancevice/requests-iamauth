"""
IAMAuth using Signatuve v4a signing process.
"""
from io import BytesIO

from botocore.awsrequest import AWSRequest
from botocore.compat import awscrt, parse_qsl, urlsplit
from requests.auth import AuthBase


class Sigv4aAuth(AuthBase):
    """
    AWS IAM authorizer for sigv4a.

    This implementation owes a lot to the blog post here:
    https://chammock.dev/posts/aws-apigw-multi-region-iam-auth/

    :param boto3.Session session: Optional boto3 Session object
    :param str service_name: Optional AWS service name

    :Example:

    >>> IAMAuth()
    >>> IAMAuth("execute-api")
    >>> IAMAuth("execute-api", "us-*")
    >>> IAMAuth("execute-api", "us-*", my_credentials_provider)
    """

    def __init__(self, service=None, region=None, credentials_provider=None):
        self.service = service or "execute-api"
        self.region = region or "*"
        self.credentials_provider = (
            credentials_provider
            or awscrt.auth.AwsCredentialsProvider.new_default_chain()
        )

    def __call__(self, request):
        # Parse request URL
        url = urlsplit(request.url)

        # Prepare AWS request
        aws_url = f"{url.scheme}://{url.netloc}{url.path}"
        aws_headers = dict(request.headers)
        aws_params = dict(parse_qsl(url.query))
        aws_request = AWSRequest(
            method=request.method,
            url=aws_url,
            headers=aws_headers,
            data=request.body,
            params=aws_params,
        )

        # Prepare CRT request
        crt_host = request.headers.get("host", url.netloc)
        crt_headers = awscrt.http.HttpHeaders([("host", crt_host)])
        crt_path = url.path or "/"
        crt_body_stream = BytesIO(request.body) if request.body else None
        crt_request = awscrt.http.HttpRequest(
            method=request.method,
            path=crt_path,
            headers=crt_headers,
            body_stream=crt_body_stream,
        )

        # Setup signing config
        signing_config = awscrt.auth.AwsSigningConfig(
            algorithm=awscrt.auth.AwsSigningAlgorithm.V4_ASYMMETRIC,
            signature_type=awscrt.auth.AwsSignatureType.HTTP_REQUEST_HEADERS,
            credentials_provider=self.credentials_provider,
            region=self.region,
            service=self.service,
        )

        # Sign CRT request and merge headers into AWS request
        awscrt.auth.aws_sign_request(crt_request, signing_config).result()
        signed_headers = dict(crt_request.headers)
        aws_request.headers = {**aws_headers, **signed_headers}

        # Return prepared AWS request
        return aws_request.prepare()
