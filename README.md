# PagerDuty Scripts

## AutoACK.
The idea of [this script](https://github.com/jfdona23/PagerDuty/blob/master/auto_ack_pd.py) is to check if an incident has arrived to my user account and if so push an ACK (acknowledged) signal to Pagerduty to avoid the incident to auto escalate, i.e. jump to the next user oncall.
It doesn't hide any kind of notification, so you will always know when an incident is raised (via phone, web or Slack).

**Note:** *send_page* function is not in use, but if you need it you need to set a second email address in order to receive the incident as *Triggered*. Otherwise if the email of the user that pushes the API call and the paged user are the same, the incident arrives as *acknowledged*.

You only need to provide this info at the begining of the script:
```python
pd_token = 'YOUR TOKEN HERE'
pd_url = 'https://api.pagerduty.com/incidents'
pd_user = 'YOUR USER ID'
pd_email = 'YOUR PD USER EMAIL' # User's email
pd_email_alt = 'ALTERNATIVE PD EMAIL' # Alternative email in case you need to page yourself
pd_service = 'YOUR PD SERVICE' # Service to send the page. Valid for send_page function (Not used...yet)
tz = 'America/Los_Angeles' # Timezone to display the incidents
```
