# Security policy

## Reporting a vulnerability

Please **do not open a public issue**. Use GitHub's private reporting instead: go to the affected repository, open the **Security** tab, then **Report a vulnerability**.

Include the affected repository and version, how to reproduce, and the impact you see. You will get an acknowledgement, and a fix or a decision, as soon as the issue is confirmed.

## Scope

The metrics endpoint is the main attack surface. By default it binds to `0.0.0.0` without authentication, and is meant to sit behind a firewall or a network policy. Setting `http.token` requires a Bearer token. Reports about exposing an unprotected endpoint on purpose are out of scope; anything that bypasses the token, leaks data beyond the documented metrics, or lets a request affect the server is in scope.

## Supported versions

Only the latest release of each repository receives fixes while the project is pre-1.0.
