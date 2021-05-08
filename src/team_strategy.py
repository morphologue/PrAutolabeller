import github
from urllib.parse import urlparse
from requests import exceptions
from strategy_base import StrategyBase

class TeamStrategy(StrategyBase):
    def __init__(self, config):
        super().__init__(config)

    def calc_labels(self, pr):
        basic = super().calc_labels(pr)
        if basic != None:
            return basic

        label_requirements = []
        parsed = urlparse(pr['url'])
        orgs_url = '{0}://{1}/user/orgs'.format(parsed.scheme, parsed.netloc)
        for org in github.get(orgs_url):
            for team_slug, label in self.config:
                membership_url = '{0}/teams/{1}/memberships/{2}'.format(org['url'], team_slug, pr['user']['login'])
                try:
                    membership = github.get(membership_url)
                    # The other possible state is "pending", which means the user has not
                    # accepted the invitation to join the team yet.
                    requirement = membership['state'] == 'active'
                except exceptions.HTTPError as ex:
                    # This API returns 404 if the user is not in the team.
                    if ex.response.status_code != 404:
                        raise
                    requirement = False
                label_requirements.append((label, requirement))

        return label_requirements
