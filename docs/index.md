# SimUCI Documentation

Welcome to the SimUCI documentation. This directory contains detailed guides and references for the SimUCI project.

## 📚 Quick Links

- **[Project README (English)](../README.md)**: Main entry point, installation, and quick start.
- **[Architecture Guide](architecture.md)**: High-level system design and component interaction.
- **[Function Profile](function-profile.md)**: Function-by-function behavior map for all source modules.
- **[Changelog](../CHANGELOG.md)**: Version history and release notes.

## 🛠️ User Guides

*(Coming soon: Detailed tutorials on creating custom experiments and improved simulation configurations)*

## 🔑 Functional Overview

- `simuci.core.experiment`: Input model and replication orchestration.
- `simuci.core.simulation`: SimPy patient journey execution.
- `simuci.core.distributions`: Cluster samplers and centroid-based assignment.
- `simuci.io.loaders`: Centroid CSV loading and schema checks.
- `simuci.io.process_data`: Patient CSV extraction helpers and time-horizon utilities.
- `simuci.analysis.stats`: Statistical validation wrappers and simulation quality metrics.
- `simuci.validation`: Input contracts and validators.
- `simuci.tooling.envcheck`: Optional environment and dependency diagnostics.

## 📦 API Reference

The public API is exposed through `simuci`. Key modules include:

- `simuci.core.experiment`: Managing simulation runs.
- `simuci.core.simulation`: The discrete-event engine.
- `simuci.core.distributions`: Statistical distributions for patient arrival/service times.
- `simuci.io.loaders`: Data loading utilities.
- `simuci.analysis.stats`: Statistical validation tools.

## 🤝 Contributing

See the [Contributing Section](../README.md#contributing) in the main README for development setup instructions.
