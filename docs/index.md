
# python-fruafr-log
> fruafr.log contains basic Python 3 logging utilities (CLI)

The focus is to log messages with a Python script (CLI). The CLIs mostly expand/implement the standard python library [logging facility](https://docs.python.org/3/library/logging.html]), but log messages are emitted in a separate process (PID) rather than as a separate thread in your application. Thus, if favors decoupling.

It provides :
- a CLI to log messages to the console : [logtoconsole.py](/src/fruafr/log/logtoconsole.py)
- a CLI to log messages to a file: [logtofile.py](/src/fruafr/log/logtofile.py)
- a CLI to log messages via syslog (via UDP or TCP): [logtosyslog.py](/src/fruafr/log/logtosyslog.py)

It also provides :
- a tiny UDP/TCP syslog server capable of saving incoming messages to a file: [tinysyslogserver.py](/src/fruafr/log/tinysyslogserver.py)`.
- formatter.LoggerClass, a class expanding the standard [logging.logger]() : [/lib/logger.py](/src/fruafr/log/lib/logger.py)
- formatter.FormatterClass, a class expanding the standard [logging.formatter]() : [/lib/formatter.py](/src/fruafr/log/lib/formatter.py)

## How to install

To use the CLI:
`pip install fruafr.log`

To use the tiny syslog server, you will need to install the package with sudo permissions:
`sudo pip install fruafr.log`

## Contents

```{toctree}
:maxdepth: 2

Overview <readme>
Contributions & Help <contributing>
License <license>
Authors <authors>
Changelog <changelog>
Module Reference <api/modules>
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

[Sphinx]: http://www.sphinx-doc.org/
[Markdown]: https://daringfireball.net/projects/markdown/
<!-- [reStructuredText]: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html -->
[MyST]: https://myst-parser.readthedocs.io/en/latest/
