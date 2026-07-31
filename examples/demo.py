"""Runnable demo. Generates a few PNGs in the current directory.

    python examples/demo.py
"""

import simple_eda_christophersnook as seda
from simple_eda_christophersnook import Chart

# 1. Quick one-liner.
seda.bar(["Mon", "Tue", "Wed", "Thu", "Fri"], [12, 19, 7, 15, 22],
         title="Daily signups", ylabel="count").save("demo_bar.png").close()

# 2. Chainable multi-series line chart (obsidian, the default theme).
steps = list(range(12))
(Chart(theme="obsidian")
    .line(steps, [s * s for s in steps], label="squared", marker="o")
    .line(steps, [s * 4 for s in steps], label="linear", marker="o")
    .labels("Growth over time", "step", "value")
    .save("demo_lines.png")
    .close())

# 3. Ivory (light) theme + escape hatch to raw matplotlib.
c = Chart(theme="ivory").hist([1, 2, 2, 3, 3, 3, 4, 4, 5], bins=5)
c.ax.axvline(3, linestyle="--", color="#ab3939", label="target")
c.labels("Distribution", "bucket", "frequency").legend().save("demo_hist_ivory.png").close()

print("Wrote demo_bar.png, demo_lines.png, demo_hist_ivory.png")
