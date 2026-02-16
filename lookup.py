#!/usr/bin/env python3
"""
WHOIS Lookup Tool - Tutorial Example

A simple CLI tool that looks up domain registration info using the APIVerve API.
https://apiverve.com/marketplace/whoislookup
"""

import requests
import sys
from datetime import datetime

# ============================================
# CONFIGURATION - Add your API key here
# Get a free key at: https://dashboard.apiverve.com
# ============================================
API_KEY = 'your-api-key-here'
API_URL = 'https://api.apiverve.com/v1/whoislookup'


def lookup_whois(domain: str) -> dict:
    """
    Look up WHOIS information for a domain.

    Args:
        domain: The domain to look up (e.g., google.com)

    Returns:
        Dictionary with registration details or error
    """
    if API_KEY == 'your-api-key-here':
        return {'error': 'API key not configured. Add your key to lookup.py'}

    # Clean domain input
    domain = domain.strip().lower()
    domain = domain.replace('https://', '').replace('http://', '')
    domain = domain.split('/')[0]

    try:
        response = requests.get(
            API_URL,
            params={'domain': domain},
            headers={'x-api-key': API_KEY}
        )

        data = response.json()

        if data.get('status') == 'ok':
            whois = data['data']
            return {
                'success': True,
                'domain': whois.get('domainName', domain),
                'registrar': whois.get('registrar'),
                'createdDate': whois.get('createdDate'),
                'expiryDate': whois.get('expiryDate'),
                'updatedDate': whois.get('updatedDate'),
                'domainStatus': whois.get('domainStatus', []),
                'nameServers': whois.get('nameServers', []),
                'registrarURL': whois.get('registrarURL')
            }
        else:
            return {'error': data.get('error', 'WHOIS lookup failed')}

    except requests.RequestException as e:
        return {'error': f'API request failed: {str(e)}'}
    except (KeyError, ValueError) as e:
        return {'error': f'Invalid response: {str(e)}'}


def format_date(date_str: str) -> str:
    """Format a date string for display."""
    if not date_str:
        return 'N/A'
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str


def print_result(result: dict):
    """Print WHOIS lookup result in a formatted way."""
    if 'error' in result:
        print(f"\n{'='*55}")
        print(f"  Error: {result['error']}")
        print(f"{'='*55}\n")
        return

    print(f"\n{'='*55}")
    print(f"  WHOIS Lookup: {result['domain']}")
    print(f"{'='*55}")

    # Registrar info
    print(f"\n  Registrar Information")
    print(f"  {'-'*51}")
    print(f"  Registrar:      {result.get('registrar') or 'N/A'}")
    print(f"  Created:        {format_date(result.get('createdDate'))}")
    print(f"  Expires:        {format_date(result.get('expiryDate'))}")
    print(f"  Updated:        {format_date(result.get('updatedDate'))}")

    # Status
    domainStatus = result.get('domainStatus', [])
    if domainStatus:
        print(f"\n  Domain Status")
        print(f"  {'-'*51}")
        for s in domainStatus[:5]:  # Show first 5 statuses
            # Truncate long status strings
            if len(s) > 50:
                s = s[:50] + '...'
            print(f"    {s}")

    # Nameservers
    nameServers = result.get('nameServers', [])
    if nameServers:
        print(f"\n  Nameservers")
        print(f"  {'-'*51}")
        for ns in nameServers:
            print(f"    {ns}")

    # Registrar URL
    registrarURL = result.get('registrarURL')
    if registrarURL:
        print(f"\n  Registrar URL: {registrarURL}")

    print(f"\n{'='*55}\n")


def interactive_mode():
    """Run the lookup in interactive mode."""
    print("\n" + "="*55)
    print("  WHOIS Lookup Tool")
    print("  Powered by APIVerve")
    print("="*55)
    print("\nLook up domain registration information")
    print("Type 'quit' to exit\n")

    while True:
        try:
            domain = input("Enter domain (e.g., google.com): ").strip()
            if domain.lower() == 'quit':
                break

            if not domain:
                print("Please enter a domain.\n")
                continue

            result = lookup_whois(domain)
            print_result(result)

        except KeyboardInterrupt:
            print("\n")
            break

    print("Goodbye!\n")


def main():
    """Main entry point."""
    if len(sys.argv) == 2:
        # Command line mode: python lookup.py google.com
        domain = sys.argv[1]
        result = lookup_whois(domain)
        print_result(result)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()
