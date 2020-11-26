# demo-address-alerts

A web app which enables users to set up email notifications in response to transaction activity 
to a set of configured addresses. This is a [Django](https://djangoproject.com) application written in 
Python 3.8. 

* [View the Demo](https://address-alerts.herokuapp.com/)
* [Powered by Blockset](https://blockset.com)

### Functionality

Anonymous users are able to associate a series of addresses with their email address, which will
become a [Webhook Subscription](https://docs.blockset.com/api/v1/subscriptions) on Blockset that
calls into this app. Users are required to confirm their subscription via a link sent to their 
email to reduce potential for unwanted notifications.

### Project Layout

Some notable files:

* `/app/blockset.py` - a [requests](https://requests.readthedocs.io/en/master/) powered Blockset API Client
* `/app/models.py` - the data model, note that we persist every webhook invocation verbatim
* `/app/views.py` - our class-based view controllers. Protects alerts with a token only visible in emails.

### How to run

* Uses Blockset for blockchain data and webhooks. Set the `BLOCKSET_TOKEN` environment variable to your client token.
* Uses Mailgun as the email provider. Set the `MAILGUN_API_KEY` and `MAILGUN_SENDING_DOMAIN` environment variables.
* Uses Postgres as the backend databse. Set `DATABSE_URL` to point to a Postgres database.
* (Optional) Uses Sentry as the error reporter. Set the `SENTRY_DSN` environment variable.
* If hosting a production version, set `HOSTNAME` to your current host name.
* Likewise, if hosting a production version, set `SECRET_KEY` to a long random string. 

### Credits & License

* Written by [Samuel Sutch](https://github.com/samuraisam)
* Licensed under the MIT License