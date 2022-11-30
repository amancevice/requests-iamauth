import argparse

import requests

from . import __version__, Sigv4Auth, Sigv4aAuth


def get_args():
    parser = argparse.ArgumentParser(
        description="IAM-authorized HTTP request helper",
        prog="iamcurl",
        usage="%(prog)s [OPTIONS] URL",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("-d", "--data", help="Request data")
    parser.add_argument("-H", "--header", action="append", help="Request header")
    parser.add_argument("-X", "--request", help="HTTP request method")
    parser.add_argument("--sigv4", action="store_true", help="Use sigv4 algorithm")
    parser.add_argument("--sigv4a", action="store_true", help="Use sigv4a algorithm")
    parser.add_argument("URL", help="URL to request")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    IAMAuth = Sigv4aAuth if args.sigv4a else Sigv4Auth
    session = requests.Session()
    session.auth = IAMAuth()
    method = args.request or "GET"
    url = args.URL
    headers = dict(x.split(": ") for x in args.header) if args.header else {}
    result = session.request(method, url, headers=headers, data=args.data)
    return result.text


if __name__ == "__main__":  # pragma: no cover
    print(main())
