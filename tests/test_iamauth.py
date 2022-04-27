import boto3
import requests

from iamauth import IAMAuth


class TestIAMAuth:
    def setup(self):
        self.boto3_session = boto3.Session(
            aws_access_key_id='<access>',
            aws_secret_access_key='<secret>',
            region_name='us-east-2',
        )
        self.subject = IAMAuth(boto3_session=self.boto3_session)

    def test_call(self):
        req = requests.Request(
            'GET',
            'http://example.com/',
            auth=self.subject,
            headers={'Content-Type': 'application/json; charset=utf-8'},
        )
        prq = req.prepare()
        assert 'X-Amz-Date' in prq.headers
        assert 'Authorization' in prq.headers
