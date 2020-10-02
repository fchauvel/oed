# How to update the documentation

This documentation is powered by [Docute](https://docute.org/), a
simple JavaScript file that dynamically serves markdown files.



The whole documentation is located in (and served from) the `docs`
folder.

## Viewing the Documentation Locally

To serve it locally, simply serve the `docs` folder using your
favourite HTTP server. For instance, in Python you can use the
command:

```shell-session
$ cd docs
$ python -m http.server
Serving HTTP on :: port 8000 (http://[::]:8000/) ...

Keyboard interrupt received, exiting.
::1 - - [02/Oct/2020 09:02:46] "GET / HTTP/1.1" 200 -
::1 - - [02/Oct/2020 09:02:46] "GET /README.md HTTP/1.1" 200 -
::1 - - [02/Oct/2020 09:02:46] code 404, message File not found
::1 - - [02/Oct/2020 09:02:46] "GET /favicon.ico HTTP/1.1" 404 -
::1 - - [02/Oct/2020 09:02:49] "GET /install.md HTTP/1.1" 200 -


```
