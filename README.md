# Python-Application-Updater
A simple Updater for Applications using Python

#Note: "Python Application" refers to the application you are using the updater to update. It does not need to be a "Python" Application
Usage.

Copy foder "updater" to your application path.
Set "updater.ini" To the web address and name of your updater.

app = the exe of the Python Application
path = The Full Path to your Python Application with a trailing \
url = the url of your site containint the update information
php = The php file (or html) of your webpage containing the version number.

##------------------------
	Notes:

	url:
	This should be the location of both your php/html file and zip file of the update
	e.g: http://mysite.com/updater/
	The Script will try find http://mysite.com/updater/ini_php.php and http://mysite.com/updater/0.0.0.0.zip

	php:
	This should only have the unformatetd version number.
	<? php echo "0.0.0.0" ?>
	The application will compare the version from the Python Application exe to the version on the php

	See the Default ini for examples of the format.
##------------------------

Copy Python Applicaiton Build into a zip file named "0.0.0.0.zip" (change to your build exe verions number) 
##------------
	To find only changed files use "utils/buildcalc.py"
##------------


If you are making a Python applicaiton add the following code.
#--------------
import sys, os, subprocess
##finds the directory of your application
if getattr(sys, 'frozen', False): #windows path fix
	exe_path = os.path.dirname(sys.executable)
elif __file__:
	exe_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
	if len(sys.argv) > 1: ##app will be run with "True" as a sys.argv, after the updater is complete. This will skip running the updater
		##do your code here
	elif os.path.isdir(exe_path+"\\updater"): ##app can find the "updater" folder
		if os.path.isfile(exe_path+"\\updater\\updater.exe"): ##app can find the "updater.exe" file
			subprocess.Popen(exe_path+"\\updater\\updater.exe")
	else: ##there is no "True" argv and the updater.exe cannot be found. Skipping the Updater process
		print("no marker and no updater")
		##same code here
#--------------	
	
Python Application Proecess:
-> Python Applicaition Start.
-> Checks for any sys.argv options. (this will need to be changed if you are using sys.argv in your application)
-> If sys.argv is set:
-->Run Python Application as Normal
-> Else If "updater" folder and "updater.exe" file exist:
--> Run "updater.exe"
-> Else:
-->Run Python Application as Normal

Updater Process:
-> Checks "updater.ini" 
-> Checks version from ini url+php
-> If version > current exe version:
--> Sets Permission on Application Path. (requires Administrator and only runs if permissions are not set)
--> Downloads new version from ini url+version+".zip"
--> Overwrights files in Application Path with files from version.zip
--> Runs Python Application
-> else:
--> Runs Python Applicaition
