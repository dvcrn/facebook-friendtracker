# Friendtracker
facebook-friendtrackr is a simple facebook application for logging and archiving facebook friends.

Friendtracker notifies a user if a friend from their friendlist went missing or if a new one decides to join.

#### Freeper?
Freeper was the internal name of friendtrackr

## Setup
Friendtracker runs on heroku with the cloud in mind.

Add ``sendgrid`` (for error mail delivery) and ``mongohq`` to your heroku app.

In addition, set the following keys

```
AWS_ACCESS_KEY_ID:          xxxxx
AWS_SECRET_ACCESS_KEY:      xxxxx
BUILDPACK_URL:              https://github.com/ddollar/heroku-buildpack-multi.git
FACEBOOK_APP_ID:            123
FACEBOOK_APP_SECRET:        abc
```

If you want the automatic notifier, add a heroku scheduler with `python manage.py sync_and_notify`