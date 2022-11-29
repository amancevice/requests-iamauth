from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from iamauth.__main__ import main, requests


class TestIAMCURL:
    def setup_method(self):
        requests.Session = MagicMock()

    @pytest.mark.parametrize("req,url", [("GET", "https://example.com/path")])
    def test_main(self, req, url):
        args = SimpleNamespace(request=req, URL=url)
        main(args)
        requests.Session.return_value.request.assert_called_once_with(
            "GET", "https://example.com/path"
        )
