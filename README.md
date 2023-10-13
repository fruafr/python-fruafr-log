# python-fruafr-log
fruafr.log contain basic Python 3 logging utilities (CLI)

The focus is to log messages with a Python script (CLI).

It provides :
- a CLI to log messages to console : [logtoconsole.py](/src/fruafr/log/logtoconsole.py)
- a CLI to log messages to a file: [logtofile.py](/src/fruafr/log/logtofile.py)
- a CLI to log messages via syslog (via UDP or TCP): [logtosyslog.py](/src/fruafr/log/logtosyslog.py)

CLIs mostly expand/implement the standard python library [logging facility](https://docs.python.org/3/library/logging.html]), but log messages are emitted in a separate process (PID) rather than as a separate thread in your application. As such, if favors decoupling.

It also provides :
- a tiny UDP/TCP syslog server capable of saving incoming messages to a file: [tinysyslogserver.py](/src/fruafr/log/tinysyslogserver.py)`.
- formatter.LoggerClass, a class expanding the standard [logging.logger]() : [/lib/logger.py](/src/fruafr/log/lib/logger.py)
- formatter.FormatterClass, a class expanding the standard [logging.formatter]() : [/lib/formatter.py](/src/fruafr/log/lib/formatter.py)

## How to install

To use the CLI:
`pip install fruafr.log`

To use the tiny syslog server, you will need to install the package with sudo permissions:
`sudo pip install fruafr.log`

## How to use

Invoke the help command of each CLI with the `-h` or `--help` option.

e.g. `src\fruafr\log\logtofile.py --help`

## Implementation details

### Target
- The code has been tested on a standalone Ubuntu 22.04 LTS machine and in an Ubuntu WSL2 virtual machine.
- Python 3 only (Tested on Python 3.10).

### Requirements
- Only requires the Python standard library.

### CLI - Good to know
- The documentation of the CLI is available with the `-h` or `-help` flags.
- It accepts the standard [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes).
- It accepts the [logging levels](https://docs.python.org/3/library/logging.html#logging-levels) of the standard library
- It accept the [default templating style](https://docs.python.org/3/library/logging.html#logrecord-attributes) of the logging library with the `--format` option: `%(asctime)s`
- It provides [standard and some non-standard options](/src/fruafr/log/lib/cli_options.yaml) with the `--options` option to meet regular logging use cases: app, user, host, ip, interface, clientlevel, service. You have to provide the values with option flags to the CLI. These records will be added to the log message in the order specified with --options (e.g. `ip,message`). You can provide a custom separator for this message section with the `--optsep` option.

### Tiny SysLog Server
- **Should only be used for testing purposes**.
- It was developed to test logtosyslog.py.
- The server can listen on a single port to both UDP (`--udp` flag) and TCP (`--tcp` flag) sockets. It uses two processes (one for UDP and one for TCP).
- It could be

## Tests
[Unit tests](/tests) are available for all modules. It uses the Python unittest suite.

In addition, the UDP/TCP syslog client/server integration has been tested with an integration test found in [`tests/test_fruafr_log_syslog_client_server.py`](/tests/test_fruafr_log_syslog_client_server.py).

### Bugs reporting
[Github Issues' page of the repository](https://github.com/fruafr/python-fruafr-log/issues)

## License
[MIT licensed](LICENSE.md).
In short: Free. Do whatever you want with this library as long as you include the license notice and the copyright in the copies.

## Author
[David HEURTEVENT](https://github.com/dheurtev)

