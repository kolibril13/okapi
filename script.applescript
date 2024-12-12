tell application "System Events"
	
	key code 107 using {option down}
	
	delay 1
	tell window "Displays" of application process "System Settings"
		(* 
			The script below works only when the external monitor is selected.
			I was not able to select it programmatically:
				Displays are represented as buttons in `scroll area 1`,
				but nothing happens when they receive `click` command
			So, ask user for help with this and click on the proper monitor
		*)
		
		-- Give user 5 sec to click on the monitor to rotate
		set autoClose to 5
		set continueButton to "Continue (in " & autoClose & " sec)"
		set stopButton to "Stop"
		display dialog "Select monitor to rotate" giving up after autoClose buttons {stopButton, continueButton} default button continueButton cancel button stopButton
		
		-- This only works when the external monitor is selected (by default or by user)
		tell pop up button 0 of group 4 of scroll area 2 of group 0 of group 2 of splitter group 0 of group 0
			set theRotation to value of it
			click
			tell menu 1
				if theRotation = "Standard" then
					click menu item "90°"
				else
					click menu item "Standard"
				end if
			end tell
		end tell
		
		-- Confirm new display setting
		delay 1
		if exists of sheet 1 then
			click button 2 of group 0 of sheet 1
		end if
		
	end tell
end tell

delay 0.5

tell application "System Settings"
	quit
end tell