<img src="icon.png" alt="" width="96" align="right">

# VaniaMetrics

Prometheus metrics for Minecraft servers and proxies — Paper, Purpur, Folia, Spigot, Sponge, Velocity, BungeeCord and Geyser.

VaniaMetrics is a small core plugin that serves `/metrics` over HTTP, plus one optional plugin per integration. Install the core, add only the collectors for the plugins you run, and point Prometheus at the server.

The documentation lives on **[vania-metrics.github.io](https://vania-metrics.github.io)**: how to [get started](https://vania-metrics.github.io/guide/getting-started) and [configure it](https://vania-metrics.github.io/guide/configuration), which platforms [each collector supports](https://vania-metrics.github.io/compatibility), and [every metric](https://vania-metrics.github.io/metrics) with its labels.

- **No runtime dependencies.** The core runs on the JDK alone: nothing shaded, nothing relocated.
- **One jar per integration.** Each collector declares `depend: [VaniaMetrics]`, so a missing target plugin disables that collector cleanly instead of breaking the core.
- **Bounded cardinality.** Per-player series have a hard cap, and rare values are folded away rather than exploding your TSDB.
- **Tested on real servers.** Java 21, Minecraft 1.21.11: every platform a repository claims is started in a container and checked by its CI, and the site shows the latest result.

## Download

Every release is built and published by CI, with its jars and their `SHA512SUMS`.

- **The core:** [latest release](https://github.com/Vania-Metrics/core/releases/latest). One jar per platform: `vania-metrics-bukkit` covers Paper, Purpur, Folia, Spigot and CraftBukkit; the others are for Sponge, Velocity, BungeeCord (and Waterfall) and Geyser.
- **A collector:** its latest release, in the table below. It goes next to the core and to the plugin it measures.

## Collectors

The core measures the JVM, the container (CPU, memory, disk), ticks, worlds, players and proxies. Each collector adds the metrics of one plugin, from its own repository, `collector-<name>`.

| | Plugin | What the collector measures | Download |
|---|---|---|---|
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-betonquest/main/icon.png" alt="" width="32"> | [BetonQuest](https://vania-metrics.github.io/collectors/betonquest) | Conversations, journal entries, points and tags | [Latest release](https://github.com/Vania-Metrics/collector-betonquest/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-chunky/main/icon.png" alt="" width="32"> | [Chunky](https://vania-metrics.github.io/collectors/chunky) | Pre-generation tasks | [Latest release](https://github.com/Vania-Metrics/collector-chunky/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-essentials/main/icon.png" alt="" width="32"> | [EssentialsX](https://vania-metrics.github.io/collectors/essentials) | Economy balances, accounts and Gini coefficient; AFK players | [Latest release](https://github.com/Vania-Metrics/collector-essentials/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-excellenteconomy/main/icon.png" alt="" width="32"> | [ExcellentEconomy](https://vania-metrics.github.io/collectors/excellenteconomy) | Balances, transactions and money flow | [Latest release](https://github.com/Vania-Metrics/collector-excellenteconomy/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-grim/main/icon.png" alt="" width="32"> | [GrimAC](https://vania-metrics.github.io/collectors/grim) | Flags, setbacks and violation levels | [Latest release](https://github.com/Vania-Metrics/collector-grim/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-luckperms/main/icon.png" alt="" width="32"> | [LuckPerms](https://vania-metrics.github.io/collectors/luckperms) | Groups, tracks, users, and online players by group | [Latest release](https://github.com/Vania-Metrics/collector-luckperms/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-multiverse/main/icon.png" alt="" width="32"> | [Multiverse-Core](https://vania-metrics.github.io/collectors/multiverse) | Worlds | [Latest release](https://github.com/Vania-Metrics/collector-multiverse/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-mvinventories/main/icon.png" alt="" width="32"> | [Multiverse-Inventories](https://vania-metrics.github.io/collectors/mvinventories) | Group switches | [Latest release](https://github.com/Vania-Metrics/collector-mvinventories/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-mvportals/main/icon.png" alt="" width="32"> | [Multiverse-Portals](https://vania-metrics.github.io/collectors/mvportals) | Portal use | [Latest release](https://github.com/Vania-Metrics/collector-mvportals/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-mythicmobs/main/icon.png" alt="" width="32"> | [MythicMobs](https://vania-metrics.github.io/collectors/mythicmobs) | Spawns, deaths and despawns | [Latest release](https://github.com/Vania-Metrics/collector-mythicmobs/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-nova/main/icon.png" alt="" width="32"> | [Nova](https://vania-metrics.github.io/collectors/nova) | Tile entities | [Latest release](https://github.com/Vania-Metrics/collector-nova/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-packetevents/main/icon.png" alt="" width="32"> | [PacketEvents](https://vania-metrics.github.io/collectors/packetevents) | Packets, and players by protocol version | [Latest release](https://github.com/Vania-Metrics/collector-packetevents/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-phoenixcrates/main/icon.png" alt="" width="32"> | [PhoenixCrates](https://vania-metrics.github.io/collectors/phoenixcrates) | Openings, keys, rewards and drop odds | [Latest release](https://github.com/Vania-Metrics/collector-phoenixcrates/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-placeholder/main/icon.png" alt="" width="32"> | [PlaceholderAPI](https://vania-metrics.github.io/collectors/placeholder) | Any placeholder value, as a gauge | [Latest release](https://github.com/Vania-Metrics/collector-placeholder/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-spark/main/icon.png" alt="" width="32"> | [spark](https://vania-metrics.github.io/collectors/spark) | TPS, tick duration, CPU, GC, allocation rate and ping | [Latest release](https://github.com/Vania-Metrics/collector-spark/releases/latest) |
| <img src="https://raw.githubusercontent.com/Vania-Metrics/collector-worldguard/main/icon.png" alt="" width="32"> | [WorldGuard](https://vania-metrics.github.io/collectors/worldguard) | Regions and denied PvP | [Latest release](https://github.com/Vania-Metrics/collector-worldguard/releases/latest) |

## Writing a collector

Depend on `fr.samflix:vania-metrics-api`, implement `Collector`, register it on enable. The [core README](https://github.com/Vania-Metrics/core) covers the API, and any `collector-*` repository is a working template.

Metric names follow `mc_<domain>_<subject>`, base units (seconds, bytes), and Prometheus naming conventions.

## Contributing

Issues and pull requests are welcome: see [CONTRIBUTING](https://github.com/Vania-Metrics/.github/blob/main/CONTRIBUTING.md). `main` only takes reviewed pull requests, squash-merged, whose title starts with a type (`feat:`, `fix:`, `docs:`…): releases are computed from it. Report a vulnerability privately, as [SECURITY](https://github.com/Vania-Metrics/.github/blob/main/SECURITY.md) explains.

## Status

Core 0.6.0, for Minecraft 1.21.11; each collector has its own version and releases. Pre-1.0: the API may still change between minor versions. Everything is open source, under the [GPL-3.0](https://github.com/Vania-Metrics/core/blob/main/LICENSE).
