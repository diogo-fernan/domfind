from traceback import format_exc

from requests import get as requests_get

from domfind.common import color, out, rw
from domfind.core import meta

__timeout = 60

__header = {'Accept': '*/*',
            'User-Agent': f"{meta.DOMFIND_NAME} {meta.DOMFIND_URL}",
            'Connection': 'close'}


def _request(uri, path):
    try:
        res = requests_get(uri, headers=__header, timeout=60)
        out.debug("res.headers", obj=dict(res.headers))
        res.raise_for_status()
    except Exception as e:
        out.warn(f"HTTP error: {e}\n{color.red(format_exc())}")
    else:
        out.debug(f"HTTP {res.status_code} \"{res.reason}\" -- \"{uri}\"")

        if res.status_code == 204 or res.headers.get("Content-Length") == 0:
            out.error(f"HTTP {res.status_code} \"{res.reason}\""
                      f" -- \"{uri}\": no content")

        rw.writef(path, res.content)
        out.info(f"updated \"{path}\""
                 f", last modified on \"{res.headers.get('Last-Modified')}\"")


def update():
    _request(meta.IANA_TLD_URL, meta.IANA_TLD_FILE)
    _request(meta.INTERNIC_ROOT_URL, meta.INTERNIC_ROOT_FILE)
