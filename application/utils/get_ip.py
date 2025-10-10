from flask import Request


def get_ip(request: Request) -> str:
    if request.headers.getlist("X-Forwarded-For"):
        # todo make sure this is what I want and not just the first element
        return ", ".join(request.headers.getlist("X-Forwarded-For"))
        # return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr
