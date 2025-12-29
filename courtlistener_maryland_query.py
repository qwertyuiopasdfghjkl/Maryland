#!/usr/bin/env python3
"""
CourtListener Maryland Private Nuisance Query Script

This script queries the CourtListener.com API to search for cases from Maryland courts
that contain the phrase "private nuisance."

Usage:
    python courtlistener_maryland_query.py [--api-key YOUR_API_KEY] [--limit RESULTS]
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Any
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class CourtListenerClient:
    """Client for interacting with the CourtListener API."""

    BASE_URL = "https://www.courtlistener.com/api/rest/v3"

    def __init__(self, api_key: str = None):
        """
        Initialize the CourtListener client.

        Args:
            api_key: Optional API key for authenticated requests (higher rate limits)
        """
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                'Authorization': f'Token {api_key}'
            })

    def search_opinions(
        self,
        query: str,
        court_filter: str = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for opinions in the CourtListener database.

        Args:
            query: Search query string
            court_filter: Court identifier to filter results
            limit: Maximum number of results to return
            offset: Pagination offset

        Returns:
            Dictionary containing search results
        """
        endpoint = f"{self.BASE_URL}/search/"

        params = {
            'q': query,
            'type': 'o',  # 'o' for opinions
            'order_by': 'score desc',
            'format': 'json'
        }

        if court_filter:
            params['court'] = court_filter

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying CourtListener API: {e}")
            return None

    def get_maryland_courts(self) -> List[str]:
        """
        Get list of Maryland court identifiers.

        Returns:
            List of court identifiers for Maryland
        """
        # Maryland court identifiers in CourtListener
        # These are the common Maryland courts in the CourtListener system
        return [
            'md',           # Supreme Court of Maryland (formerly Court of Appeals)
            'mdctspec',     # Court of Special Appeals of Maryland
            'mdsuperct',    # Circuit Courts of Maryland (Superior Court level)
            'mddistct',     # District Courts of Maryland
            'mdag',         # Maryland Attorney General
            'mdworkcompcom' # Maryland Workers' Compensation Commission
        ]


def format_result(result: Dict[str, Any], index: int) -> str:
    """
    Format a single search result for display.

    Args:
        result: Search result dictionary
        index: Result number

    Returns:
        Formatted string representation of the result
    """
    output = [
        f"\n{'='*80}",
        f"Result #{index}",
        f"{'='*80}",
        f"Case Name: {result.get('caseName', 'N/A')}",
        f"Court: {result.get('court', 'N/A')}",
        f"Date Filed: {result.get('dateFiled', 'N/A')}",
        f"Docket Number: {result.get('docketNumber', 'N/A')}",
        f"Status: {result.get('status', 'N/A')}",
    ]

    if result.get('citation'):
        output.append(f"Citation: {', '.join(result['citation'])}")

    if result.get('absolute_url'):
        output.append(f"URL: https://www.courtlistener.com{result['absolute_url']}")

    # Show snippet if available
    if result.get('snippet'):
        output.append(f"\nSnippet:")
        output.append(f"{result['snippet']}")

    return '\n'.join(output)


def save_results_to_file(results: List[Dict[str, Any]], filename: str = "maryland_nuisance_results.json"):
    """
    Save search results to a JSON file.

    Args:
        results: List of search results
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results to file: {e}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Query CourtListener for Maryland private nuisance cases'
    )
    parser.add_argument(
        '--api-key',
        help='CourtListener API key (optional, for higher rate limits)',
        default='a9faf4472816402e1c94d18295ac8e8150343d74'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='Maximum number of results to retrieve (default: 20)'
    )
    parser.add_argument(
        '--output',
        default='maryland_nuisance_results.json',
        help='Output JSON file (default: maryland_nuisance_results.json)'
    )
    parser.add_argument(
        '--courts',
        nargs='+',
        help='Specific Maryland court(s) to query (optional)',
        default=None
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Initialize client
    print("Initializing CourtListener client...")
    client = CourtListenerClient(api_key=args.api_key)

    # Search query for "private nuisance"
    search_query = '"private nuisance"'

    # Get Maryland courts to search
    maryland_courts = args.courts if args.courts else client.get_maryland_courts()

    print(f"\nSearching for: {search_query}")
    print(f"Maryland courts: {', '.join(maryland_courts)}")
    print(f"Result limit: {args.limit}\n")

    all_results = []

    # Query each Maryland court
    for court in maryland_courts:
        if args.verbose:
            print(f"Querying {court}...")

        results = client.search_opinions(
            query=search_query,
            court_filter=court,
            limit=args.limit
        )

        if results and results.get('results'):
            all_results.extend(results['results'])
            if args.verbose:
                print(f"  Found {len(results['results'])} results")

        # Be respectful of API rate limits
        time.sleep(0.5)

    # Display results
    print(f"\n{'='*80}")
    print(f"SEARCH RESULTS: Found {len(all_results)} total results")
    print(f"{'='*80}")

    if all_results:
        for idx, result in enumerate(all_results, 1):
            print(format_result(result, idx))

        # Save to file
        save_results_to_file(all_results, args.output)
    else:
        print("\nNo results found.")

    # Display summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total results: {len(all_results)}")
    print(f"Search query: {search_query}")
    print(f"Courts searched: {', '.join(maryland_courts)}")

    if args.api_key:
        print("\nUsing API key for authenticated access.")


if __name__ == "__main__":
    main()
