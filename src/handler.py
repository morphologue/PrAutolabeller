import json

def handle(event, context):
    """Handle GitHub PR webhook by adding labels to the PR based on the team of the author and/or
    the paths changed. The mapping from team/paths to labels comes from the environment.
    """

    return {
        "statusCode": 200,
        "body": json.dumps(event),
    }
