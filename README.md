- Clone this repo and `cd` to it

- Set environemt variable `SC_TOKEN` to your token

```console
$ export SC_TOKEN=<your_token>
```


- Set environemt variable `SC_ORGANIZATION` to your token

```console
$ export SC_ORGANIZATION=<your_organization_name>
```

- Install required packages (make sure `python3` and `python3-pip` installed):

```console
$ pip3 install -r requirements.txt
```

- Uhmm... create folder named `data` to save data:

```console
$ mkdir data
```

- Serve APIs with `uvicorn` in background:

```console
$ uvicorn app:app --host 0.0.0.0 --port 9000 &
```
