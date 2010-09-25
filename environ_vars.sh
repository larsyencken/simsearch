#!/bin/bash
# 
#  environ_vars.sh
#  simsearch
#  
#  Created by Lars Yencken on 2008-10-06.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 
#  Sets the necessary environment variables for foks to be run from the
#  command line. Don't run this file, instead type:
#   
#    source environmentVars.sh
#
#  from the shell. You can then run foks scripts normally.
#

# Ensure we're in the correct directory
if [ ! -d simsearch ]; then
  echo 'ERROR: cannot find foks source directory' 
  return
fi

export DJANGO_SETTINGS_MODULE='simsearch.settings'
export PYTHONPATH="$(pwd):${PYTHONPATH}"

source ss-env/bin/activate

echo 'Environment variables set'
