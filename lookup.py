#!/usr/bin/env python3
"""
WHOIS lookups from the command line.

    python lookup.py github.com     # one domain
    python lookup.py                # type domains until you quit

Reads APIVERVE_API_KEY from .env, like the web app.
"""
import re
import sys

from apiverve import ApiError, call_api


def day(value):
    return value[:10] if value else 'n/a'


def show(d):
    if not d.get('createdDate') and not d.get('registrar'):
        print(f"\n  No WHOIS record for {d.get('domain')}. It may not be registered.\n")
        return
    print(f"\n  {d.get('domain') or d.get('domainName')}")
    print(f"  Registrar     {d.get('registrar') or 'n/a'}")
    print(f"  Registered    {day(d.get('createdDate'))}")
    print(f"  Expires       {day(d.get('expiryDate'))}")
    print(f"  Updated       {day(d.get('updatedDate'))}")
    if d.get('domainAgeYears') is not None:
        print(f"  Age           {d['domainAgeYears']} years")
    servers = d.get('nameServers') or []
    if servers:
        print('  Name servers  ' + '\n                '.join(s.lower() for s in servers))
    statuses = [re.sub(r'\s*https?://.*$', '', s) for s in d.get('domainStatus') or []]
    if statuses:
        print('  Status        ' + '\n                '.join(statuses))
    print()


def lookup(domain):
    try:
        show(call_api('whoislookup', {'domain': domain}))
    except ApiError as err:
        print(f'  Error: {err}\n')


def main():
    if len(sys.argv) > 1:
        for domain in sys.argv[1:]:
            lookup(domain)
        return
    print("WHOIS lookup. Type 'quit' to exit.\n")
    while True:
        domain = input('Domain: ').strip()
        if domain.lower() in ('quit', 'exit', 'q'):
            return
        if domain:
            lookup(domain)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
