import datetime
import requests
import geocoder
import json

class WeatherForecast:
    def __init__(self, file_name):
        self.file_name = file_name
        self.forecast_data = {}# Dictionary to store forecast data

    # Method to set weather forecast for a particular date
    def __setitem__(self, date, forecast):
        # Add or update forecast for the given date
        self.forecast_data[date] = forecast
        # Write the updated forecast data to the file
        self.write_to_file()

    # Method to get weather forecast for a particular date
    def __getitem__(self, date):
        # Return forecast for the given date
        return self.forecast_data.get(date, None)
    
    # Method to iterate over all dates for which the weather forecast is known
    def __iter__(self):
        # Return an iterator over the keys of the forecast data dictionary
        return iter(self.forecast_data)
    
    # Method to read forecast data from file and populate the forecast dictionary
    def read_from_file(self):
        while True:
            self.searched_date = input("\nPlease enter the date in the following format yyyy-mm-dd, if empty the current date will be used: ")
        
            if searched_date.strip() == "":
                # Get the current date and time
                current_time = datetime.datetime.now()
                # Extract year, month, and day
                year = current_time.year
                month = current_time.month
                day = current_time.day
                # Combine year+month+day to have them shown in the expected format
                searched_date = f"{year}-{month:02d}-{day:02d}"

            else:
                try:
                    datetime.datetime.strptime(searched_date, "%Y-%m-%d")
                except ValueError:
                    print("\nInvalid date format. Make sure to use 'YYYY-MM-DD' format!")
                    continue

            self.city = input("\nWhat city do you want to check? ").capitalize()

            self.found = False
            try:
                with open("dates.txt", "r") as file:
                    for line in file:
                        dictionary = json.loads(line)

                        # Parsing latitude and longitude in dates.txt
                        latitude =dictionary["latitude"]
                        longitude = dictionary["longitude"]

                        # Parsing daily dict in dates.txt
                        daily = dictionary.get("daily", {})
                        time = daily.get("time", [])

                        # Checking if the input date is matching in time variable AND the input city is matching city using the reverse method from the coordinates found in file 
                        if searched_date in time and city in geocoder.arcgis([latitude, longitude], method='reverse').city:
                            self.found = True
                            precip_value = daily.get("precipitation_sum", [])
                            print(precip_value)
                            for v in precip_value:

                                if v > 0.0:
                                    print(f"It will rain as precipitation value is: {v}")
                                    file.close()
                                    break
                                    
                                elif v == 0.0:
                                    print(f"It will not rain as precipitation value is: {v}")
                                    file.close()
                                    break

                                else:
                                    print("I do not Know!")
                                    file.close()
                                    break
            except FileNotFoundError:
                print("\nFile 'dates.txt' not found. Creating a new file.\n")
                
                with open("dates.txt", "w") as file:
                    self.found = False
                    file.close()
                    break
    def write_to_file(self):
        self.url = "https://api.open-meteo.com"
        self.found = False

        if self.found:
            location = geocoder.arcgis(self.city)

            if location.ok:
                latitude = location.latlng[0]
                longitude = location.latlng[1]

                response = requests.get(self.url + f"/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={self.searched_date}&end_date={self.searched_date}")

                response_json = response.json()
                response_write = json.dumps(response_json) + '\n'
                with open("dates.txt", "a") as file:
                    file.write(response_write)

                daily_precip_sum = response_json.get("daily", {})
                precipitation_sum = daily_precip_sum.get("precipitation_sum", [])
                
                for value in precipitation_sum:
                    if value > 0.0:
                        print(f"It will rain as precipitation value is: {value}")
                        break

                    elif value == 0.0:
                        print(f"It will not rain as precipitation value is: {value}")
                        break

                    else:
                        print("I do not Know!")
                        break
            else:
                print("\nCould not find coordinates for the city.")


weather_forecast = WeatherForecast("dates.txt")


print(weather_forecast)