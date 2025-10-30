#######################################
## The3DP                            ##
## Expected Finish Date:             ##
##  11/8/2025                        ##
## Goal: Make a corrected            ##
## calculator using bare Python      ##
## based on corrections/improvements ##
## from 'Calc-v1.0'                  ##
#######################################

###=================================== PSEUDOCODE =========================================##
##BEGIN SMART_CALCULATOR                                                                   ##                                                                 
##                                                                                         ##
##    IMPORT math module                                                                   ##
##                                                                                         ##
##    DEFINE allowed_names AS dictionary of math functions and constants                   ##
##        (exclude anything that starts with "__")                                         ##
##                                                                                         ##
##    PRINT welcome messages and usage examples                                            ##
##                                                                                         ##
##    LOOP forever:                                                                        ##
##        PROMPT user for an expression                                                    ##
##                                                                                         ##
##        IF expression is "exit" OR "quit":                                               ##
##            PRINT goodbye message                                                        ##
##            BREAK the loop                                                               ##
##                                                                                         ##
##        TRY:                                                                             ##
##            IF expression ends with "d)":                                                ##
##                REPLACE "d)" with "*(pi/180))" to convert degrees to radians             ##
##                                                                                         ##
##            EVALUATE expression using only allowed_names (safe eval)                     ##
##            PRINT the result                                                             ##
##                                                                                         ##
##        EXCEPT if an error occurs:                                                       ##
##            PRINT an error message with the exception details                            ##
##                                                                                         ##
##    END LOOP                                                                             ##
##                                                                                         ##
##END PROGRAM                                                                              ##
###========================================================================================##
