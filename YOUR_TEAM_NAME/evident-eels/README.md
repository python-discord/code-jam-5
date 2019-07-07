# Evident Eels

## Quick start

```bash
# Start a development server
$ python start_server.py
```

## Development Setup

First, export `FLASK_APP` as `module.py`, which acts as the entry point for the app.

```bash
# For Ubuntu
$ export FLASK_APP=module.py
# For Windows CMD
$ set FLASK_APP=module.py
# For Windows PowerShell
$ $env:FLASK_APP = "module.py"
```

After that's complete, the following commands are at your disposal:

```bash
# Runs a development server on localhost
$ flask run
# Starts up a Python terminal instance with our environment preloaded
$ flask shell
```
