from urllib.parse import urlparse, parse_qsl

import boto3
import requests

from iamauth import Sigv4Auth


class TestSigv4Auth:
    def setup_method(self):
        self.boto3_session = boto3.Session(
            aws_access_key_id="<access>",
            aws_secret_access_key="<secret>",
            region_name="us-east-2",
        )
        self.subject = Sigv4Auth(boto3_session=self.boto3_session)

    def test_call(self):
        req = requests.Request(
            "GET",
            "http://example.com/",
            auth=self.subject,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        prq = req.prepare()
        assert "X-Amz-Date" in prq.headers
        assert "Authorization" in prq.headers

    def test_call_with_query_params(self):
        req = requests.Request(
            "GET",
            "http://example.com/",
            auth=self.subject,
            params={"singleValueParam": "val1", "multiValueParam": ["val2", "val3"]},
        )
        prq = req.prepare()
        query = urlparse(prq.url).query
        assert parse_qsl(query) == [
            ("singleValueParam", "val1"),
            ("multiValueParam", "val2"),
            ("multiValueParam", "val3"),
        ]
