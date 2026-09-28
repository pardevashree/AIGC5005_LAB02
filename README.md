# LAB02: TV shows aggeregation summary
This program downloads real TV show records from the TVMaze API, cleans them, groups them by meaningful fields, and writes a summary JSON file. The summary helps understand patterns in genres, languages, ratings, and decades.

---

## Data source
URL: "https://api.tvmaze.com/shows?page=0"
each records represents one TV show,containing fields such as name, genres, language, rating, and premiere date.When I checked the dataset on the webpage, page 0 contained roughly 249 records.
The program uses the first 100 entries, and then filters these raw records to keep only the fields required for aggregation.

---

## Setup
1. create conda or python virtual environment(here conda is used)
```
conda create -n lab02_env python=3.12
conda activate lab02_env
```

2. install required packages
```
pip install -r requirements.txt
```

---

## Run
```
python records.py
```

---

## Example Output
1. excert of summary.jason
```
{
  "source_url": "https://api.tvmaze.com/shows?page=0",
  "records_processed": 100,
  "shows_per_genre": {
    "Drama": 68,
    "Science-Fiction": 16,
    "Thriller": 24,
    "Action": 25,
    "Crime": 29,
    "Horror": 13,
    "Romance": 14
  },
  "avg_rating_per_language": {
    "English": 7.6,
    "Japanese": 7.9
  },
  "shows_per_decade": {
    "2010s": [
      73,
      [
        1,
        2,
        3,
        4,
        5
      ]
    ],
    "2000s": [
      23,
      [
        8,
        18,
        19,
        22,
        25
      ]
    ]
  }
}
```

2. What this summary tells me
- Drama is the most common genre in the dataset.
- The dataset mainly contains shows in two languages: English and Japanese, both with average  ratings above 7.0
- The 2010s decade has the highest number of shows, suggesting this period had significant increase in TV production and broadcasting activity

---

## Data quirks
- Outdated external IDs:  
Fields such as tvrage and thetvdb often contain old or deprecated identifiers.
Many records have missing or null values,these IDs are no longer reliable for modern use.

- Missing or null ratings:  
The rating.average field is frequently null, meaning many shows have no rating data available.
This requires careful handling when computing averages.

- Inconsistent availability information:  
The network and webChannel fields do not clearly indicate whether a show was broadcast locally or globally.Some streaming platforms list country: null, while others list a country even if the show was globally available.


---

## Design choices
- Filter only the fields needed for aggregation:
The raw API objects contain many unused fields (e.g., tvrage, thetvdb, network, webChannel).
I kept only the fields required for the three aggregations to simplify the dataset and avoid inconsistent metadata.
- Missing fields are normalized, not filtered out
The program does not remove records with missing fields.
Instead, required_records() replaces missing values with None (or empty lists/dicts).
- Use dictionaries for grouping 
Aggregations such as “shows per genre” and “average rating per language” are naturally represented using dictionaries, making the summary easy to read and easy to extend.
- Tuple for decade aggregation
I chose to represent each decade using a tuple in Python: (count,list of ids)
A tuple expresses that these two values — the number of shows in that decade and the list of their IDs — form a fixed pair that belongs together and should not be modified independently.

---

## Known Limitations
- Record count is fixed at 100 and not user‑configurable
the program does not allow the user to specify how many records they want to process.
The value is hard‑coded, which limits flexibility.
- Average ratings may be imprecise
Because the null ratings are skipped, the computed averages may not represent the entire dataset.
- Decade grouping depends on the premiered date format
If a show has an unexpected or missing date format, it cannot be placed into a decade bucket.
- Aggregations may use fewer records because missing fields are normalized  
Missing values are replaced with None instead of being filtered out.
This prevents crashes, but each aggregation only includes records where the required fields are present, so summaries may be based on a smaller subset of the dataset.
- Average rating per year is not implemented yet
The program currently computes average ratings by language and groups shows by decade, but it does not include the optional aggregation that computes average ratings per year.
This feature would provide insight into the quality of shows produced each year, but it remains unimplemented and may be added in a future version.





