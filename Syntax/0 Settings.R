# Settings.R 
# Inputs: 
#    - None 
# 
# Outputs: 
#    - None
# 
# Overview: 
#    - This script calls packages and creates the settings necessary for other scripts

# ------------------------------------------------------------------------------
## Load Packages ---- 
library(readr)    # Easier read/write from other formats 
library(glue)     # Easier string concatenation 
library(magrittr) # Piping functions for easier understanding 
library(openxlsx) # For outputting to Excel 
library(dplyr)    # Simplifying data wrangling 
library(rvest)    # Reading data from the web 
library(stringr)  # Easier wrangling of character strings 
library(here)     # Simplifying working with file paths 
library(purrr)    # For iterating functions 


## Set Paths ---- 
STAT19_LINK <- "https://asmc.com.au/industry-overview/statistics/weekly-crush-statistics-2019/" 
STAT18_LINK <- "https://asmc.com.au/industry-overview/2018-weekly-crushing-statistics/" 


## Create Output Path (if necessary) ---- 
if(dir.exists("supplementary_data") == FALSE) {
  dir.create("supplementary_data")
} 

