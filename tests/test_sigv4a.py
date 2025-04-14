from urllib.parse import urlparse, parse_qsl

import requests
from botocore.compat import awscrt

from iamauth import Sigv4aAuth


class TestIAMAuth:
    def setup_method(self):
        credentials_provider = awscrt.auth.AwsCredentialsProvider.new_static(
            access_key_id="<access-key>",
            secret_access_key="<secret-key>",
            session_token="<session-token>",
        )
        self.subject = Sigv4aAuth(credentials_provider=credentials_provider)

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
