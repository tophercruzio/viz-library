"""Force a non-interactive backend so tests run headless in CI."""

import matplotlib

matplotlib.use("Agg")
