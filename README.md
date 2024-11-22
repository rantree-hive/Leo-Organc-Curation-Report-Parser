# Leo Organic Curation Report Parser

This script processes curation reports from the Hive blockchain to generate insights on user curations. It uses the Hive API to fetch blog posts tagged with "leo-curation" and extracts detailed statistics on curated users and their curators.

---

## Features

- **Fetch Curation Reports**: Retrieves posts authored by `leo-curation` from the Hive blockchain.
- **Analyze Curation Data**: Extracts information on which users were curated and by whom.
- **Rank Curated Users**: Displays curated users sorted by the total number of curations received, with details on curators.

---

## How to Use

1. Clone this repository:
git clone <repository_url> cd <repository_name>

2. Install dependencies:
- Ensure you have Python 3.x installed.
- Install required packages:
  ```
  pip install requests
  ```

3. Run the script:
  ```
  python leo_organic_curation_report_parser.py
  ```
4. Example of output:

```

gloreal 6 (4 by uyobong, 2 by princessbusayo)
```


## Requirements

- Python 3.x
- `requests` library

---
