# VaniaMetrics

Prometheus metrics for Minecraft servers and proxies — Paper, Purpur, Folia, Spigot, Sponge, Velocity, BungeeCord and Geyser.

VaniaMetrics is a small core plugin that serves `/metrics` over HTTP, plus one optional plugin per integration. Install the core, add only the collectors for the plugins you run, and point Prometheus at the server.

Documentation, compatibility and the reference of every metric: **[vania-metrics.github.io](https://vania-metrics.github.io)**.

- **No runtime dependencies.** The core runs on the JDK alone: nothing shaded, nothing relocated.
- **One jar per integration.** Each collector declares `depend: [VaniaMetrics]`, so a missing target plugin disables that collector cleanly instead of breaking the core.
- **Bounded cardinality.** Per-player series have a hard cap, and rare values are folded away rather than exploding your TSDB.
- **Tested on real servers.** Java 21, Minecraft 1.21.11: every platform a repository claims is started in a container and checked by its CI.

## Repositories

| Repository | What it measures |
|---|---|
| [core](https://github.com/Vania-Metrics/core) | JVM, cgroup, disk, TPS/MSPT, worlds, players, proxy — and the public API |
| [collector-betonquest](https://github.com/Vania-Metrics/collector-betonquest) | BetonQuest conversations, journal entries, points and tags |
| [collector-chunky](https://github.com/Vania-Metrics/collector-chunky) | Chunky pre-generation tasks |
| [collector-essentials](https://github.com/Vania-Metrics/collector-essentials) | Economy balances, accounts and Gini coefficient; AFK players |
| [collector-excellenteconomy](https://github.com/Vania-Metrics/collector-excellenteconomy) | ExcellentEconomy balances, transactions and money flow |
| [collector-grim](https://github.com/Vania-Metrics/collector-grim) | GrimAC flags, setbacks and violation levels |
| [collector-luckperms](https://github.com/Vania-Metrics/collector-luckperms) | LuckPerms groups, tracks, users, and online players by group |
| [collector-multiverse](https://github.com/Vania-Metrics/collector-multiverse) | Multiverse-Core worlds |
| [collector-mvinventories](https://github.com/Vania-Metrics/collector-mvinventories) | Multiverse-Inventories group switches |
| [collector-mvportals](https://github.com/Vania-Metrics/collector-mvportals) | Multiverse-Portals usage |
| [collector-mythicmobs](https://github.com/Vania-Metrics/collector-mythicmobs) | MythicMobs spawns, deaths and despawns |
| [collector-nova](https://github.com/Vania-Metrics/collector-nova) | Nova tile entities |
| [collector-packetevents](https://github.com/Vania-Metrics/collector-packetevents) | Packets, and players by protocol version |
| [collector-phoenixcrates](https://github.com/Vania-Metrics/collector-phoenixcrates) | PhoenixCrates openings, keys, rewards and drop odds |
| [collector-placeholder](https://github.com/Vania-Metrics/collector-placeholder) | Any PlaceholderAPI value, as a gauge |
| [collector-spark](https://github.com/Vania-Metrics/collector-spark) | spark TPS, tick duration, CPU, GC, allocation rate and ping |
| [collector-worldguard](https://github.com/Vania-Metrics/collector-worldguard) | WorldGuard regions and denied PvP |

Which platforms and versions each one supports, and what its latest CI run found: **[compatibility](https://vania-metrics.github.io/compatibility)**.

## Writing a collector

Depend on `fr.samflix:vania-metrics-api`, implement `Collector`, register it on enable. The [core README](https://github.com/Vania-Metrics/core) covers the API, and any `collector-*` repository is a working template.

Metric names follow `mc_<domain>_<subject>`, base units (seconds, bytes), and Prometheus naming conventions.

## Status

Pre-1.0: the API may still change between minor versions. Repositories are being prepared for public release.
