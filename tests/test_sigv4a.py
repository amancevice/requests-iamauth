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
