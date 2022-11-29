import argparse
import json
import sys

import requests

from . import __version__
from . import IAMAuth


def main(args):
    session = requests.Session()
    session.auth = IAMAuth()
    method = args.request or "GET"
    url = args.URL
    result = session.request(method, url)
    return result.json()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="IAM-authorized HTTP request helper",
        prog="iamcurl",
        usage="%(prog)s [OPTIONS] URL",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("-d", "--data", help="Request data")
    parser.add_argument("-H", "--header", help="Request header")
    parser.add_argument("-X", "--request", help="HTTP request method")
    parser.add_argument("URL", help="URL to request")
    args = parser.parse_args()
    json.dump(main(args), sys.stdout)
