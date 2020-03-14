# Gcode #
This page describes the RepRapFirmware supported G-codes, originally based on the information from the [http://reprap.org/wiki/G-code RepRap wiki G-code page].

This page describes the RepRapFirmware supported G-codes, originally based on the information from the http://reprap.org/wiki/G-code.

G-Codes are a widely used machine control language. They are human readable and editable. RepRapFirmware follows the philosophy of "G-code everywhere", in essence the users or external program's interaction with the firmware should be through G-codes. There are G-codes for all supported control and configuration inputs along with status and debugging information.

There are some G-Codes listed on the http://reprap.org/wiki/G-code that are not implemented in RepRapFirmware. More details can be found on the G-Codes not implemented page.

-----

# Introduction #
A typical piece of G-code sent to a machine running RepRapFirmware might look like this (The meaning of these codes (and more) is explained below on this page.)

```` G10 P0 S195 R175
T0
G1 X100 Y100 Z0.3 F3000
G1 X100.4 Y99.3 E0.23 F600
...many 1000 more lines... 
````
-----

## G-Code Everywhere ##
A design philosophy of RepRapFirmware is "G-code everywhere" what this means is explained in this sub section

The G-code can originate from a number of sources:

Sent to over USB (for example from http://www.pronterface.com/)
Sent by the Duet Web Control Web (DWC) Interface
Sent by an external controller such as the PanelDue.
In all cases the G-Code could

be entered by user one line at time, for example during configuration or testing
be sent by the User Interface (Pronterface, Web Interface or PanelDue) in response to the user pressing buttons
originate from macros that are triggered on startup, on certain events (such as error conditions), or called by the user or UI.
be from a g-code file which are normally stored on the on-board or external SD card.
A key difference from other 3d printer firmwares is not employing a separate command set (other than G-codes) to configure the printer. To that end RepRapFirmware has a large collection of configuration g-codes that allow the behaviour of the machine to be controlled. For some examples of when these G-Codes are employed have a look at these wiki pages:

Configuring RepRapFirmware for a Cartesian printer
Configuring RepRapFirmware for a Delta printer
Configuring RepRapFirmware for a CoreXY printer
Configuring RepRapFirmware for an IDEX printer
Configuring RepRapFirmware for a SCARA printer
Configuring RepRapFirmware for a Polar printer
Configuring RepRapFirmware for a Hangprinter printer
Tuning the heater temperature control
Setting up automatic probing of the print bed
Using servos and controlling unused IO pins
The advantage of "G-code everywhere" is the same commands can be send from any of the G-Code sources, and originate from the user, a UI, macro or file and it will generate the same response from the firmware. This greatly improves the ease and power of firmware configuration and operation.

-----

# G-Code Structure #
This section explains the elements that make up a G-Code command.

## Comments ##
G-Code comments begin at a semicolon, and end at the end of the line:

```` 
T0 ; This is a comment
G92 E0
''';So is this'''
G28 
````
Alternatively, comments can be enclosed in brackets, but they must start and end on the same line:

G28 (here come the axes to be homed) X Y
Comments and white space will be ignored by RepRapFirmware when executing the G-Code

## Fields ##
A RepRap G-Code is a list of fields that are separated by white spaces or line breaks. A field can be interpreted as a command, parameter, or for any other special purpose. It consists of one letter directly followed by a number, or can be only a stand-alone letter (Flag). The letter gives information about the meaning of the field (see the list below in this section). Numbers can be integers (128) or fractional numbers (12.42), depending on context. For example, an X coordinate can take integers (X175) or fractionals (X17.62), but selecting extruder number 2.76 would make no sense. In this description, the numbers in the fields are represented by nnn as a placeholder.

In RepRapFirmware 3.01 and later, instead of a number you may use an expression enclosed in braces, for example {2+2}. See GCode Meta Commands for details of the supported expression types.

In RepRapFirmware, some parameters can be followed by more than one number, with colon used to separate them. Typically this is used to specify extruder parameters, with one value provided per extruder. If only one value is provided where a value is needed for each extruder, then that value is applied to all extruders.

Letter	Meaning
Gnnn	Standard G-Code command, such as move to a point
Mnnn	RepRap-defined command, such as turn on a cooling fan
Tnnn	Select tool nnn. In RepRap, a tool is typically associated with a nozzle, which may be fed by one or more extruders.
Snnn	Command parameter, such as time in seconds; temperatures; voltage to send to a motor
Pnnn	Command parameter, such as time in milliseconds; proportional (Kp) in PID Tuning
Xnnn	A X coordinate, usually to move to. This can be an Integer or Fractional number.
Ynnn	A Y coordinate, usually to move to. This can be an Integer or Fractional number.
Znnn	A Z coordinate, usually to move to. This can be an Integer or Fractional number.
U,V,W	Additional axis coordinates
Innn	Parameter - X-offset in arc move (Not yet implemented in RepRapFirmware); integral (Ki) in PID Tuning; signal inversion
Jnnn	Parameter - Y-offset in arc move (Not yet implemented in RepRapFirmware)
Dnnn	Parameter - used for diameter; derivative (Kd) in PID Tuning; drive number
Hnnn	Parameter - used for heater number in PID Tuning
Fnnn	Feedrate in mm per minute. (Speed of print head movement)
Rnnn	Parameter - used for temperatures
Qnnn	Parameter - not currently used
Ennn	Length of filament to move through the extruder. This is exactly like X, Y and Z, but for the length of filament to consume.
Nnnn	Line number. Used to request repeat transmission in the case of communications errors. Optional
*nnn	Checksum. Used to check for communications errors. Optional
### Case sensitivity ###
The original NIST GCode standard requires gcode interpreters to be case-insensitive, except for characters in comments. However, not all 3D printer firmwares conform to this and some recognise uppercase command letters and parameters only.

RepRapFirmware version 1.19 and later is case-insensitive, except for characters within quoted strings. RepRapFirmware version 1.18 and earlier accept only uppercase letters for command and parameter letters.

### Quoted strings ###
In RepRapFirmware, quoted strings are permitted anywhere a string parameter is expected. This allows file names, WiFi passwords etc. to contain spaces, semicolons and other characters that would otherwise not be permitted. Double-quote characters are used to delimit the string, and any double-quote character within the string must be repeated.

Unfortunately, many gcode sender programs convert all characters to uppercase and don't provide any means to disable this feature. Therefore, within a quoted-string, the single-quote character is used as a flag to force the following character to lowercase. If you want to include a single quote character in the string, use two single quote characters to represent one single quote character.

Example: to add SSID MYROUTER with password ABCxyz;" 123 to the WiFi network list, use command:

```` M587 S"MYROUTER" P"ABCxyz;"" 123" ````
or if you can't send lowercase characters:

```` M587 S"MYROUTER" P"ABC'X'Y'Z;"" 123" ```` 
### Checking ###
This is an optional feature that is seldom used as g-code files are normally printed form the on-board SD card.

N: Line number

Example: N123

If present, the line number should be the first field in a line. For G-code stored in files on SD cards the line number is usually omitted.

If checking is supported, the firmware expects line numbers to increase by 1 each line, and if that doesn't happen it is flagged as an error. But you can reset the count using M110 (see below).

*: Checksum

Example: *71

If present, the checksum should be the last field in a line, but before a comment. For G-code stored in files on SD cards the checksum is usually omitted.

If checking is supported, the RepRap firmware checks the checksum against a locally-computed value and, if they differ, requests a repeat transmission of the line of the given number.

Method

Example: N123 [...G Code in here...] *71

The firmware checks the line number and the checksum.

You can leave both of these out - RepRap will still work, but it won't do checking. You have to have both or neither though.

If only one appears, it produces an error.

The checksum "cs" for a G-Code string "cmd" (including its line number) is computed by exor-ing the bytes in the string up to and not including the * character as follows:

int cs = 0;
for(i = 0; cmd[i] != '*' && cmd[i] != NULL; i++)
 cs = cs ^ cmd[i];
cs &= 0xff; // Defensive programming...
and the value is appended as a decimal integer to the command after the * character.

## Conditional execution, loops, and other command words ##
In RepRapFirmware 3.01 and later, if the line begins with a recognised keyword (optionally preceded by N and a line number, and/or space or tab characters) then that line of GCode is interpreted as a meta-command. Recognised keywords are:

abort elif else if set var while

See GCode Meta Commands for details of these commands.

A line that does not start with one of these keywords must start with command letter G, M or T or be empty apart from white space and comments.

## Multiple commands on a single line ##
RepRapFirmware allows multiple G- and M-commands to be included in a single line. Each occurrence of G or M on the line that is preceded by a space or tab character and is not inside a quoted string or a command starts a new command.

## Buffering ##
RepRapFirmware stores some commands in a ring buffer internally for execution. This means that there is no (appreciable) delay while a command is acknowledged and the next transmitted. In turn, this means that sequences of line segments can be plotted without a dwell between one and the next. As soon as one of these buffered commands is received it is acknowledged and stored locally. If the local buffer is full, then the acknowledgement is delayed until space for storage in the buffer is available. PC host programs rely on this for flow control when the controller electronics does not support device level flow control.

Only the G0 to G3 movement commands are buffered by RepRapFirmware. All other G, M or T commands are not buffered. When M555 P6 is used to select nanoDLP compatibility mode, no commands are buffered.

When an unbuffered command is received it is stored, but it is not acknowledged to the host until the buffer is exhausted and then the command has been executed.

