#!/bin/bash

git ls-remote --tags https://danila_vershinin@bitbucket.org/tildeslash/monit.git | cut -d$'\t' -f2 | sort -V | tail -n 1 | cut -d'/' -f3 | cut -d^ -f1 | sed 's@release-@@g' | sed 's@-@.@g'
