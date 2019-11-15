#!/usr/bin/python3
#
# Pull a triggered incident and push it as acknowledged.
#
# Manage incidents in PagerDuty with my user token (User API Key)
# https://api.pagerduty.com/incidents
#
# Manage incidents in PagerDuty with Integration API Key
# https://events.pagerduty.com/v2/enqueue


from time import sleep
from requests import request
from json import loads, dumps


zpd_token = 'YOUR_TOKEN'
pd_url = 'https://api.pagerduty.com/incidents'
pd_user = 'YOUR_USERID'


def get_url(method, url, **kwargs):
    r = request(method, url, **kwargs)
    j = r.json() 
    return j


def get_page():
    pd_load = {
            'statuses[]': ['triggered'],
            'user_ids[]': [pd_user],
            'time_zone' : 'America/Los_Angeles'
    }

    pd_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(zpd_token),
    }
    r = get_url('GET', pd_url, params=pd_load, headers=pd_headers)
    return r


def send_page(title):
    pd_load = {
      "incident": {
        "title": title,
        "service": {
          "id": "P4XLKS1",
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
        'From': 'YOUR_EMAIL',
        'Authorization': 'Token token={0}'.format(zpd_token),
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
        'From': 'YOUR_EMAIL',
        'Authorization': 'Token token={0}'.format(zpd_token),
    }

    r = get_url('PUT', pd_url, data=dumps(pd_load), headers=pd_headers)
    return r


c = get_page()

for i in range(0,len(c['incidents'])):
    id = c['incidents'][i]['id']
    print("ACK to {0}".format(id))
    mod_page(id,"acknowledged")
