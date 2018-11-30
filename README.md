# Jithub
A github to jira integration server

The goal of the server is to improve the integration between Jira and Github by providing options not available such as acting upon tag addition/deletion.

## Disclaimer

This is very much a work in progress at the moment.

However it is working and usable as is and I will do my best to keep it like this.

## Usage

### Requirements :
- Python 3.6+
- A working JIRA Cloud instance and an [application link](https://confluence.atlassian.com/adminjiraserver071/using-applinks-to-link-to-other-applications-802592232.html) with oauth authentication
- A ssh key
- A github Token

### Step 1 :
- `mv config.json.sample config.json`
- Replace default values with your own
- `python oauthflow.py`
- Follow the instructions

At this point you should have an oauth token and a secret for this token.

### Step 2 :

##### Option 1:
*This is the best option for testing your configuration locally*

- Set up a [ngrok](https://ngrok.com/) account
- Download ngrok
- On your machine:
	- `<path-to-ngrok>/ngrok http 34567`
	- `PORT=34567 python <path-to-jithub>/server.py`
- Set up a webhook in github that send events to the ngrok address

You're all set, Github will start sending events to the Jithub server. Every event that is not yet implemented will result in a `501`.

##### option 2:
*This is the best option if you want Jithub for a production setup*

###### Requirements:

- Any Docker environment: Docker for mac, Vagrant...
- An account for a service capable of running docker images: Heroku, AWS, GCP...


###### Building the image:

- `cd <path-to-jithub>`
- `docker build -t <fancy-name> .`

Now you have a working docker image. I wont cover all the steps to run this images into all the available services but here is a Heroku how-to:

- `heroku login`
- `heroku create`
- `heroku container:login`
- `heroku container:push web`
- `heroku container:release web`

Now you have Jithub running in heroku under the address given at step 2.

You can set up a github webhook to send events to that address.
