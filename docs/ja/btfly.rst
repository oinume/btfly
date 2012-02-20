:orphan:

.. highlight:: bash

btfly manual page
=================

SYNOPSIS
--------

**btfly** [*options*] command

DESCRIPTION
-----------
TODO:

COMMANDS
--------
TODO:

env
^^^
TODO:

csv
^^^
TODO:

hosts
^^^^^
TODO:

tomahawk_hosts
^^^^^^^^^^^^^^
TODO:

tomahawk_hosts_file
^^^^^^^^^^^^^^^^^^^
TODO:


OPTIONS
-------
These programs follow the usual GNU command line syntax, with long options starting with two dashes ('--').
A summary of options is included below.
For a complete description, see the Info files.

[-h] [-c CONF] [-H HOSTS_CONF] [-s STATUSES] [-r ROLES]
             [-f FIELD] [-o OUTPUT_FILE] [-D]

-c, --conf
^^^^^^^^^^
TODO:

-H, --hosts-conf
^^^^^^^^^^
TODO:

-s, --statuses
^^^^^^^^^^
TODO:

-r, --roles
^^^^^^^^^^^
TODO:

-f, --field
^^^^^^^^^^^
TODO:

-o, --output-file
^^^^^^^^^^^^^^^^^
TODO:

-D, --debug
^^^^^^^^^^^
TODO:

-h, --hosts
^^^^^^^^^^^
Specifies host names for sending commands. You can specify multiple hosts with ','.

-f, --hosts-files
^^^^^^^^^^^^^^^^^
Specifies hosts files which listed host names for sending commands.
You can specify multiple hosts files with ','.

Format of hosts file is below. ::

  web01
  web02
  #web03
  web04

A line of starting with '#' disables a host.

-l, --prompt-login-password
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prompts a password for ssh authentication at first. If the password is all the same between target hosts, you'll input a password just once.

-s, --prompt-sudo-password
^^^^^^^^^^^^^^^^^^^^^^^^^^
Prompts a password for sudo explicitly. If the password is all the same between target hosts,
you'll input a password just once.
If commands include "sudo", tomahawk asks sudo password automatically.

-c, --continue-on-error
^^^^^^^^^^^^^^^^^^^^^^^
Continues to send commands even if any errors.
The default behavior is fail-safe, means that tomahawk will stop if any errors.

-p, --parallel
^^^^^^^^^^^^^^
Specifies a number of processes for parallel command execution. (default: 1)
If your machine has many cpu cores, --parallel 2 .. N might be faster.

-t, --timeout
^^^^^^^^^^^^^
Specifies timeout seconds for a command.

--expect-timeout
^^^^^^^^^^^^^^^^
Duplicated. Use t (-timeout) instead.

-u, --ssh-user
^^^^^^^^^^^^^^
Specifies ssh user. The default is a current logged in user.

-o, --ssh-options
^^^^^^^^^^^^^^^^^
Specifies ssh options.

--output-format
^^^^^^^^^^^^^^^
Specifies command output format.
The default is '${user}@${host} % ${command}\n${output}\n'


SEE ALSO
--------
* :manpage:`tomahawk-rsync(1)`
* :manpage:`ssh(1)`
* :manpage:`scp(1)`
