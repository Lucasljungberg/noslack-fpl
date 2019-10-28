# noslack-fpl

## Usage
This repo is written with and for `python >3.5`.

I've used f-strings because they're great and so no filthy `python2.x`
casuals can run it.

### Install
First, activate virtual environment if you've got one:

```
$ . /path/to/environment/env/activate
(env) $
```

Use `pip` to install requirements:

```
(env) $ pip install -r requirements.txt
```

### Start development server
This will start the development server with live-reload.

```
(env) $ export FLASK_ENV=development
(env) $ python -m server
```
