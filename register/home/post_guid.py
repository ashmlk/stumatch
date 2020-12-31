from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID
import hashlib


def uuid2slug(idstring):
    hasheduuid = hashlib.md5(idstring.encode("utf-8")).digest()
    return urlsafe_b64encode(UUID(hasheduuid).bytes).rstrip(b"=").decode("ascii")


def slug2uuid(slug):
    return str(UUID(bytes=urlsafe_b64decode(slug + "==")))
