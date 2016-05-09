"""Constants for the pyhat program """

from HTMLParser import HTMLParser
import getopt
import sys
import os
import time
import string
import cgi

#----- some constants used in verbose display ------
PASS1_MESSAGE = """
********************************
*                              *
*       STARTING PASS 1        *
*                              *
********************************
"""

PASS2_MESSAGE = """
********************************
*                              *
*       STARTING PASS 2        *
*                              *
********************************
"""

INSERTING_TOC_MESSAGE = """
********************************
*                              *
* INSERTING TABLE OF CONTENTS  *
*                              *
********************************
"""

#--- constants used  in setting defaults for options ----
DEBUGGING     = True
RUNMODE_REMOVE   = "RemoveOldTocButDoNotCreateNewToc"
RUNMODE_REPLACE  = "RemoveOldTocAndCreateNewToc"


#----- some more constants ----------------------
DEBUGGING     = True
RUNMODE_REMOVE   = "RemoveOldTocButDoNotCreateNewToc"
RUNMODE_REPLACE  = "RemoveOldTocAndCreateNewToc"
ERROR_LINES_TO_PRINT = 10
VALID_HEADING_NUMBERS = [1,2,3,4,5,6]
CLASSNAME_FOR_Toc = "table_of_contents"
CLASSNAME_FOR_Target  = "contents_item"
TARGET_ANCHOR = '<a id="%s_0"></a>' % CLASSNAME_FOR_Target
TILDES = "~"*20
TOTAL_COLUMNS = 6


# ----------------------------------------------------------------
# These variables are used as constants by the state machines.
# Since they may also be used for display,
# they are designed to be human-readable.
STATE_Background  = "background |"
STATE_Toc         = "OLD TOC    |"
STATE_Target      = "OLD TARGET |"
STATE_Heading     = "HEADING    |"
 

START_TAG         = "StartTag"
END_TAG           = "EndTag"

EVENT_StartToc    = "StartToc"
EVENT_EndToc      = "EndToc"

EVENT_StartDiv    = "StartDiv"
EVENT_EndDiv      = "EndDiv"

EVENT_StartSpan   = "StartSpan"
EVENT_EndSpan     = "EndSpan"

EVENT_StartTarget = "StartTarget"
EVENT_EndTarget   = "EndTarget"

EVENT_StartHeading  = "StartHeading"
EVENT_EndHeading    = "EndHeading"

EVENT_StartHeading1 = "StartHeading1"
EVENT_EndHeading1   = "EndHeading1"

TRIVIAL_EVENT       = "TrivialEvent"

# ----------------------------------------------------------------

optionDeepestHeading = 4
optionOutputDir    = "pyhat_out"          # default value
errorOutput = ""

TABLE_OF_CONTENTS_PLACEHOLDER = """<div class="table_of_contents">
<!-- ~~~~~~~ pyhat will place the TABLE OF CONTENTS here. ~~~~~~~~~~~~~~~~~ -->
</div>"""

#-----------------------------------------------------------
#
#     start: Function definitions
#
#-----------------------------------------------------------
def toHtmlText(argString):
	"""Convert special characters in a string to HTML elements.	"""
	return cgi.escape(argString)
	
def virtualPrint(s):
	"""add string s to the errorOutput string for CGI.
	Otherwise, just print it.
	"""
	global errorOutput
	errorOutput += (s + "\n")

	
def errorEnd():
	raise AssertionError(errorOutput)

	
def iso_date(sep = "-"):
	"""Return the current date in ISO-standard format
	"""
	year, month, day, hour, minute, second, weekday, julianday, dst = time.localtime(time.time())
	year_AsPaddedText  = string.zfill(year , 4)
	month_AsPaddedText  = string.zfill(month, 2)
	day_AsPaddedText   = string.zfill(day  , 2)
	return year_AsPaddedText +sep +month_AsPaddedText +sep +day_AsPaddedText


def iso_time(sep = ":"):
	"""Return the current time in ISO-standard format
	"""
	year, month, day, hour, minute, second, weekday, julianday, dst = time.localtime(time.time())
	hour_text_AsPaddedText   = string.zfill(hour  , 2)
	minute_text_AsPaddedText  = string.zfill(minute, 2)
	second_text_AsPaddedText  = string.zfill(second, 2)
	return  hour_text_AsPaddedText +sep +minute_text_AsPaddedText +sep +second_text_AsPaddedText


PROGRAM_INFO = """
<!--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Table of contents was automatically generated by program: pyhat.py.
Generation date/time: """ + iso_date() + " " + iso_time() + """
For more information: visit www.ferg.org/pyhat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-->
"""

def getClass(argAttrs):
	"""Extract and return the value of the "class" attribute from a list
	of (attributeName, attributeValue) pairs.  If the "class" attribute does
	not exist in the list, return None.
	"""
	return getAttr("class",argAttrs)


def getAttr(argAttrName, argAttrs):
	"""Extract and return the value of a particular attribute from a list
	of (attributeName, attributeValue) pairs.  If the attribute does
	not exist in the list, return None.
	"""
	for attr in argAttrs:
		if attr[0] == argAttrName: return attr[1]
	return None

def errorHandler(msg):
	errorMessage(msg)
	errorEnd()

def errorMessage(msg):
	virtualPrint("\n" + ("="*70))
	virtualPrint( "pyhat: Error Report")
	virtualPrint( "------------------------")
	virtualPrint( msg)
	virtualPrint( "="*70)


def dq(s):
	"""Enclose a string argument in double quotes"""
	return '"'+ s + '"'

def f_exists(f1):
	f1 = os.path.normcase(f1)
	return os.path.isfile(f1)

def d_exists(d):
	"""Return a boolean indicating whether directory d exists."""
	return os.path.isdir(d)

def d_create(d):
	"""Create a directory if it doesn't exist"""
	if d_exists(d): return
	try:
		return os.mkdir(d)
	except OSError:
		errorHandler("Attempt to create directory " + d + " failed.")
		
def getDocumentText(argInfileName):
	# Verify that argInfileName file really exits.
	if not f_exists(argInfileName):
		errorHandler("I could not find input file: " + argInfileName)

	# Read the input file into a string called aDocument
	argInfile = open(argInfileName, "r")
	aDocument = argInfile.read()
	argInfile.close()
	return aDocument

def writeOutputDocument(aDocument, argOutfileName):
	"""write the new document to the output file"""
	argOutfile = open(argOutfileName, "w")
	argOutfile.write(aDocument)
	argOutfile.close()
	return
