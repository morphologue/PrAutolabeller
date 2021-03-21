import os
import hmac
import json

def handle(event, context):
    """Handle GitHub PR webhook by adding labels to the PR based on the team of the author and/or
    the paths changed. The mapping from team/paths to labels comes from the environment.
    """

    # Check GitHub's signature
    expected_dig = 'sha256=' + hmac.new(
        os.environ['SIGNATURE_KEY'].encode('utf-8'),
        event['body'].encode('utf-8'),
        'sha256').hexdigest()
    if not hmac.compare_digest(event['headers'].get('X-Hub-Signature-256', ''), expected_dig):
        return { 'statusCode': 401, 'body': 'Unauthorized' }
    
    # Disregard events except pull_request
    github_event_name = event['headers'].get('X-GitHub-Event', '')
    def succeed():
        print('Successfully handled event {0}'.format(github_event_name))
        return { 'statusCode': 204 }
    if github_event_name != 'pull_request':
        return succeed()

    # Disregard drafts
    body = json.loads(event.body)
    pr_url = body['pull_request']['url']
    if body['pull_request']['draft']:
        print('Ignoring draft {0}'.format(pr_url))
        return succeed()
    
    user_url = body['pull_request']['user']['url']
    print('The user URL is {0}'.format(user_url))

    return succeed()
