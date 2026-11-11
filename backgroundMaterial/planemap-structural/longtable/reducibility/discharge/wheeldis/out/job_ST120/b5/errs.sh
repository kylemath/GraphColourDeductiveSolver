#!/bin/zsh
# print only the errors of a module log (path prefix stripped)
awk '/: error/{p=1} /: warning/{p=0} p' $1.log | sed 's#^/Users/.*/b5/##' | head -${2:-80}
