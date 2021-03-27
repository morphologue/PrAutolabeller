# PrAutolabeller

Handle GitHub PR webhook by adding labels to the PR based on the team of the author and/or the
paths changed. The mapping from team/paths to labels comes from the environment.

## Configuration
### Labels for team members
If the `TEAM_STRATEGY` variable is present in the environment, the lambda will attempt to add labels on the basis of PR authors' teams. The variable's value is formatted as follows:

        Team1=Label1,Team2=Label2,...

Nested teams are respected: if a user who is a member of both Team1 and Team2 opens a PR, the lambda will ascribe both Label1 and Label2 to the PR.

### Labels for changed paths
If the `PATH_STRATEGY` variable is present in the environment, the lambda will attempt to add labels on the basis of changed files. The variable's value is formatted as follows:

        Path1=Label1,Path2=Label2,...

The paths may include globs (e.g. `*.js=FrontEnd`). Globs don't stop at directory boundaries so `app*.js` would match `/application/files/index.js`.

Note that a leading slash is prepended to GitHub's idea of the path, so a file at the repo root can be referred to as `/file.txt`.

## Building and running the code locally

### Prerequisites
* Docker Desktop
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* To replay GitHub responses: [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/) v0.18.2 (requires WSL on Windows)
* To debug via the supplied [launch.json](.vscode/launch-json): VS Code
* To deploy: an AWS account

### Steps
1. From a shell (or Git bash on Windows) in the repo root:

        ./build.sh

    This runs `sam build`, which causes artifacts to be populated under `.aws-sam/`.

1. From a different shell (WSL on Windows):

        ./replay.sh

    This starts an HTTP server which will replay the GitHub responses under [flows/](flows/).

1. Back in the first shell:

        ./debug.sh

    This manipulates the code built in step 1 above so that a debugger can be attached.

    Then it runs `sam local invoke` to simulate a hit on the webhook using [pull_request.json](events/pull_request.json).

    **WARNING: Don't run `sam deploy` after using this script as the deployed lambda will wait forever for a debugger to be attached!**

1. Once the lambda has started it will wait for you to attach a debugger. If you are using VS Code, you can click "Play" in the Run & Debug pane.

1. Observe that the lambda interacts with the server and adds the expected labels.

Some points to note:

* If you just want to trigger the lambda locally without the ability to debug it, you can run `run.sh` instead of `debug.sh`.

* The [template.yaml](template.yaml) includes placeholder values for the GitHub signature key (GitHub->lambda) and GitHub API token (lambda->GitHub). Obviously these would need to be replaced prior to deployment in a real environment, however the events and saved responses in this repo use the placeholder values for your debugging convenience.

* The GitHub responses were recorded by using a script similar to [record.sh](record.sh).

## Permissions
The GitHub token configured for the Lambda must have `repo` and `read:org` scopes.

Only the `pull_request` event needs to be forwarded to the lambda: it will ignore all other events.

## Caveats
* The lambda can only add _existing_ labels to a PR. You can make a label in the web UI via `https://github.com/{owner}/{repo}/issues/labels`, e.g. https://github.com/morphologue/PrAutolabeller/issues/labels.

* To prevent unnecessary updates (especially when removing labels!), the lambda will only respond to the `opened`, `ready_for_review` and `reopened` actions.

* Drafts are wholly ignored because they are an antifeature.
