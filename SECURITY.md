# Security Policy

## Supported Versions

This project is under active development. Security fixes are applied to the latest release on the `master` branch. Older releases are not maintained.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest | :x:               |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

To report a vulnerability, please use [GitHub's private vulnerability reporting](https://github.com/trademomentum-llc/multimodal-agent-builder/security/advisories/new) or email the maintainer directly. Include:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof-of-concept
- The affected component(s) and version(s)

We will acknowledge receipt within **72 hours** and aim to provide an initial assessment within **7 business days**. Critical vulnerabilities will be prioritized for patching.

## Security Scope

The following areas are in scope for security reports:

### API Key & Credential Management
This project integrates with third-party LLM providers (OpenAI, Google Gemini, Anthropic). All API keys and secrets must be stored in environment variables or `.env` files and are **never** committed to source control. Reports of credential leakage vectors or insecure secret handling are welcome.

### Input Validation & Injection
The FastAPI backend processes user-supplied text, files (images, audio, PDFs), and multipart payloads. Vulnerabilities related to prompt injection, path traversal, file-type bypass, or payload-size abuse are in scope.

### Dependency Supply Chain
We pin dependencies by hash or commit SHA where feasible and run automated scans (njsscan, Dependabot). Reports of vulnerable or compromised transitive dependencies are appreciated.

### Authentication & Authorization
Any bypass of rate limiting, CORS policy, or access controls on API endpoints is in scope.

## Out of Scope

- Vulnerabilities in upstream LLM provider APIs (OpenAI, Google, Anthropic) — report those to the respective providers
- Social engineering or phishing attacks against maintainers
- Denial-of-service attacks that rely on volumetric traffic rather than application logic

## Disclosure Policy

We follow coordinated disclosure. Once a fix is released, we will:

1. Credit the reporter (unless they prefer anonymity)
2. Publish a GitHub Security Advisory describing the issue and remediation
3. Tag a new release with the patch applied
