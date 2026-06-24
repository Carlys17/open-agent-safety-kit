# Security Policy

This project is a safety tool, but it may process traces that include sensitive data.

## Do not submit secrets

Do not open issues or pull requests containing:

- private keys
- seed phrases
- API keys
- `.env` contents
- wallet files
- personal access tokens
- production credentials

## Reporting security issues

If you find a security issue in the toolkit itself, open a private report through GitHub Security Advisories if available, or contact the maintainer directly.

## Design principle

The toolkit should be safe by default. Rules should help users detect exposed secrets and unsafe automation without encouraging publication of sensitive traces.
