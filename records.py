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
    return {
        "id": records.get("id"),
        "language": records.get("language"),
        "genres": (records.get("genres") or []),                                        #handels null values, if get() returns none, it will be replaced by an empty list to prevent errors during iteration
        "rating": (records.get("rating") or {}).get("average"),                         # if rating missing/null, it will be replaced by an empty dict to prevent errors when trying to access the "average" key
        "premiered": records.get("premiered")[:4] if records.get("premiered") else None # accesing only the year part,if the value is missing/null, it will be replaced by None to prevent errors when trying to slice a NoneType object
    }




def shows_per_genre(records):
    """Counts the number of shows per genre from the given records."""

    # dictonary is used for grouping as
    # It is easy to read, easy to update, and lets me access each genre’s count directly by key.

    summary = {}
    for record in records:
        for genere in record["genres"]:
            summary[genere] = summary.get(genere, 0) + 1 

    return summary  # function returns {'Drama': 20, 'Comedy': 15, 'Action': 10, ...}





def avg_rating_per_language(records):
    """Calculates the average rating per language from the given records."""

    # used two dictionaries, one to store addition of ratings per language and another to store the count of shows per language. 
    # this allows me to calculate average rating for each language, by doing summation of ratings / no of shows for that language.
    
    total_language_rating = {}
    show_count_per_language = {}

    for record in records:
        lang = record["language"]
        rating = record["rating"]

        if lang and rating is not None:  # only consider shows with a valid rating and language
            total_language_rating[lang] = total_language_rating.get(lang, 0) + rating
            show_count_per_language[lang] = show_count_per_language.get(lang, 0) + 1

    # Calculate the average rating for each language
    averages = {
        lang: round(total_language_rating[lang] / show_count_per_language[lang], 1) # rounding to 1 decimal place to keep the output concise and readable
        for lang in total_language_rating
    }

    return averages # function returns {'English': 7.5, 'Spanish': 6.8, 'French': 7.2, ...}



def  shows_per_decade(records):
    """Counts the number of shows per decade and their IDs."""
    # 
    summary = {}
    for record in records:
        year = record["premiered"]
        if year:
            decade = year[:3] + "0s"

            count,ids = summary.get(decade, (0, []))
            summary[decade] = (count + 1, (ids + [record["id"]])[:5])

    return summary



''' forth aggerigation (optional)
def avg_rating_per_year(records):
    """Calculates the average rating per year from the given records."""
'''




def build_summary(records):
    """Builds a summary of the given records, including shows per genre, average rating per language, and shows per decade."""
    summary = {
        "shows_per_genre": shows_per_genre(records),
        "avg_rating_per_language": avg_rating_per_language(records),
        "shows_per_decade": shows_per_decade(records)   
    }
    return summary




def write_summary(summary, output_file):
    """Writes the summary to the specified output file in JSON format."""




def main():
    """Main function to fetch data,run aggerigation and build summary."""
    raw_records = fetch_data(URL)[:50] # fetch data from the URL and limit to first 50 records
    cleaned_records = [required_records(r) for r in raw_records] # using list comprehension to make a list of filtered records 
    summary = build_summary(cleaned_records)
    write_summary(summary, OutputFile)
    #print(cleaned_records)
    summary =shows_per_decade(cleaned_records)
    print(summary)





if __name__ == "__main__":
    main()

