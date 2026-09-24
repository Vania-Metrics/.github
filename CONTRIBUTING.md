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

A platform is marked `yes` in `compatibility.yml` only once its cell passes; `untested` cells run without failing the build. CI runs the same tests on every push to `main` and publishes the results on the [compatibility page](https://vania-metrics.github.io/compatibility).

## Rules that matter

- **Metrics:** `mc_<domain>_<subject>`, base units (`_seconds`, `_bytes`), `_total` for counters. Never put an unbounded value (player name, UUID, free text) in a label unless it goes through the core's bounded player series.
- **No runtime dependencies** in the core. Collectors use `compileOnly` only; nothing is shaded.
- **Main thread:** a collector that touches the Bukkit API must say so (`needsMainThread`); everything else runs off-thread.
- **Compatibility:** compile against the oldest API version you support, and use reflection for anything newer.
- The build runs `javac -Xlint:all -Werror`. Warnings fail the build.

## Pull requests

- One topic per PR, with a short description of what changes for server owners.
- Mention any change to a metric name, label or config key explicitly.
- Keep comments for the *why*; the code shows the *what*.
