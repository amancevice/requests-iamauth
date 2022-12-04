from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from iamauth import __main__ as index


class TestIAMCURL:
    def setup_method(self):
        index.get_args = MagicMock()
        index.requests.Session = MagicMock()

    @pytest.mark.parametrize("req,url", [("GET", "https://example.com/path")])
    def test_main(self, req, url):
        index.get_args.return_value = SimpleNamespace(
            data=None,
            header=[],
            request=req,
            sigv4a=False,
            URL=url,
        )
        index.main()
        index.requests.Session.return_value.request.assert_called_once_with(
            "GET",
            "https://example.com/path",
            headers={},
            data=None,
        )
