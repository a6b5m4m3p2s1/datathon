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
start_time <- proc.time()

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
# weather_stations <- data.frame(station_id = c("4096", "4078"), 
#                                station_name = c("Proserpine Airport", "Mackay"))
# 
# station <- weather_stations$station_id # We'll just be passing station_id into function

all_stations <- readRDS(here("Supplementary_Data", "Weather Stations - RDS", "Weather Stations.RDS")) 
station <- as.character(all_stations$Site) 


# ------------------------------------------------------------------------------
## Iterate through months and weather stations ---- 
observations <- purrr::map_df(.x = station, function(station, months) {
  
  print(station)
  print(months)
  
  ## Iterate through all months for a particular station 
  tryCatch(purrr::map_df(months, ~fetch_weather(month = .x, station = station), station), 
  error = function(e){data.frame(month = months, station = station, date = NA, day = NA, 
                                 min_temp = NA, max_temp = NA, rainfall_mm = NA, 
                                 evap_mm = NA, sun_hours = NA, max_wind_gust_dir = NA, 
                                 max_wind_gust_km_h = NA, max_wind_gust_time = NA, 
                                 temp_9am = NA, RH_9am = NA, cloud_8th_9am = NA, 
                                 wind_dir_9am = NA, wind_spd_km_h_9am = NA, MSLP_hPa_9am = NA, 
                                 temp_3pm = NA, RH_3pm = NA, cloud_8th_3pm = NA, 
                                 wind_dir_3pm = NA, wind_spd_km_h_3pm = NA, MSLP_hPa_3pm = NA)})
  
}, months)


# ------------------------------------------------------------------------------
## Output in CSV and RDS formats ---- 
write_csv(observations, here("supplementary_data", 
                             "Weather Observations (All).csv")) 

saveRDS(observations, here("supplementary_data", 
                           "Weather Observations (All).rds")) 

check01 <- observations %>% count(month, station) 
check02 <- check01 %>% filter(n > 1) %>% count(station) 

all_stations %<>% mutate_all(as.character) %>% select(Site, Name, Lat, Lon)

valid <- check02 %>% 
  select(station) %>% 
  left_join(all_stations, by = c("station" = "Site")) 

observations_final <- valid %>% inner_join(observations) 

write_csv(observations_final, here("supplementary_data", "Weather Observations (All Valid).CSV"))
saveRDS(observations_final, here("supplementary_data", "Weather Observations (All Valid).RDS"))

# ------------------------------------------------------------------------------
end_time <- proc.time() 

time_taken <- end_time[3] - start_time[3] 
minutes_taken <- time_taken / 60 


# ------------------------------------------------------------------------------

