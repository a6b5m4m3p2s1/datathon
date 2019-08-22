# Grabbing Crush Statistics 
# Inputs: 
#    - None: draws data from the web. 
# 
# Outputs: 
#    -  
# 
# Overview: 
#    - This script takes Bureau of Meteorology Daily Data and outputs in Excel 
#      format. 

# ------------------------------------------------------------------------------
## Preliminaries ---- 
## Load Packages and Source Functions 
library(here) 
source(here("Syntax", "0 Functions.R"))


## Set Paths 
# Model Proserpine: "http://www.bom.gov.au/climate/dwo/201807/html/IDCJDW4096.201807.shtml" 


# ------------------------------------------------------------------------------
## Specify data that is of interest ---- 
## Months
months <- c("201807", "201808", "201809", "201810", "201811", "201812", "201901", "201902", 
            "201903", "201904", "201905", "201906", "201907") 

## Weather Stations of Interest
weather_stations <- data.frame(station_id = c("4096", "4078"), 
                               station_name = c("Proserpine Airport", "Mackay"))

station <- weather_stations$station_id # We'll just be passing station_id into function


# ------------------------------------------------------------------------------
## Iterate through months and weather stations ---- 
observations <- purrr::map_df(.x = station, function(station, months) {
  
  print(station)
  print(months)
  
  ## Iterate through all months for a particular station 
  purrr::map_df(months, ~fetch_weather(month = .x, station = station), station)
  
}, months)


# ------------------------------------------------------------------------------
## Output in CSV and RDS formats ---- 
write_csv(observations, here("supplementary_data", 
                             "Weather Observations (Mackay & Proserpine).csv")) 

saveRDS(observations, here("supplementary_data", 
                           "Weather Observations (Mackay & Proserpine).rds")) 


# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

