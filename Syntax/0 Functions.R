# Functions
# Inputs: 
#    - None 
# 
# Outputs: 
#    - None
# 
# Overview: 
#    - This script creates bespoke functions used in other scripts 

# ------------------------------------------------------------------------------
## Preliminaries ---- 
source(here("Syntax", "0 Settings.R"))

# ------------------------------------------------------------------------------
## fetch_weather() ---- 
fetch_weather <- function(month, station) {
  
  link <- glue("http://www.bom.gov.au/climate/dwo/{month}/html/IDCJDW{station}.{month}.shtml")
  page <- read_html(link)
  tab <- html_nodes(page, "table")
  weather <- html_table(tab[[1]], header = FALSE, fill = TRUE)
  
  #print(station)
  
  names(weather) <- c("date", "day", "min_temp", "max_temp",
                      "rainfall_mm", "evap_mm", "sun_hours", "max_wind_gust_dir",
                      "max_wind_gust_km_h", "max_wind_gust_time", "temp_9am",
                      "RH_9am", "cloud_8th_9am", "wind_dir_9am", "wind_spd_km_h_9am",
                      "MSLP_hPa_9am", "temp_3pm", "RH_3pm", "cloud_8th_3pm",
                      "wind_dir_3pm", "wind_spd_km_h_3pm", "MSLP_hPa_3pm")
  
  weather %<>%
    filter(!date %in% c("Date", "Mean", "Highest", "Lowest", "Total"),
           !str_detect(date, "Statistics")) %>%
    mutate(month = !!month,
           station = !!station)
  
  print(str_glue("{month} {station}"))
  
  #Sys.sleep(5)
  
  return(weather)
  
}

