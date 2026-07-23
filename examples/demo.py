"""Runnable demo of vizlib. Generates a few PNGs in the current directory.

    python examples/demo.py
"""

import vizlib
from vizlib import Chart

# 1. Quick one-liner.
vizlib.bar(["Mon", "Tue", "Wed", "Thu", "Fri"], [12, 19, 7, 15, 22],
           title="Daily signups", ylabel="count").save("demo_bar.png").close()

# 2. Chainable multi-series line chart.
steps = list(range(12))
(Chart(theme="clean")
    .line(steps, [s * s for s in steps], label="squared")
    .line(steps, [s * 4 for s in steps], label="linear")
    .labels("Growth over time", "step", "value")
    .save("demo_lines.png")
    .close())

# 3. Dark theme + escape hatch to raw matplotlib.
c = Chart(theme="dark").hist([1, 2, 2, 3, 3, 3, 4, 4, 5], bins=5)
c.ax.axvline(3, linestyle="--", color="white", label="target")
c.labels("Distribution", "bucket", "frequency").save("demo_hist_dark.png").close()

print("Wrote demo_bar.png, demo_lines.png, demo_hist_dark.png")
