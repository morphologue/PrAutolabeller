def request(flow):
    real_github_token = 'REPLACE_ME!'

    auth_header = flow.request.headers.get('Authorization')
    if auth_header:
        flow.request.headers['Authorization'] = auth_header.replace('__GITHUB_TOKEN_PLACEHOLDER__', real_github_token)

def response(flow):
    recording_proxy = 'http://host.docker.internal:8080'

    link_header = flow.response.headers.get('Link')
    if link_header:
        flow.response.headers['Link'] = link_header.replace('https://api.github.com', recording_proxy)

    flow.response.content = flow.response.content.replace(b'https://api.github.com', recording_proxy.encode('ascii'))
