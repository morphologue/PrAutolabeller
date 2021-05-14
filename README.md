# PrAutolabeller
Add labels to GitHub PRs based on the team of the author and/or the paths changed.

## Configuration
### Labels for team members
If the `TEAM_STRATEGY` variable is present in the environment, the lambda will attempt to add labels on the basis of PR authors' teams. The variable's value is formatted as follows:

        Team1=Label1,Team2=Label2,...

Nested teams are respected: if a user who is a member of both Team1 and Team2 opens a PR, the lambda will ascribe both Label1 and Label2 to the PR.

If the user is _not_ a member of a specified team, but the team's label was added manually, the lambda will remove the incorrect label.

For drafts, all team-based labels will be removed, always.

### Labels for changed paths
If the `PATH_STRATEGY` variable is present in the environment, the lambda will attempt to add labels on the basis of changed files. The variable's value is formatted as follows:

        Path1=Label1,Path2=Label2,...

The paths may include globs (e.g. `*.js=FrontEnd`). Globs don't stop at directory boundaries so `app*.js` would match `/application/files/index.js`.

Note that a leading slash is prepended to GitHub's idea of the path, so a file at the repo root can be referred to as `/file.txt`.

If a PR does _not_ alter a certain path, but the path's label was added manually, the lambda will remove the incorrect label.

For drafts, all path-based labels will be removed, always.

### Constant labels
If the `CONST_STRATEGY` variable is present in the environment, the lambda will either add (=`true`) or remove (=`false`) the labels specified therein:

        true=Label1,false=Label2,true=Label3

For drafts, all specified labels will be removed irrespective of `true` or `false`.

### Disambiguation
If a label should be both added and removed via different strategies (or by its repeated configuration for the one strategy), then the label will be
_added_ rather than removed.

## Building and running the code

### Requirements
* Docker
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* To replay GitHub responses: [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/) v6.0.2 (requires WSL and dos2unix on Windows)
* To debug via the supplied [launch.json](.vscode/launch.json): VS Code
* To deploy: an AWS account

### Steps to debug locally
1. From a shell (WSL on Windows):

        dos2unix replay.sh  # If you encounter line ending issues on Windows
        ./replay.sh

    This starts an HTTP server which will replay the GitHub responses under [mitmproxy/](mitmproxy/).

1. In VS Code, choose the "PR" profile from the Launch & Debug pane and click "play".

1. Observe that the lambda interacts with the HTTP replay and sets the expected labels.

Some points to note:

* The [template.yaml](template.yaml) includes placeholder values for the GitHub signature key (GitHub->Lambda) and GitHub API token (Lambda->GitHub). Obviously these would need to be replaced prior to deployment in a real environment, however the events and saved responses in this repo use the placeholder values for your debugging convenience.

* The GitHub responses were recorded using [record.sh](record.sh).

### Steps to deploy to AWS
1. Configure the default AWS account to have admin permissions.
2. From a shell:

        sam build --use-container
        sam deploy

## GitHub Permissions
The GitHub token configured for the Lambda must have `repo` and `read:org` scopes.

Only the `pull_request` event needs to be forwarded to the lambda: it will ignore all other events.

## Caveats
* The lambda can only add _existing_ labels to a PR. You can make a label in the web UI via `https://github.com/{owner}/{repo}/issues/labels`, e.g. https://github.com/morphologue/PrAutolabeller/issues/labels.

* To prevent unnecessary updates (especially when removing labels!), the lambda will only respond to the `opened`, `ready_for_review`, `convert_to_draft` and `reopened` actions.

* Labels can only be removed from drafts because drafts are an antifeature.

## Licence
This software is licensed under the [MIT licence](LICENSE).
