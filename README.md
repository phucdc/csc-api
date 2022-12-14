- Clone this repo and `cd` to it

- Set environemt variable `SONAR_TOKEN` to your token

```console
$ export SONAR_TOKEN=<your_token>
```

- Install required packages (make sure `python3` and `python3-pip` installed):

```console
$ pip3 install -r requirements.txt
```

- Uhmm... create folder named `sonar` to save data:

```console
$ mkdir sonar
```

- Serve APIs with `gunicorn`(not available for Windows yet) in background:

```console
$ gunicorn -b 0.0.0.0:9000 app:app &
```