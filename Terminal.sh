#!/bin/bash
CD_CMD="cd "\\\"$(pwd)\\\"" && source kvm.sh"
VERSION=$(sw_vers -productVersion)
if (( $(expr $VERSION '<' 10.7.0) )); then
	IN_WINDOW="in window 1"
fi
osascript<<END
try
	tell application "System Events"
		if (count(processes whose name is "Terminal")) is 0 then
			tell application "Terminal"
				do script "$CD_CMD && $1" $IN_WINDOW
				activate
			end tell
		else
			tell application "Terminal"
				activate
				do script " $CD_CMD && $1"
			end tell
		end if
	end tell
end try
END