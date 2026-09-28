from pathlib import Path
import requests
import json

URL = "https://api.tvmaze.com/shows?page=0"
OutputFile = Path("summary.json")

def fetch_data(url):
    """Fetches data from the given URL and returns it as a python objects."""
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError: # if exception occurred when requests.get() failed to estabish a connection
        print("Connection error. Unable to reach the server. Please check your internet connection.")

    except requests.exceptions.Timeout: # requests.get() established connection, exception was raised because server did not respond in time
        print("Request timed out. Please try again later.")

    except requests.exceptions.HTTPError as http_err: # response.raise_for_status() rises exception,response was recived but with an unsuccessful status code(>=400)
        print("HTTP error occurred")
        print(f"details: {http_err}")

    except ValueError: # excepiton raised by response.json(),data received from server is not valid JSON
        print("Invalid JSON data received to parse as python objects.")

    
        

def required_records(records):
    """Filters the records by key fields to include only those which is required for aggregation."""




def shows_per_genre(records):
    """Counts the number of shows per genre from the given records."""




def avg_rating_per_language(records):
    """Calculates the average rating per language from the given records."""




def  shows_per_decade(records):
    """Counts the number of shows per decade from the given records."""




''' forth aggerigation (optional)
def avg_rating_per_year(records):
    """Calculates the average rating per year from the given records."""
'''




def build_summary(records):
    """Builds a summary of the given records, including shows per genre, average rating per language, and shows per decade."""
    summary = {
    }
    return summary




def write_summary(summary, output_file):
    """Writes the summary to the specified output file in JSON format."""




def main():
    """Main function to fetch data,run aggerigation and build summary."""
    raw_records = fetch_data(URL)
    cleaned_records = [required_records(r) for r in raw_records] # using list comprehension to make a list of filtered records 
    summary = build_summary(cleaned_records)
    write_summary(summary, OutputFile)






if __name__ == "__main__":
    main()

