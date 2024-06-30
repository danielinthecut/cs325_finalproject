import requests

def gatherForecast(latitude, longitude):
    baseURL = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(baseURL)

    if response.status_code == 200:
        data = response.json()
        forecastURL = data['properties']['forecast']
        return gatherDetails(forecastURL)
    else:
        return None

def gatherDetails(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['properties']['periods']
    else:
        return None

def extractData(periods):
    forecastList = []
    for listings in periods:
        forecastInfo = {
            'name': listings.get('name'),
            'startTime': listings.get('startTime'),
            'temperature': listings.get('temperature'),
            'shortForecast': listings.get('shortForecast')
        }
        forecastList.append(forecastInfo)
    return forecastList

def saveForecastInFile(forecastData, filename='forecast.txt'):
    with open(filename, 'w') as file:
        for forecast in forecastData:
            line = f"{forecast['name']}|{forecast['startTime']}|{forecast['temperature']}|{forecast['shortForecast']}\n"
            file.write(line)

def readForecastFromFile(filename='forecast.txt'):
    forecastData = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                name, startTime, temperature, shortForecast = line.strip().split('|')
                forecastData.append({
                    'name': name,
                    'startTime': startTime,
                    'temperature': temperature,
                    'shortForecast': shortForecast
                })
        print(f"Forecast data read from {filename}")
    except IOError as e:
        print(f"Error reading forecast data from file: {e}")

    return forecastData

def createHTMLForecast(forecastData, filename='weatherForecast.html'):
    html_content = """
    <html>
    <head>
        <title>Weather Forecast</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Weather Forecast</h2>
        <table>
            <tr>
                <th>Date</th>
                <th>Start Time</th>
                <th>Temperature</th>
                <th>Forecast</th>
            </tr>
    """

    for forecast in forecastData:
        html_content += "<tr>"
        html_content += f"<td>{forecast['name']}</td>"
        html_content += f"<td>{forecast['startTime']}</td>"
        html_content += f"<td>{forecast['temperature']}</td>"
        html_content += f"<td>{forecast['shortForecast']}</td>"
        html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """

    try:
        with open(filename, 'w') as file:
            file.write(html_content)
        print(f"HTML file '{filename}' generated successfully.")
    except IOError as e:
        print(f"Error generating HTML file: {e}")

# Main
if __name__ == "__main__":
    
    latitude = 38.6246
    longitude = -90.1847

    periods = gatherForecast(latitude, longitude)

    if periods:
        
        forecastData = extractData(periods)

        # Save to file
        saveForecastInFile(forecastData)

        # Read from file
        forecastDataFromFile = readForecastFromFile()

        # Create HTML file 
        createHTMLForecast(forecastData)
    else:
        print("Error to retrieve data.")