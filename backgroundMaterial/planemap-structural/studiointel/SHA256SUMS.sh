#!/bin/sh
cd "$(dirname "$0")"; shasum -a 256 graphs.py builders.py radius.py search.py check.py regress.sh
