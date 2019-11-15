#!/usr/bin/python3
#
# Pull a triggered incident and push it as acknowledged or resolved.
#
# Endpoint to manage incidents in PagerDuty with user token (User API Key)
# https://api.pagerduty.com/incidents
#
# Endpoint to manage incidents in PagerDuty with Integration API Key
# https://events.pagerduty.com/v2/enqueue


from requests import request
from json import loads, dumps


pd_token = 'YOUR TOKEN HERE'
pd_url = 'https://api.pagerduty.com/incidents'
pd_user = 'YOUR USER ID'
pd_email = 'YOUR PD USER EMAIL' # User's email
pd_email_alt = 'ALTERNATIVE PD EMAIL' # Alternative email in case you need to page yourself
pd_service = 'YOUR PD SERVICE' # Service to send the page. Valid for send_page function (Not used...yet)
tz = 'America/Los_Angeles' # Timezone to display the incidents

def get_url(method, url, **kwargs):
    r = request(method, url, **kwargs)
    j = r.json()
    return j


def get_page():
    pd_load = {
            'statuses[]': ['triggered'],
            'user_ids[]': [pd_user],
            'time_zone' : tz
    }

    pd_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(pd_token),
    }
    r = get_url('GET', pd_url, params=pd_load, headers=pd_headers)
    return r


def send_page(title):
    pd_load = {
      "incident": {
        "title": title,
        "service": {
          "id": pd_service,
          "type": "service_reference"
        },
        "assignments": [{
          "assignee" : {
              "id": pd_user,
              "type": "user_reference"
          }
        }]
      }
    }

    pd_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'From': '{0}'.format(pd_email_alt),
        'Authorization': 'Token token={0}'.format(pd_token),
    }

    r = get_url('POST', pd_url, data=dumps(pd_load), headers=pd_headers)
    return r


def mod_page(id, status):
    pd_load = {
        "incidents": [
            {
            "id": id,
            "type": "incident_reference",
            "status": status
            }
        ]
    }

    pd_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'From': '{0}'.format(pd_email),
        'Authorization': 'Token token={0}'.format(pd_token),
    }

    r = get_url('PUT', pd_url, data=dumps(pd_load), headers=pd_headers)
    return r


def main():
    c = get_page() # Retrieve the current incidents

    for i in range(0,len(c['incidents'])):
        id = c['incidents'][i]['id']
        print("ACK to {0}".format(id))
        mod_page(id,"acknowledged")

main()
