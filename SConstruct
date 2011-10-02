# -*- coding: utf-8 -*-
#
#  SConstruct
#  simsearch
# 
#  Created by Lars Yencken on 27-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Build instructions for the stroke similarity extension."
"""

#----------------------------------------------------------------------------#

import os
from distutils import sysconfig

#----------------------------------------------------------------------------#

# Default include path for python, version inspecific.
#scons_python_version = sysconfig.get_config_var('VERSION')
scons_python_version = '2.7'
python_version = ARGUMENTS.get('python') or scons_python_version 

print 'Using Python %s' % python_version

#----------------------------------------------------------------------------#

def check_libraries(env):
    """ Check whether the correct libraries exist, and thus whether building
        is possible.
    """
    # Detect OS X python installation, and attempt to correct for it.
    if os.uname()[0] == 'Darwin':
        env.Replace(SHLINKFLAGS='$LINKFLAGS -bundle -flat_namespace -undefined suppress')
        env.Replace(SHLIBSUFFIX='.so')
        if os.path.isdir('/opt/local'):
            env.Append(
                    LIBPATH=['/opt/local/lib'],
                    CPPPATH=['/opt/local/include']
                )

    # Detect the presence of necessary dependencies.
    conf = Configure(env)

    if not conf.CheckLibWithHeader('m', 'math.h', 'c'):
        print "Can't find standard math libraries."
        Exit(1)

    if not conf.CheckLibWithHeader('python%s' % python_version,
            'Python.h', 'c'):
        print "Can't find python %s." % python_version
        Exit(1)

    env = conf.Finish()

    return env

#----------------------------------------------------------------------------#
# CONFIGURATION
#----------------------------------------------------------------------------#

# Set up the compilation environment.
env = Environment(
        CPPPATH=sysconfig.get_python_inc().replace(scons_python_version,
                python_version),
        LIBPATH=[sysconfig.get_config_var('LIBPL').replace(
                scons_python_version, python_version)],
        SHLIBPREFIX='',
        LIBS=['python%s' % python_version],
    )

environmentVars = (
        'CPATH',
        'LD_LIBRARY_PATH',
        'LIBRARY_PATH',
        'PATH',
        'PYTHONPATH',
    )

envDict = env['ENV']
for var in environmentVars:
    if var in os.environ:
        envDict[var] = os.environ[var]

# Choose between debugging or optimized mode.
if ARGUMENTS.get('debug'):
    print 'Using debug targets'
    env.Replace(DEBUG=True, CXXFLAGS='-O0 -g -Wall ', CFLAGS='-O0 -g -Wall ')
else:
    print 'Using optimised targets'
    env.Replace(DEBUG=False, CXXFLAGS='-O3 -DNDEBUG -Wall ',
           CFLAGS='-O3 -DNDEBUG -Wall ')

# Configure the environment.
env = check_libraries(env)

pyxbuild = Builder(action='cython -o $TARGET $SOURCE')
env.Append(BUILDERS={'Cython': pyxbuild})

#----------------------------------------------------------------------------#

SConscript('simsearch/SConscript', exports='env')

#----------------------------------------------------------------------------#
