---
title: T
tags: [T-Commands] 
keywords: beta 
last_updated: April 02, 2020 
summary: Select Tool
permalink: T.html
toc: false 
---


### Parameters

* `nnn`: Tool number to select. A negative number deselects all tools.
* `R1`: Select the tool that was active when the print was last paused (firmware 1.20 and later)
* `Pnnn`: Bitmap of all the macros to be run (dc42 build 1.19 or later and ch fork 1.17b or later)
* Tool number

## Examples

* ` T0 ; select tool  ` 0
* ` T1 P0 ; select tool 1 but don't run any tool change macro  ` files
* T-1 P0 ; deselect all tools but don't run any tool change macro files
* T R1 ; select the tool that was active last time the print was paused
* T ; report the current tool number

If T''n'' is used to select tool ''n'' but that tool is already active, the command does nothing. Otherwise, the sequence followed is:

* If another tool is already selected and all axes have been homed, run macro tfree#.g where # is the number of that tool
* If another tool is already selected, deselect it and set its heaters to their standby temperatures (as defined by the R parameter in the most recent ` G10 command for that  ` tool)
* If all axes have been homed, run macro tpre#.g where # is the number of the new tool
* Set the new tool to its operating temperatures specified by the S parameter in the most recent ` G10 command for that  ` tool
* If all axes have been homed, run macro tpost#.g where # is the number of the new tool. Typically this file would contain at least a ` M116 command to wait for its temperatures to  ` stabilise.
* Apply any X, Y, Z offset for the new tool specified by G10
* Use the new tool.

Selecting a non-existent tool (100, say) just does Steps 1-2 above<sub>1</sub>. That is to say it leaves the previous tool in its standby state. You can, of course, use the ` G10 command beforehand to set that standby temperature to anything you  ` like.

After a reset tools will not start heating until they are selected. You can either put them all at their standby temperature by selecting them in turn, or leave them off so they only come on if/when you first use them. The ` M0, M1 and M112 commands turn them all off. You can, of course, turn them all off with the M1 command, then turn some back on again. Don't forget also to turn on the heated bed (if any) if you use that  ` trick.

Tool numbering starts at 0 by default however ` M563 allows the user to specify tool numbers, so with them you can have tools 17, 99 and 203 if you want. Negative numbers are not  ` allowed.

## Notes

<sub>1</sub> Selecting a non-existent tool also removes any X/Y/Z offset applied for the old tool.

<sub>2</sub> Under special circumstances, the execution of those macro files may not be desired. RepRapFirmware 1.19 or later supports an optional P parameter to specify which macros shall be run. If it is absent then all of the macros above will be run, else you can pass a bitmap of all the macros to be executed. The bitmap of this value consists of tfree=1, tpre=2 and tpost=4.

Note that you may wish to include a move to a parking position 'within the tfreeN.g gcode macro in order to allow the new extruder to reach temperature while not in contact with the print.

