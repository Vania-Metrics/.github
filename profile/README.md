# VaniaMetrics

Prometheus metrics for Minecraft servers — Paper and Velocity.

VaniaMetrics is a small core plugin that serves `/metrics` over HTTP, plus one optional plugin per integration. Install the core, add only the collectors for the plugins you run, and point Prometheus at the server.

- **No runtime dependencies.** The core runs on the JDK alone: nothing shaded, nothing relocated.
- **One jar per integration.** Each collector declares `depend: [VaniaMetrics]`, so a missing target plugin disables that collector cleanly instead of breaking the core.
- **Bounded cardinality.** Per-player series have a hard cap, and rare values are folded away rather than exploding your TSDB.
- **Java 21**, Paper 1.21+, Velocity 3.x.

## Repositories

| Repository | What it measures | Platforms |
|---|---|---|
| [core](https://github.com/Vania-Metrics/core) | JVM, cgroup, disk, TPS/MSPT, worlds, players, proxy — and the public API | Paper, Velocity |
| [collector-betonquest](https://github.com/Vania-Metrics/collector-betonquest) | BetonQuest objectives and quest progress | Paper |
| [collector-chunky](https://github.com/Vania-Metrics/collector-chunky) | Chunky pre-generation tasks | Paper |
| [collector-essentials](https://github.com/Vania-Metrics/collector-essentials) | EssentialsX and Vault economy | Paper |
| [collector-excellenteconomy](https://github.com/Vania-Metrics/collector-excellenteconomy) | ExcellentEconomy currencies | Paper |
| [collector-grim](https://github.com/Vania-Metrics/collector-grim) | GrimAC anticheat flags | Paper |
| [collector-luckperms](https://github.com/Vania-Metrics/collector-luckperms) | LuckPerms groups and tracks | Paper, Velocity |
| [collector-multiverse](https://github.com/Vania-Metrics/collector-multiverse) | Multiverse-Core worlds | Paper |
| [collector-mvinventories](https://github.com/Vania-Metrics/collector-mvinventories) | Multiverse-Inventories groups | Paper |
| [collector-mvportals](https://github.com/Vania-Metrics/collector-mvportals) | Multiverse-Portals usage | Paper |
| [collector-mythicmobs](https://github.com/Vania-Metrics/collector-mythicmobs) | MythicMobs spawns and kills | Paper |
| [collector-nova](https://github.com/Vania-Metrics/collector-nova) | Nova blocks and addons | Paper |
| [collector-packetevents](https://github.com/Vania-Metrics/collector-packetevents) | PacketEvents client versions and traffic | Paper, Velocity |
| [collector-phoenixcrates](https://github.com/Vania-Metrics/collector-phoenixcrates) | PhoenixCrates openings and keys | Paper |
| [collector-placeholder](https://github.com/Vania-Metrics/collector-placeholder) | Any PlaceholderAPI value, as a gauge | Paper |
| [collector-spark](https://github.com/Vania-Metrics/collector-spark) | spark TPS, MSPT and CPU | Paper, Velocity |
| [collector-worldguard](https://github.com/Vania-Metrics/collector-worldguard) | WorldGuard regions | Paper |

## Writing a collector

Depend on `fr.samflix:vania-metrics-api`, implement `Collector`, register it on enable. The [core README](https://github.com/Vania-Metrics/core) covers the API, and any `collector-*` repository is a working template.

Metric names follow `mc_<domain>_<subject>`, base units (seconds, bytes), and Prometheus naming conventions.

## Status

Pre-1.0: the API may still change between minor versions. Repositories are being prepared for public release.
