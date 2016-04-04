=============
IonFlowScript
=============

Read Ion Torrent flow scripts controlling your sequencer's fluidics in a more friendly format, turning

::

    *	0.100	217
    *	0.000	78
    LOOPSTART
    *	2.000	78
    *	4.000	0
    LOOP	0.000	4

into output showing the time in seconds and the valves opened

::

    0.000*: Purge Degasser (3, 8) for 0.1
    0.100*: STOP / CLOSE Pressurize all Bottles (3, 2, 5, 7, 9)
    LOOPSTART
        0.100*: Pressurize all Bottles (3, 2, 5, 7, 9) for 2.0
        2.100*: All valves Closed (0) for 4.0
    LOOPEND x4

Sorry, it's not currently an editor.
I mostly guessed the specification for the files so there may be errors.
Also there are no tests.

=====
Usage
=====

Find the directory containing the fluidics scripts and function definitions.
This can be found on your PGM or by extracting the ScriptsVERSION.tar.bz2 archive
found in ``/var/www/updates`` on your Torrent Server.

::

    ionflowscript /directory/containing/scripts Script_ToAnalyse

Example Output
--------------

::

    45.250*: W2 to W4 (3, 7, 11, 13) for 5.0
Showing that at 45.25 seconds, valves 3, 7, 11 and 13 are opened for 5 seconds.

::

    15.000*: Confirm W1 Holds Pressure (5) for 30.0 		P = GET	0	P = HTARGET
        ELSE Check Wash1 for leaks.
Checks pressure in W1 and displays an error on failure.

============
Installation
============

Sorry, it's not on pip right now... but you can use pip to install it locally.

::

    git clone https://github.com/bcaller/ionflowscript.git
    pip install -e ./ionflowscript

=======
License
=======
Released under GPLv3.
Copyright 2016 Ben Caller.
Not in any way affiliated with Ion Torrent or Thermo Fisher or anyone else.