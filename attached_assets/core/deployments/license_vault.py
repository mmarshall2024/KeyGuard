
from flask import request
def check_license(req):
    return req.headers.get("X-License-Key") == os.getenv("OMNI_LICENSE_KEY")
