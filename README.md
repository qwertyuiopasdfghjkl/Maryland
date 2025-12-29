# CourtListener Maryland Private Nuisance Query

This project contains a Python script to query the CourtListener.com database for Maryland court cases containing the phrase "private nuisance."

## Features

- Queries CourtListener API for Maryland court cases
- Filters for the specific phrase "private nuisance"
- Searches across all Maryland courts including:
  - Supreme Court of Maryland
  - Court of Special Appeals of Maryland
  - Circuit Courts of Maryland
  - District Courts of Maryland
  - Maryland Attorney General
  - Maryland Workers' Compensation Commission
- Exports results to JSON format
- Displays formatted results with case details, citations, and snippets

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (No API Key)

```bash
python courtlistener_maryland_query.py
```

### With API Key (Recommended for higher rate limits)

```bash
python courtlistener_maryland_query.py --api-key YOUR_API_KEY
```

### Custom Options

```bash
# Limit results to 50
python courtlistener_maryland_query.py --limit 50

# Custom output file
python courtlistener_maryland_query.py --output my_results.json

# Verbose output
python courtlistener_maryland_query.py --verbose

# Search specific courts only
python courtlistener_maryland_query.py --courts md mdctspec
```

### Getting an API Key

For better performance and higher rate limits, get a free API key from CourtListener:
1. Visit https://www.courtlistener.com/help/api/
2. Create an account
3. Generate an API key from your profile

## Output

The script produces:
1. **Console output**: Formatted results with case details
2. **JSON file**: Complete results saved to `maryland_nuisance_results.json` (or custom filename)

### Result Fields

Each result includes:
- Case name
- Court identifier
- Date filed
- Docket number
- Status
- Citations
- URL to full case on CourtListener
- Text snippet showing context

## Example Output

```
================================================================================
Result #1
================================================================================
Case Name: Smith v. Jones
Court: md
Date Filed: 2020-05-15
Docket Number: 123456
Status: Published
Citation: 450 Md. 123
URL: https://www.courtlistener.com/opinion/...

Snippet:
...the plaintiff alleged a claim for private nuisance based on...
```

## Maryland Courts Searched

- `md` - Supreme Court of Maryland
- `mdctspec` - Court of Special Appeals of Maryland
- `mdsuperct` - Circuit Courts of Maryland
- `mddistct` - District Courts of Maryland
- `mdag` - Maryland Attorney General
- `mdworkcompcom` - Maryland Workers' Compensation Commission

## Notes

- The script respects API rate limits with automatic delays between requests
- Without an API key, you may encounter rate limiting on large queries
- Results are sorted by relevance score

## License

This is a utility script for querying public court records via the CourtListener API.
