#!/bin/bash

echo "$1$abadsalt$cJYsdaTkB9F9L9yH2Qjtd." > inputs.txt

/usr/sbin/john inputs.txt 2&1 > /dev/null
watch -n 60 'cat ~/.john/john.pot'
