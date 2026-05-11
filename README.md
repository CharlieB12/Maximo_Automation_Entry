# Maximo_Automation_Entry
Compilation of scripts used for the automation of manual calibration data entry into IBM Maximo. (Pipettes, dataloggers, etc.)

**!!Sensitive and proprietary information removed for Abbott data integrity and security!!**

  **-All HTML and CSS attributes within code are standard to IBM Maximo and can be inspected from a typical browser. No Abbott specific information is displayed in this project.** 

  **-Abbott asset data and calibration records removed.**

  ------------------------------------------------------------

  **ellab_automate.py** - The Abbott Nutrition validation team uses ellab data loggers in order to log temperatures over a period of time within a manufactoring system (CIP, wet lines, etc). These probes verify the accuracy, process variables, and overall safety of production methods.
  
With hundreds of these dataloggers being used through out the year it is my job as a calibration technician to verify they are accurate and display trustworthy readings for validation, quality, and audit purposes. However, with such a large quantity of probes, testpoints, and data being collected, the manual entry into our CMMS is slow, repetetive, and prone to human error.

This script reads an excel file housing each of the ellabs used after a validation effort and 6 different calibration test points (3 as found datalogger readings, 3 verified standard readings) and enters them into IBM Maximo. It compares the readings to make sure they are within tolerance and signs off on them until the entire list is done.

This improved entry time from around 1 minute 20 seconds down to 22 seconds, a time decrease of ~70% per record, saving hours of time in manual entry.
------------------------------------------------------------------
