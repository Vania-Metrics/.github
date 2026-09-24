# VaniaMetrics

Prometheus metrics for Minecraft servers and proxies — Paper, Purpur, Folia, Spigot, Sponge, Velocity, BungeeCord and Geyser.

VaniaMetrics is a small core plugin that serves `/metrics` over HTTP, plus one optional plugin per integration. Install the core, add only the collectors for the plugins you run, and point Prometheus at the server.

The documentation lives on **[vania-metrics.github.io](https://vania-metrics.github.io)**: how to [get started](https://vania-metrics.github.io/guide/getting-started) and [configure it](https://vania-metrics.github.io/guide/configuration), which platforms [each collector supports](https://vania-metrics.github.io/compatibility), and [every metric](https://vania-metrics.github.io/metrics) with its labels.

- **No runtime dependencies.** The core runs on the JDK alone: nothing shaded, nothing relocated.
- **One jar per integration.** Each collector declares `depend: [VaniaMetrics]`, so a missing target plugin disables that collector cleanly instead of breaking the core.
- **Bounded cardinality.** Per-player series have a hard cap, and rare values are folded away rather than exploding your TSDB.
- **Tested on real servers.** Java 21, Minecraft 1.21.11: every platform a repository claims is started in a container and checked by its CI, and the site shows the latest result.

## Collectors

The core measures the JVM, the container (CPU, memory, disk), ticks, worlds, players and proxies. Each collector adds the metrics of one plugin, from its own repository, `collector-<name>`.

| Plugin | What the collector measures |
|---|---|
| [BetonQuest](https://vania-metrics.github.io/collectors/betonquest) | Conversations, journal entries, points and tags |
| [Chunky](https://vania-metrics.github.io/collectors/chunky) | Pre-generation tasks |
| [EssentialsX](https://vania-metrics.github.io/collectors/essentials) | Economy balances, accounts and Gini coefficient; AFK players |
| [ExcellentEconomy](https://vania-metrics.github.io/collectors/excellenteconomy) | Balances, transactions and money flow |
| [GrimAC](https://vania-metrics.github.io/collectors/grim) | Flags, setbacks and violation levels |
| [LuckPerms](https://vania-metrics.github.io/collectors/luckperms) | Groups, tracks, users, and online players by group |
| [Multiverse-Core](https://vania-metrics.github.io/collectors/multiverse) | Worlds |
| [Multiverse-Inventories](https://vania-metrics.github.io/collectors/mvinventories) | Group switches |
| [Multiverse-Portals](https://vania-metrics.github.io/collectors/mvportals) | Portal use |
| [MythicMobs](https://vania-metrics.github.io/collectors/mythicmobs) | Spawns, deaths and despawns |
| [Nova](https://vania-metrics.github.io/collectors/nova) | Tile entities |
| [PacketEvents](https://vania-metrics.github.io/collectors/packetevents) | Packets, and players by protocol version |
| [PhoenixCrates](https://vania-metrics.github.io/collectors/phoenixcrates) | Openings, keys, rewards and drop odds |
| [PlaceholderAPI](https://vania-metrics.github.io/collectors/placeholder) | Any placeholder value, as a gauge |
| [spark](https://vania-metrics.github.io/collectors/spark) | TPS, tick duration, CPU, GC, allocation rate and ping |
| [WorldGuard](https://vania-metrics.github.io/collectors/worldguard) | Regions and denied PvP |

## Writing a collector

Depend on `fr.samflix:vania-metrics-api`, implement `Collector`, register it on enable. The [core README](https://github.com/Vania-Metrics/core) covers the API, and any `collector-*` repository is a working template.

Metric names follow `mc_<domain>_<subject>`, base units (seconds, bytes), and Prometheus naming conventions.

## Status

Version 0.6.0, for Minecraft 1.21.11. Pre-1.0: the API may still change between minor versions. The repositories stay private while they are prepared for public release; the documentation and the test results are public.
