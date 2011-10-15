# android-tools #
android-tools consists of a couple BASH scripts, **p2pkg** and **stoat** that I use to manage test builds on android devices and easily interact with multiple devices connected to adb without having to resort to using cumbersome serial numbers (a la the `adb -s` option).

## Installation ##
These scripts were developed on an OS X box, using the standard BSD utils. To install simply drop the scripts somewhere in your `$PATH`. The file devices.list will need to be readable to stoat so put it somewhere accessible. p2pkg needs to be configured to know where your test builds can be found, using the variable `$BUILDSDIR`. stoat needs to be told where devices.list can be found, using the variable `$DEVLIST`. Finally, make sure that you have the android sdk properly installed, and that `adb` is also in your `$PATH`.
The sample config file android-tools.conf should be copied to ~/.android-tools.conf. It is in this file that p2pkg and stoat will find configuration options. Check the sample for a description of the options.


## Usage ##
### p2pkg ###
p2pkg is a simple package manager that I use to manage test builds. It assumes that your builds are arranged like so:

    $BUILDSDIR/3.0.0.1/*.apk
    $BUILDSDIR/3.0.0.2/*.apk
    ...etc

`$BUILDSDIR` is configured in ~/.android-tools.conf and points to a directory containing sub-directories named as version numbers; those directories contain the test build .apk itself. p2pkg uses simple sorting, pattern matching and goo old-fashioned shell expansion to pick the right build, so it's kind of brittle. YMMV.
Basic usage is like so:

    p2pkg [options] [-t TAG] BUILD

A summary of options can be obtained by running `p2pkg -h`, but the most basic command is:

    p2pkg -n

which will identify the most recent build and install it onto the device connected to adb. If you have more than one device attached (and stoat is properly set up) you can use the `-t` option to specify a device using a tag #:

    p2pkg -t TAG -n

where `TAG` is an asset tag that is available in devices.list. Note that options do _not_ stack and must be specified individually (as in `-c -n`, but not `-cn`).

---

### stoat ###
stoat (Serial To Asset Tag) provides translation between asset tag numbers, serial numbers, and if they're available can return a human-readable string for each device (typically the device name). stoat also provides an adb wrapper which can reference devices by asset tag instead of serial number. Basic usage is:

    stoat [-l] [-n] [-s] [-e] [-f] [KEY] |  [adb [-t TAG] COMMANDS]

If `[KEY]` is passed without the `-s` option, it is assumed that it is an asset tag and will return the device's serial number if found in devices.list. If the `-s` option is supplied with `[KEY]` then it is assumed to be a serial number (or portion of a serial number) and will return the asset tag relating to the first match in devices.list.

If the `-n` option is supplied, either the asset tag or serial number (if the `-s` option is used) will be translated into a human readable name.

`-l` will output the list of devices currently found in devices.list and exit.
`-e` will open devices.list in your `$EDITOR` (default `nano`) and `-f` will sort devices.list by asset tag.

### stoat adb ###
The command `stoat adb` is where the magic happens, providing a wrapper to adb that can be used to identify devices by asset tag instead of serial numbers. The adb option does not support the previous options. Basic usage is like so:

    stoat adb [-t TAG] COMMANDS

Where you can specify a device by asset tag using the `-t` option, and then issue commands directly to adb. An example would be:

    stoat adb -t 666 get-state

Which will lookup the serial number of the device with asset tag 000666 and then pass the appropriate serial number to `adb` and issue the `get-state` command.

### devices.list ###

This is the text file that `stoat` uses to do its translation lookups. It's a simple format, using colons `:` as delimiters:

    123456:ab12cd34ef56gh78:Device Name

Where `123456` is the asset tag, `ab12cd34ef56gh78` is the serial number, and `Device Name` is the human readable-string.
Patterns are first-match only, so duplicate asset tags and serial numbers will probably be ignored and should just be avoided altogether.
