#!/bin/bash

echo "$1$abadsalt$cJYsdaTkB9F9L9yH2Qjtd." > inputs.txt

/usr/sbin/john inputs.txt -wordlist=/usr/share/dict/american-english 
watch -n 60 'cat ~/.john/john.pot'

# hint, reorder the .pot file in order from the inputs. duplicate hashes are skipped.
