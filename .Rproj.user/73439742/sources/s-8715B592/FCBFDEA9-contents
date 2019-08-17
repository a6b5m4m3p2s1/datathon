# ------------------------------------------------------------------------------
## Preliminaries ---- 
## Load Packages 
library(readr) 
library(glue) 
library(magrittr) 
library(openxlsx) 
library(dplyr) 
library(rvest) 
library(stringr) 


## Set Paths 
STAT19_LINK <- "https://asmc.com.au/industry-overview/statistics/weekly-crush-statistics-2019/" 
STAT18_LINK <- "https://asmc.com.au/industry-overview/2018-weekly-crushing-statistics/" 


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

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
