"""
AWS IAM Authorizer.
"""

from .sigv4 import Sigv4Auth
from .sigv4a import Sigv4aAuth  # noqa: F401

__version__ = "0.8.0"

IAMAuth = Sigv4Auth
