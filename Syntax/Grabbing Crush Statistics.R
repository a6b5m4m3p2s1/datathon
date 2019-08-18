# Grabbing Crush Statistics 
# Inputs: 
#    - None: draws data from the web. 
# 
# Outputs: 
#    - Weekly crush statistics in XLSX, CSV and RDS formats, in a supplementary_data
#      subfolder. 
# 
# Overview: 
#    - This script takes the data in the 2018 and 2019 crush statistics and 
#      outputs them in Excel format, also in CSV and RDS. 

# ------------------------------------------------------------------------------
## Preliminaries ---- 
## Load Packages 
library(readr)    # Easier read/write from other formats 
library(glue)     # Easier string concatenation 
library(magrittr) # Piping functions for easier understanding 
library(openxlsx) # For outputting to Excel 
library(dplyr)    # Simplifying data wrangling 
library(rvest)    # Reading data from the web 
library(stringr)  # Easier wrangling of character strings 
library(here)     # Simplifying working with file paths 


## Set Paths 
STAT19_LINK <- "https://asmc.com.au/industry-overview/statistics/weekly-crush-statistics-2019/" 
STAT18_LINK <- "https://asmc.com.au/industry-overview/2018-weekly-crushing-statistics/" 


## Create Output Path (if necessary) 
if(dir.exists("supplementary_data") == FALSE) {
  dir.create("supplementary_data")
} 


# ------------------------------------------------------------------------------
## Retrieve 2019 Crush Statistics ---- 
crushstats19 <- read_html(STAT19_LINK)               # Explore the webpage 
tables19 <- html_nodes(crushstats19, "table")        # Identify tables 
crush19 <- html_table(tables19[[1]], header = FALSE) # Retrieve the table 
## The headers are in row 3, need to set this row as column names and then drop three rows. 
## Final row is also not data 
## But first, two columns have the same row... 

crush19[3, 6] <- "to_date_crush_pc" # overwrite row 3, column 6, with this string 

names(crush19) <- crush19[3, ] # Names are crush19, row 3, all columns 
crush19 <- crush19[-c(1:3, 15), ]  # crush19 is crush19, without rows 1:3, and 15 


## Retrieve 2018 Crush Statistics ---- 
crushstats18 <- read_html(STAT18_LINK)               # Explore the webpage 
tables18 <- html_nodes(crushstats18, "table")        # Identify tables 
crush18 <- html_table(tables18[[1]], header = FALSE) # Retrieve the table 

crush18[3, 6] <- "to_date_crush_pc" 

names(crush18) <- crush18[3, ] 
crush18 <- crush18[-c(1:4, 33), ]


# ------------------------------------------------------------------------------
## Clean the datasets ---- 
crush19 %<>% 
  # Rename the variables, so we don't have to deal with spaces and back ticks 
  rename(week_ending = `Week Ending`, 
         orig_forecast = `Original Forecast`, 
         curr_forecast = `Current Forecast`, 
         weekly_crush = `Weekly Crush`, 
         to_date_crush = `To-Date Crush`, 
         weekly_ccs = `Weekly CCS`, 
         to_date_ccs = `To-Date CCS`) %>% 
  # Convert week_ending to a date, and remove the commas and % from other variables 
  mutate(week_ending = as.Date(week_ending, format = "%d/%m/%Y"), 
         orig_forecast = str_replace_all(orig_forecast, ",", "" ), 
         curr_forecast = str_replace_all(curr_forecast, ",", ""), 
         weekly_crush = str_replace_all(weekly_crush, ",", ""), 
         to_date_crush = str_replace_all(to_date_crush, ",", ""), 
         to_date_crush_pc = str_replace_all(to_date_crush_pc, "%", "")) %>% 
  # Convert the numeric variables to numeric, and convert the percentage to a decimal 
  mutate(orig_forecast = as.numeric(orig_forecast), 
         curr_forecast = as.numeric(curr_forecast), 
         weekly_crush = as.numeric(weekly_crush), 
         to_date_crush = as.numeric(to_date_crush), 
         to_date_crush_pc = as.numeric(to_date_crush_pc) / 100) # Because it was a percentage 


