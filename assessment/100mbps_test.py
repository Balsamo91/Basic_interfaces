import datetime
import requests
import geocoder
import json

class WeatherForecast:
    def __init__(self, file_name):
        self.file_name = file_name
        self.forecast_data = {}  # Dictionary to store forecast data

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
        try:
            with open(self.file_name, "r") as file:
                    try:
                        self.forecast_data.update(json.load(file))
                    except json.decoder.JSONDecodeError:
                        print("File is empty. No existing forecast data.")
        except FileNotFoundError:
            print("File not found. No existing forecast data.")

    def write_to_file(self):
        with open(self.file_name, "w") as file:
            json.dump(self.forecast_data, file)

    def update_forecast(self):
        while True:
            searched_date = input("\nPlease enter the date in the following format yyyy-mm-dd, if empty the current date will be used: ")
        
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

            city = input("\nWhat city do you want to check? ").capitalize()

            found = False
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
                            found = True
                            precip_value = daily.get("precipitation_sum", [])
                            print(precip_value)
                            for v in precip_value:
                                if v > 0.0:
                                    print(f"It will rain as precipitation value is: {v}")
                                    break
                                elif v == 0.0:
                                    print(f"It will not rain as precipitation value is: {v}")
                                    break
                                else:
                                    print("I do not Know!")
                                    break
            except FileNotFoundError:
                print("\nFile 'dates.txt' not found. Creating a new file.\n")
                found = False

            if not found:
                location = geocoder.arcgis(city)

                if location.ok:
                    latitude = location.latlng[0]
                    longitude = location.latlng[1]

                    url = "https://api.open-meteo.com"
                    response = requests.get(url + f"/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}")

                    response_json = response.json()
                    daily_precip_sum = response_json.get("daily", {})
                    precipitation_sum = daily_precip_sum.get("precipitation_sum", [])

                    if precipitation_sum:
                        self[searched_date] = response_json  # Update forecast data
                        print("Forecast updated and saved.")
                    else:
                        print("No forecast data available.")
                else:
                    print("\nCould not find coordinates for the city.")

            if input("\nWould you like to continue? (yes/no): ").lower() != "yes":
                print("Bye, have a good one!")
                break

# Usage
weather_forecast = WeatherForecast("dates.txt")
weather_forecast.read_from_file()  # Load existing forecast data

weather_forecast.update_forecast()  # Update forecast data interactively

