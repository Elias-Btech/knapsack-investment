"""
Visualization Module – Investment Portfolio Optimizer
Generates 6 polished charts comparing DP vs Greedy results.
White background, consistent color theme, clear annotations.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

from knapsack_dp import (
    load_investments,
    knapsack_dp_2d,
    knapsack_greedy,
    traceback,
)

# ── Global Style ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":     "white",
    "axes.facecolor":       "white",
    "axes.edgecolor":       "#CCCCCC",
    "axes.grid":            True,
    "grid.color":           "#EEEEEE",
    "grid.linestyle":       "--",
    "grid.linewidth":       0.8,
    "font.family":          "DejaVu Sans",
    "font.size":            11,
    "axes.titlesize":       14,
    "axes.titleweight":     "bold",
    "axes.labelsize":       12,
    "axes.labelweight":     "bold",
    "xtick.labelsize":      10,
    "ytick.labelsize":      10,
    "legend.fontsize":      10,
    "legend.framealpha":    0.9,
    "savefig.facecolor":    "white",
    "savefig.dpi":          300,
    "savefig.bbox":         "tight",
})

# ── Color Palette ─────────────────────────────────────────────────────────────
DP_COLOR     = "#2563EB"   # strong blue  → DP
GREEDY_COLOR = "#DC2626"   # strong red   → Greedy
ACCENT       = "#16A34A"   # green        → positive highlights
NEUTRAL      = "#6B7280"   # grey         → secondary info
GOLD         = "#D97706"   # amber        → 1D DP / third series

# ─────────────────────────────────────────────────────────────────────────────
#  CHART 1 – DP vs Greedy: Return & Budget Utilization
# ─────────────────────────────────────────────────────────────────────────────

def plot_dp_vs_greedy_comparison(dp_ret, gr_ret, dp_cost, gr_cost, budget=500):
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("Dynamic Programming vs Greedy — Full Dataset ($500K Budget)",
                 fontsize=15, fontweight="bold", y=1.02)

    # ── Left: Return comparison ──────────────────────────────────────────────
    ax = axes[0]
    labels = ["Dynamic\nProgramming", "Greedy"]
    values = [dp_ret, gr_ret]
    colors = [DP_COLOR, GREEDY_COLOR]
    bars = ax.bar(labels, values, color=colors, width=0.45,
                  edgecolor="white", linewidth=1.5, zorder=3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.015,
                f"${val:,.2f}K",
                ha="center", va="bottom", fontsize=12, fontweight="bold",
                color=bar.get_facecolor())

    gap = dp_ret - gr_ret
    pct = gap / dp_ret * 100 if dp_ret > 0 else 0
    ax.annotate(
        f"DP gains\n+${gap:,.2f}K\n({pct:.1f}% better)",
        xy=(0.5, (dp_ret + gr_ret) / 2),
        xytext=(1.35, (dp_ret + gr_ret) / 2),
        fontsize=9, color=ACCENT, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5),
        va="center",
    )

    ax.set_title("Maximum Return Achieved")
    ax.set_ylabel("Total Return ($K)")
    ax.set_ylim(0, max(values) * 1.25)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
    ax.set_axisbelow(True)

    # ── Right: Budget utilization ────────────────────────────────────────────
    ax2 = axes[1]
    util_dp = dp_cost / budget * 100
    util_gr = gr_cost / budget * 100

    bar_vals = [dp_cost, gr_cost]
    bars2 = ax2.bar(labels, bar_vals, color=colors, width=0.45,
                    edgecolor="white", linewidth=1.5, zorder=3)

    for bar, val, util in zip(bars2, bar_vals, [util_dp, util_gr]):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + budget * 0.015,
                 f"${val:,}K\n({util:.1f}%)",
                 ha="center", va="bottom", fontsize=11, fontweight="bold",
                 color=bar.get_facecolor())

    ax2.axhline(budget, color=NEUTRAL, linestyle="--", linewidth=1.5,
                label=f"Budget limit (${budget:,}K)", zorder=2)
    ax2.set_title("Budget Utilization")
    ax2.set_ylabel("Capital Used ($K)")
    ax2.set_ylim(0, budget * 1.3)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
    ax2.legend(loc="upper right")
    ax2.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("charts/comparison_dp_vs_greedy.png")
    print("[✓] Saved: charts/comparison_dp_vs_greedy.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
#  CHART 2 & 3 – Portfolio Allocation (Horizontal Bar, not Pie)
# ─────────────────────────────────────────────────────────────────────────────

def plot_portfolio_allocation(selected, names, costs, returns,
                               title, filename, bar_color):
    portfolio = sorted(
        [(names[i], costs[i], returns[i]) for i in selected],
        key=lambda x: x[2], reverse=True
    )

    top_n = 12
    top = portfolio[:top_n]
    rest_count = len(portfolio) - top_n
    rest_ret   = sum(r for _, _, r in portfolio[top_n:])
    rest_cost  = sum(c for _, c, _ in portfolio[top_n:])

    if rest_count > 0:
        top.append((f"Others ({rest_count} items)", rest_cost, rest_ret))

    item_names = [t[0] for t in top]
    item_costs = [t[1] for t in top]
    item_rets  = [t[2] for t in top]

    y = np.arange(len(item_names))
    fig, ax = plt.subplots(figsize=(13, max(6, len(y) * 0.55 + 1.5)))

    # Return bars
    bars = ax.barh(y, item_rets, color=bar_color, alpha=0.85,
                   edgecolor="white", linewidth=1.2, label="Return ($K)", zorder=3)

    # Cost markers as thin overlay
    ax.barh(y, item_costs, color="#94A3B8", alpha=0.55,
            edgecolor="none", label="Cost ($K)", zorder=2)

    # Value labels
    for bar, val in zip(bars, item_rets):
        ax.text(bar.get_width() + max(item_rets) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"${val:,.2f}K",
                va="center", ha="left", fontsize=9, fontweight="bold",
                color=bar_color)

    ax.set_yticks(y)
    ax.set_yticklabels(item_names, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Value ($K)")
    ax.set_title(title)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
    ax.set_xlim(0, max(item_rets) * 1.2)
    ax.legend(loc="lower right")
    ax.set_axisbelow(True)

    total_ret  = sum(returns[i] for i in selected)
    total_cost = sum(costs[i]   for i in selected)
    fig.text(0.99, 0.01,
             f"Total Return: ${total_ret:,.2f}K  |  Total Cost: ${total_cost:,}K  |  Items: {len(selected)}",
             ha="right", va="bottom", fontsize=9, color=NEUTRAL,
             style="italic")

    plt.tight_layout()
    plt.savefig(f"charts/{filename}")
    print(f"[✓] Saved: charts/{filename}")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
#  CHART 4 – Test Case Results: DP vs Greedy
# ─────────────────────────────────────────────────────────────────────────────

def plot_test_case_results():
    test_cases = [
        ("Classic\n5-item",    35.00, 28.00),
        ("Greedy\nFailure",    16.00, 15.00),
        ("All Items\nFit",     22.00, 22.00),
        ("Tight\nBudget",      60.00, 60.00),
        ("Single\nItem",       10.00, 10.00),
        ("Choose\nBetter",     10.00, 10.00),
        ("No Items\nFit",       0.00,  0.00),
        ("Large\nGap",         20.00, 12.00),
    ]

    labels   = [tc[0] for tc in test_cases]
    dp_vals  = [tc[1] for tc in test_cases]
    gr_vals  = [tc[2] for tc in test_cases]

    x     = np.arange(len(labels))
    width = 0.32

    fig, ax = plt.subplots(figsize=(14, 6))

    bars_dp = ax.bar(x - width / 2, dp_vals, width, label="DP (Optimal)",
                     color=DP_COLOR, edgecolor="white", linewidth=1.2, zorder=3)
    bars_gr = ax.bar(x + width / 2, gr_vals, width, label="Greedy",
                     color=GREEDY_COLOR, edgecolor="white", linewidth=1.2, zorder=3)

    # Value labels
    for bar in bars_dp:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.4,
                    f"{h:.0f}", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color=DP_COLOR)

    for bar in bars_gr:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.4,
                    f"{h:.0f}", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color=GREEDY_COLOR)

    # Highlight cases where DP beats greedy
    for i, (dp, gr) in enumerate(zip(dp_vals, gr_vals)):
        if dp > gr:
            ax.annotate("DP wins",
                        xy=(x[i] - width / 2, dp),
                        xytext=(x[i] - width / 2, dp + 3.5),
                        ha="center", fontsize=8, color=ACCENT,
                        fontweight="bold",
                        arrowprops=dict(arrowstyle="-", color=ACCENT,
                                        lw=0.8, linestyle="dotted"))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_xlabel("Test Case")
    ax.set_ylabel("Return Value")
    ax.set_title("DP vs Greedy — All 8 Test Cases (Brute-Force Verified)")
    ax.set_ylim(0, max(dp_vals) * 1.35)
    ax.legend(loc="upper right")
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("charts/test_cases_comparison.png")
    print("[✓] Saved: charts/test_cases_comparison.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
#  CHART 5 – Complexity Comparison (Time & Space)
# ─────────────────────────────────────────────────────────────────────────────

def plot_complexity_comparison():
    algorithms  = ["DP (2D)\nO(n·W)", "DP (1D)\nO(n·W)", "Greedy\nO(n log n)"]
    time_ms     = [11.989, 6.771, 0.5]
    space_cells = [60_000, 500, 120]
    colors      = [DP_COLOR, GOLD, GREEDY_COLOR]

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("Algorithm Complexity — Runtime & Memory (n=120, W=500)",
                 fontsize=14, fontweight="bold", y=1.02)

    # ── Left: Runtime ────────────────────────────────────────────────────────
    ax = axes[0]
    bars = ax.bar(algorithms, time_ms, color=colors, width=0.45,
                  edgecolor="white", linewidth=1.5, zorder=3)

    for bar, val in zip(bars, time_ms):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(time_ms) * 0.02,
                f"{val:.3f} ms",
                ha="center", va="bottom", fontsize=11, fontweight="bold",
                color=bar.get_facecolor())

    ax.set_title("Actual Runtime")
    ax.set_ylabel("Time (milliseconds)")
    ax.set_ylim(0, max(time_ms) * 1.3)
    ax.set_axisbelow(True)

    # ── Right: Memory (log scale with clear labels) ──────────────────────────
    ax2 = axes[1]
    bars2 = ax2.bar(algorithms, space_cells, color=colors, width=0.45,
                    edgecolor="white", linewidth=1.5, zorder=3)

    for bar, val in zip(bars2, space_cells):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 val * 2.2,
                 f"{val:,} cells",
                 ha="center", va="bottom", fontsize=11, fontweight="bold",
                 color=bar.get_facecolor())

    ax2.set_yscale("log")
    ax2.set_title("Memory Usage (log scale)")
    ax2.set_ylabel("Memory Cells (log scale)")
    ax2.set_ylim(10, max(space_cells) * 15)
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
    )
    ax2.set_axisbelow(True)

    # Annotation: 1D DP is 120× more memory-efficient than 2D
    ratio = space_cells[0] // space_cells[1]
    ax2.annotate(
        f"1D uses {ratio}× less\nmemory than 2D",
        xy=(1, space_cells[1]),
        xytext=(1.6, space_cells[1] * 8),
        fontsize=9, color=ACCENT, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5),
    )

    plt.tight_layout()
    plt.savefig("charts/complexity_comparison.png")
    print("[✓] Saved: charts/complexity_comparison.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
#  CHART 6 – Investment Landscape Scatter Plot
# ─────────────────────────────────────────────────────────────────────────────

def plot_investment_distribution(ids, names, costs, returns,
                                  dp_sel, gr_sel):
    dp_set = set(dp_sel)
    gr_set = set(gr_sel)

    # Classify each point
    both    = [i for i in range(len(costs)) if i in dp_set and i in gr_set]
    dp_only = [i for i in range(len(costs)) if i in dp_set and i not in gr_set]
    gr_only = [i for i in range(len(costs)) if i not in dp_set and i in gr_set]
    neither = [i for i in range(len(costs)) if i not in dp_set and i not in gr_set]

    fig, ax = plt.subplots(figsize=(12, 8))

    def scatter_group(indices, color, label, marker, size, zorder, alpha=0.75):
        if not indices:
            return
        ax.scatter(
            [costs[i]   for i in indices],
            [returns[i] for i in indices],
            c=color, label=label, marker=marker,
            s=size, alpha=alpha, edgecolors="white",
            linewidths=0.6, zorder=zorder
        )

    scatter_group(neither, "#CBD5E1", "Not selected",          "o", 60,  2, alpha=0.5)
    scatter_group(both,    ACCENT,    "Selected by both",      "D", 110, 5)
    scatter_group(dp_only, DP_COLOR,  "DP only (unique pick)", "^", 110, 4)
    scatter_group(gr_only, GREEDY_COLOR, "Greedy only",        "s", 110, 4)

    # Annotate a few interesting DP-only picks
    annotated = 0
    for i in sorted(dp_only, key=lambda x: returns[x], reverse=True):
        if annotated >= 4:
            break
        ax.annotate(
            names[i],
            xy=(costs[i], returns[i]),
            xytext=(costs[i] + 3, returns[i] + 2),
            fontsize=7.5, color=DP_COLOR,
            arrowprops=dict(arrowstyle="-", color=DP_COLOR, lw=0.8),
        )
        annotated += 1

    ax.set_xlabel("Cost ($K)")
    ax.set_ylabel("Expected Return ($K)")
    ax.set_title("Investment Landscape — Cost vs Return (120 Items)\n"
                 "Showing which items each algorithm selected",
                 fontsize=13)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=10)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("charts/investment_distribution.png")
    print("[✓] Saved: charts/investment_distribution.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs("charts", exist_ok=True)

    print("=" * 60)
    print("  GENERATING VISUALIZATION CHARTS")
    print("=" * 60)

    CSV_FILE = "investments.csv"
    BUDGET   = 500

    ids, names, costs, returns = load_investments(CSV_FILE)

    dp_ret, dp_table = knapsack_dp_2d(costs, returns, BUDGET)
    dp_sel           = traceback(dp_table, costs, BUDGET)
    gr_ret, gr_sel   = knapsack_greedy(costs, returns, BUDGET)

    dp_cost = sum(costs[i] for i in dp_sel)
    gr_cost = sum(costs[i] for i in gr_sel)

    print("\n[1/6] DP vs Greedy comparison bar chart...")
    plot_dp_vs_greedy_comparison(dp_ret, gr_ret, dp_cost, gr_cost, BUDGET)

    print("[2/6] DP portfolio allocation (horizontal bar)...")
    plot_portfolio_allocation(dp_sel, names, costs, returns,
                              "DP Optimal Portfolio — Top Investments by Return",
                              "portfolio_dp.png", DP_COLOR)

    print("[3/6] Greedy portfolio allocation (horizontal bar)...")
    plot_portfolio_allocation(gr_sel, names, costs, returns,
                              "Greedy Portfolio — Top Investments by Return",
                              "portfolio_greedy.png", GREEDY_COLOR)

    print("[4/6] Test case comparison...")
    plot_test_case_results()

    print("[5/6] Complexity comparison...")
    plot_complexity_comparison()

    print("[6/6] Investment landscape scatter plot...")
    plot_investment_distribution(ids, names, costs, returns, dp_sel, gr_sel)

    print("\n" + "=" * 60)
    print("  ✓ ALL 6 CHARTS GENERATED SUCCESSFULLY")
    print("  Location: charts/ folder")
    print("=" * 60)


if __name__ == "__main__":
    main()
