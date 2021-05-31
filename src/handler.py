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

    # Disregard non-openy type actions (especially unlabelling!)
    body = json.loads(event['body'])
    pr = body['pull_request']
    if body['action'] not in { 'opened', 'ready_for_review', 'converted_to_draft', 'reopened' }:
        print('Ignoring irrelevant action "{0}" on PR {1}'.format(body['action'], pr['url']))
        return succeed()

    # Gather required changes
    existing_labels = { label['name'] for label in pr['labels'] }
    target_labels = existing_labels.copy()
    for label, requirement in strategy_context.calc_labels(pr).items():
        if requirement:
            target_labels.add(label)
        elif label in target_labels:
            target_labels.remove(label)
    if existing_labels == target_labels:
        return succeed()

    # Make required changes
    ordered_labels = list(sorted(target_labels))
    print('Setting label(s) to "{0}" on PR {1}'.format(", ".join(ordered_labels), pr['url']))
    github.patch(pr['issue_url'], { 'labels': ordered_labels })

    return succeed()
