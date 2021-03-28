import os
import hmac
import json
import github
import strategy_context

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
        print('Successfully handled event "{0}"'.format(github_event_name))
        return { 'statusCode': 204 }
    if github_event_name != 'pull_request':
        return succeed()

    # Disregard drafts and non-openy type actions (especially unlabelling!)
    body = json.loads(event['body'])
    pr = body['pull_request']
    if pr['draft']:
        print('Ignoring draft {0}'.format(pr['url']))
        return succeed()
    if body['action'] not in { 'opened', 'ready_for_review', 'reopened' }:
        print('Ignoring irrelevant action "{0}" on PR {1}'.format(body['action'], pr['url']))
        return succeed()

    # Gather required labels.
    desired_labels = strategy_context.calc_labels(pr)
    existing_labels = { label['name'] for label in pr['labels'] }
    new_labels = desired_labels.difference(existing_labels)
    if not len(new_labels):
        return succeed()
    final_labels = list(sorted(desired_labels.union(existing_labels)))

    # Finally, add new labels
    print('Setting label(s) to "{0}" on PR {1}'.format(", ".join(final_labels), pr['url']))
    github.patch(pr['issue_url'], { 'labels': final_labels })

    return succeed()