crush18 %<>% 
  # Rename the variables, so we don't have to deal with spaces and back ticks 
  rename(week_ending = `Week Ending`, 
         orig_forecast = `Original Forecast`, 
         curr_forecast = `Current Forecast`, 
         weekly_crush = `Weekly Crush`, 
         to_date_crush = `To-Date Crush`, 
         weekly_ccs = `Weekly CCS`, 
         to_date_ccs = `To-Date CCS`) %>% 
  # Convert week_ending to a date, and remove the commas and % from other variables 
  mutate(week_ending = as.Date(week_ending, format = "%d/%m/%Y"), 
         orig_forecast = str_replace_all(orig_forecast, ",", "" ), 
         curr_forecast = str_replace_all(curr_forecast, ",", ""), 
         weekly_crush = str_replace_all(weekly_crush, ",", ""), 
         to_date_crush = str_replace_all(to_date_crush, ",", ""), 
         to_date_crush_pc = str_replace_all(to_date_crush_pc, "%", "")) %>% 
  # Convert the numeric variables to numeric, and convert the percentage to a decimal 
  mutate(orig_forecast = as.numeric(orig_forecast), 
         curr_forecast = as.numeric(curr_forecast), 
         weekly_crush = as.numeric(weekly_crush), 
         to_date_crush = as.numeric(to_date_crush), 
         to_date_crush_pc = as.numeric(to_date_crush_pc) / 100) # Because it was a percentage 


# ------------------------------------------------------------------------------
## Prepare to write to Excel ---- 
crush_wb <- createWorkbook() # create the Excel Workbook 
modifyBaseFont(crush_wb, fontSize = 8, fontName = "Arial") # Set the formatting 

## Create the tabs for each year 
addWorksheet(wb = crush_wb, 
             sheetName = "2018 Crush Statistics", 
             tabColour = "#ADFF2F") 
addWorksheet(wb = crush_wb, 
             sheetName = "2019 Crush Statistics", 
             tabColour = "#9ACD32") 

## Add formatting for the sheets 
setColWidths(wb = crush_wb, 
             sheet = "2018 Crush Statistics", 
             cols = 1:ncol(crush18), 
             widths = "auto") 
setColWidths(wb = crush_wb, 
             sheet = "2019 Crush Statistics", 
             cols = 1:ncol(crush19), 
             widths = "auto") 
addFilter(wb = crush_wb, 
          sheet = "2018 Crush Statistics", 
          rows = 1, 
          cols = 1:length(crush18)) 
addFilter(wb = crush_wb, 
          sheet = "2019 Crush Statistics", 
          rows = 1, 
          cols = 1:length(crush19)) 

## Write the data to the tabs 
writeData(wb = crush_wb, 
          sheet = "2018 Crush Statistics", 
          x = crush18, 
          headerStyle = createStyle(textDecoration = "bold")) 
writeData(wb = crush_wb, 
          sheet = "2019 Crush Statistics", 
          x = crush19, 
          headerStyle = createStyle(textDecoration = "bold")) 


# ------------------------------------------------------------------------------
## Output the Data to Excel ---- 
saveWorkbook(crush_wb, 
             here("supplementary_data", "Industry Crush Statistics.xlsx"), 
             overwrite = TRUE) 


# ------------------------------------------------------------------------------
## Output in CSV and RDS formats ---- 
write_csv(crush18, here("supplementary_data", "Industry Crush Stats (2018).csv")) 
write_csv(crush19, here("supplementary_data", "Industry Crush Stats (2019).csv")) 

saveRDS(crush18, here("supplementary_data", "Industry Crush Stats (2018).rds")) 
saveRDS(crush19, here("supplementary_data", "Industry Crush Stats (2019).rds")) 


# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

