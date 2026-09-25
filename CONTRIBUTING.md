# Contributing to VaniaMetrics

Thanks for helping. This applies to every repository in the organization unless it has its own `CONTRIBUTING.md`.

## Before you start

- **Bugs:** open an issue with your server software and version, the VaniaMetrics version, and the relevant `/metrics` output or log lines.
- **New collector or new metric:** open an issue first. Metric names are a public contract — once dashboards depend on them, renaming is expensive — so they are agreed on before code is written.

## Building

Every repository builds with the Gradle wrapper and Java 21:

```sh
./gradlew build
```

Collectors compile against the `core` API at the tag pinned in `gradle.properties`. To work against a local checkout of `core`:

```sh
./gradlew build -PvaniaCore.dir=../core
```

Dependency checksums are verified. If you change a dependency, regenerate them:

```sh
./gradlew --write-verification-metadata sha256 build
```

## Testing on real servers

The core's testkit starts every platform a repository's `compatibility.yml` claims in a container, installs the jars, reads `/metrics`, and checks that the server stops cleanly with a clean log. It needs Docker, or Podman with its user socket.

```sh
./gradlew integrationTest integrationTestUntested --continue -PvaniaCore.dir=../core   # a collector
./gradlew :vania-metrics-testkit:integrationTest                                       # the core
```

A platform is marked `yes` in `compatibility.yml` only once its cell passes; `untested` cells run without failing the build. CI runs the same tests on every pull request and every push to `main`; the results of `main` are published on the [compatibility page](https://vania-metrics.github.io/compatibility).

## Rules that matter

- **Metrics:** `mc_<domain>_<subject>`, base units (`_seconds`, `_bytes`), `_total` for counters. Never put an unbounded value (player name, UUID, free text) in a label unless it goes through the core's bounded player series.
- **No runtime dependencies** in the core. Collectors use `compileOnly` only; nothing is shaded.
- **Main thread:** a collector that touches the Bukkit API must say so (`needsMainThread`); everything else runs off-thread.
- **Compatibility:** compile against the oldest API version you support, and use reflection for anything newer.
- The build runs `javac -Xlint:all -Werror`. Warnings fail the build.

## Pull requests

`main` only takes pull requests, in every repository. Members push branches to the organization's repositories; everyone else works from a fork.

- One topic per PR, with a short description of what changes for server owners.
- Mention any change to a metric name, label or config key explicitly.
- Keep comments for the *why*; the code shows the *what*.
- The PR is squash-merged: its **title becomes the commit message** on `main`, so it starts with a type (below), and its description becomes the commit body.
- Merging needs one approving review from a member, every conversation resolved, and a green CI: `build` in the core, `ci / collector` in a collector, the real-server tests. A push after the approval needs a new one. A fork's workflow runs wait for a maintainer to approve them.
- Every commit on `main` has a verified signature: the squash commit is signed by GitHub. Signing your own commits is welcome, not required.

## Commits and releases

The PR title, which becomes the commit message on `main`, starts with a type, because releases are computed from it:

| Type | Release |
|---|---|
| `feat:` | a minor version, listed under Features |
| `fix:` | a patch version, listed under Bug Fixes |
| `feat!:`, `fix!:` | a breaking change: still a minor version while we are before 1.0 |
| `chore:`, `docs:`, `ci:`, `build:`, `test:`, `refactor:` | no release |

Every repository versions itself: a collector's version is in `version.txt`, the core's in `Version.java`. On every merge into `main`, release-please keeps a release pull request up to date with the next version and its changelog. GitHub Actions opens it, so no CI runs on it: a maintainer merges it past the required check. Merging it tags `vX.Y.Z`, creates the GitHub release, and attaches the jars with their `SHA512SUMS`. The core version a collector is built against stays in its `gradle.properties` and `compatibility.yml`; moving to a new core is a `feat: core API x.y.z` commit.

## License

Every repository is under the GNU General Public License v3.0, in its `LICENSE` file. By contributing, you agree that your contribution is released under it.
