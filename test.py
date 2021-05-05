from urllib import request
from urllib.parse import urlparse, parse_qs
import urllib.error

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return


opener = request.build_opener(NoRedirect)
request.install_opener(opener)

try:
    r = request.urlopen('https://warp.plus/FRs9d')
except urllib.error.HTTPError as e:
    r = e

url = r.headers.get("location")
parsed = urlparse(url)
print(parse_qs(parsed.query)['referrer'][0])