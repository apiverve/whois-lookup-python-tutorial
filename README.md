# WHOIS Lookup Tool | APIVerve API Tutorial

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.7+-3776ab)](https://python.org)
[![APIVerve | WHOIS Lookup](https://img.shields.io/badge/APIVerve-WHOIS_Lookup-purple)](https://apiverve.com/marketplace/whoislookup?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial)

A Python CLI tool that looks up domain registration information. View registrar, dates, nameservers, and contact details.

![Screenshot](https://raw.githubusercontent.com/apiverve/whois-lookup-python-tutorial/main/screenshot.jpg)

---

### Get Your Free API Key

This tutorial requires an APIVerve API key. **[Sign up free](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial)** - no credit card required.

---

## Features

- Look up WHOIS data for any domain
- View registrar information
- See creation and expiry dates
- View nameservers
- See domain status codes
- Contact information (when available)
- Interactive mode or command-line arguments

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/apiverve/whois-lookup-python-tutorial.git
   cd whois-lookup-python-tutorial
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**

   Open `lookup.py` and replace the API key:
   ```python
   API_KEY = 'your-api-key-here'
   ```

4. **Run the tool**

   Interactive mode:
   ```bash
   python lookup.py
   ```

   Command line mode:
   ```bash
   python lookup.py github.com
   ```

## Usage Examples

### Look up a domain
```bash
$ python lookup.py github.com

=======================================================
  WHOIS Lookup: github.com
=======================================================

  Registrar Information
  ---------------------------------------------------
  Registrar:      MarkMonitor Inc.
  Created:        2007-10-09
  Expires:        2026-10-09
  Updated:        2024-09-08

  Domain Status
  ---------------------------------------------------
    clientDeleteProhibited
    clientTransferProhibited
    clientUpdateProhibited

  Nameservers
  ---------------------------------------------------
    dns1.p08.nsone.net
    dns2.p08.nsone.net
    dns3.p08.nsone.net
    dns4.p08.nsone.net
    ns-1283.awsdns-32.org
    ns-1707.awsdns-21.co.uk
    ns-421.awsdns-52.com
    ns-520.awsdns-01.net

=======================================================
```

## Project Structure

```
whois-lookup-python-tutorial/
├── lookup.py           # Main Python script
├── requirements.txt    # Dependencies (requests)
├── screenshot.jpg      # Preview image
├── LICENSE             # MIT license
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. User provides a domain name
2. Script cleans and validates the input
3. API queries WHOIS database
4. Script formats and displays results

### The API Call

```python
response = requests.get(
    'https://api.apiverve.com/v1/whoislookup',
    params={'domain': domain},
    headers={'x-api-key': API_KEY}
)
```

## API Reference

**Endpoint:** `GET https://api.apiverve.com/v1/whoislookup`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `domain` | string | Yes | Domain to look up (e.g., "google.com") |

**Example Response:**

```json
{
  "status": "ok",
  "error": null,
  "data": {
    "registrar": "MarkMonitor Inc.",
    "createdDate": "2007-10-09T18:20:50Z",
    "expiryDate": "2026-10-09T18:20:50Z",
    "updatedDate": "2024-09-08T09:08:09Z",
    "status": ["clientDeleteProhibited", "clientTransferProhibited"],
    "nameservers": ["dns1.p08.nsone.net", "dns2.p08.nsone.net"]
  }
}
```

## Use Cases

- **Domain research** - Check who owns a domain
- **Due diligence** - Verify domain ownership
- **Expiry tracking** - Monitor domain expiration
- **Brand protection** - Find infringing domains
- **Security investigation** - Research suspicious domains
- **Sales prospecting** - Find domain contact info

## Customization Ideas

- Add domain expiry alerts
- Monitor multiple domains from a list
- Save results to CSV/JSON
- Build a web interface
- Compare WHOIS history over time
- Integrate with CRM systems

## Related APIs

Explore more APIs at [APIVerve](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial):

- [Domain Availability](https://apiverve.com/marketplace/domainavailability?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - Check if a domain is available
- [DNS Lookup](https://apiverve.com/marketplace/dnslookup?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - Check DNS records
- [SSL Checker](https://apiverve.com/marketplace/sslchecker?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - Check SSL certificates

## License

MIT - see [LICENSE](LICENSE)

## Links

- [Get API Key](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - Sign up free
- [APIVerve Marketplace](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - Browse 300+ APIs
- [WHOIS Lookup API](https://apiverve.com/marketplace/whoislookup?utm_source=github&utm_medium=tutorial&utm_campaign=whois-lookup-python-tutorial) - API details
