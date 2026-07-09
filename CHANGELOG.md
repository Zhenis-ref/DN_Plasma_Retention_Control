# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-07-09

### Added

- Initial public research-prototype structure.
- Environment model for HL-2A-inspired plasma-retention control experiments.
- Baseline threshold/hysteresis controller.
- Brute-force control search implementation.
- DN/CCE coordinate-search controller using ΔN–ΔD state representation.
- Trajectory plots and comparative report generation.
- Noise-robustness tests up to 20% measurement noise.
- English `README.md`.
- `LICENSE`, `PATENT_NOTICE.md`, `CITATION.cff`, `requirements.txt`, `.gitignore`.

### Results

- Brute force: 4,880 evaluations, total control effort 10.80, residual resource 0.596.
- DN coordinate approach: 1,097 evaluations, total control effort 10.80, residual resource 0.596.
- Computational evaluation reduction: 4.45×.
- Search-space reduction: 77.5%.
