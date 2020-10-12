# Docker Compose as a **usable** library

The code monkey patches the docker compose.cli.main functions so that the compose CLI commands can be given programmatically, and the output is retrieved in a StringIO object.

Check the sample compose-up.py for both the patch and usage. The `run()` function allows you to define CLI like commands to be run against docker-compose.