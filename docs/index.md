
# python-fruafr-log
> fruafr.log contains basic Python 3 logging utilities (CLI)

It provides :
- a CLI to log messages to the console : [logtoconsole.py]
- a CLI to log messages to a file: [logtofile.py]
- a CLI to log messages via syslog (via UDP or TCP): [logtosyslog.py]

It also provides :
- a tiny UDP/TCP syslog server capable of saving incoming messages to a file: [tinysyslogserver.py]`.
- formatter.LoggerClass, a class expanding the standard [logging.logger] : [/lib/logger.py]
- formatter.FormatterClass, a class expanding the standard [logging.formatter] : [/lib/formatter.py]

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
[logtoconsole.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/logtoconsole.py
[logtofile.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/logtofile.py
[logtosyslog.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/logtosyslog.py
[tinysyslogserver.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/tinysyslogserver.py
[logging.logger]: https://docs.python.org/3/library/logging.html#logger-objects
[/lib/logger.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/lib/logger.py
[logging.formatter]: https://docs.python.org/3/library/logging.html#formatter-objects
[/lib/formatter.py]: https://github.com/fruafr/python-fruafr-log/blob/main/src/fruafr/log/lib/formatter.py
