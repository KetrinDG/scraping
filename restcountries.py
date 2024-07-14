import requests
from prettytable import PrettyTable

class CountryInfo:
    def __init__(self, api_url='https://restcountries.com/v3.1/all'):
        self.api_url = api_url

    def get_country_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def display_countries(self):
        data = self.get_country_data()
        if data:
            table = PrettyTable()
            table.field_names = ["Country Name", "Capital", "Flag URL"]

            for country in data:
                name = country.get('name', {}).get('common', 'N/A')
                capital = country.get('capital', ['N/A'])[0] if country.get('capital') else 'N/A'
                flag = country.get('flags', {}).get('png', 'N/A')
                table.add_row([name, capital, flag])

            print(table)

if __name__ == "__main__":
    ci = CountryInfo()
    ci.display_countries()
