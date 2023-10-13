# Change Log

All notable changes to the fruafr.log project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.0] - 2023-10-13

### Added
- Initial version of fruafr.log
- a CLI to log messages to console
- a CLI to log messages to a file
- a CLI to log messages via syslog (via UDP or TCP)
- a tiny UDP/TCP syslog server capable of saving incoming messages to a file:
- logger.LoggerClass, a class expanding the standard
- formatter.FormatterClass, a class expanding the standard
