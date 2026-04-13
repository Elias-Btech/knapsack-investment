"""
============================================================
  Q3 – 0/1 Knapsack: Investment Portfolio Optimization
  Full Implementation  |  Algorithm Design & Analysis
============================================================
  Sections
  --------
  1. load_investments()   – read CSV into parallel arrays
  2. knapsack_dp_2d()     – 2D DP table (with traceback)
  3. traceback()          – reconstruct selected items
  4. knapsack_dp_1d()     – space-optimised 1D DP
  5. knapsack_greedy()    – greedy by return/cost ratio
  6. knapsack_brute()     – brute-force (small inputs only)
  7. run_test_case()      – named test-case runner
  8. main()               – full pipeline on investments.csv
=============================================================
"""

import csv
import io
import sys
import time
import itertools
from contextlib import redirect_stdout


# ═══════════════════════════════════════════════════════════
#  1 – LOAD DATA FROM CSV
# ═══════════════════════════════════════════════════════════

def load_investments(filename: str):
    """
    Parse investments.csv into four parallel arrays.

    Returns
    -------
    ids     : list[str]   – Investment_ID  (e.g. 'INV_001')
    names   : list[str]   – human-readable name
    costs   : list[int]   – capital required  (knapsack weight)
    returns : list[float] – expected profit   (knapsack value)
    """
    ids, names, costs, returns = [], [], [], []

    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row:
                    continue
                ids.append(row["Investment_ID"].strip())
                names.append(row["Name"].strip())
                try:
                    costs.append(int(row["Cost"].strip()))
                    returns.append(float(row["Return"].strip()))
                except (ValueError, TypeError) as exc:
                    raise ValueError(
                        f"Invalid numeric value in '{filename}' on row {reader.line_num}: {exc}"
                    ) from exc
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Could not open investment file: '{filename}'. "
            "Please generate or provide the CSV first."
        ) from exc

    print(f"[✓] Loaded {len(ids)} investments from '{filename}'")
    return ids, names, costs, returns


# ═══════════════════════════════════════════════════════════
#  2 – 2D DYNAMIC PROGRAMMING TABLE
# ═══════════════════════════════════════════════════════════

def knapsack_dp_2d(costs: list, returns: list, budget: int):
    """
    Build the full (n+1) × (W+1) DP table.

    Recurrence
    ----------
    dp[i][w] = 0                                        if i=0 or w=0
    dp[i][w] = dp[i-1][w]                               if cost[i] > w
    dp[i][w] = max(dp[i-1][w],
                   dp[i-1][w - cost[i]] + return[i])    otherwise

    Returns
    -------
    max_return : float   – optimal total return
    dp         : 2D list – full table needed for traceback
    """
    n = len(costs)
    W = budget

    # Allocate (n+1) rows × (W+1) columns, all zeros
    dp = [[0.0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        c = costs[i - 1]      # weight of item i
        r = returns[i - 1]    # value  of item i

        for w in range(W + 1):
            # Choice A: leave item i out
            skip = dp[i - 1][w]

            # Choice B: include item i (only if it fits)
            take = (dp[i - 1][w - c] + r) if c <= w else 0.0

            dp[i][w] = max(skip, take)

    return dp[n][W], dp


# ═══════════════════════════════════════════════════════════
#  3 – TRACEBACK  (reconstruct selected items)
# ═══════════════════════════════════════════════════════════

def traceback(dp: list, costs: list, budget: int) -> list:
    """
    Walk backwards through the DP table to find which items
    were included in the optimal solution.

    Returns list of 0-based indices (original array order).
    """
    n = len(costs)
    w = budget
    selected = []

    for i in range(n, 0, -1):
        # If the value differs from the row above, item i was taken
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)   # 0-based index
            w -= costs[i - 1]        # reduce remaining capacity

    selected.reverse()
    return selected


# ═══════════════════════════════════════════════════════════
#  4 – SPACE-OPTIMISED 1D DP
# ═══════════════════════════════════════════════════════════

def knapsack_dp_1d(costs: list, returns: list, budget: int) -> float:
    """
    Same result as 2D DP but uses only O(W) space.

    Key insight: traverse w from W DOWN to cost[i] so that
    each item is counted at most once (0/1 constraint).
    Left-to-right traversal would allow reuse → unbounded knapsack.

    Returns only the maximum return (no traceback possible).
    """
    W = budget
    dp = [0.0] * (W + 1)   # single rolling row

    for i in range(len(costs)):
        c = costs[i]
        r = returns[i]
        if c == 0:
            # Zero-cost item: take it only if it increases return.
            if r > 0:
                dp = [v + r for v in dp]
            continue
        # RIGHT-TO-LEFT is mandatory for 0/1 correctness
        for w in range(W, c - 1, -1):
            dp[w] = max(dp[w], dp[w - c] + r)

    return dp[W]


# ═══════════════════════════════════════════════════════════
#  5 – GREEDY ALGORITHM  (for comparison)
# ═══════════════════════════════════════════════════════════

def knapsack_greedy(costs: list, returns: list, budget: int):
    """
    Greedy strategy: sort by return/cost ratio (highest first),
    then pick each investment if it still fits in the budget.

    Time: O(n log n)  |  NOT guaranteed optimal for 0/1 knapsack.

    Returns
    -------
    total_return : float
    selected     : list of 0-based indices
    """
    n = len(costs)

    # Guard: if cost is 0, treat positive-return items first;
    # negative or zero return zero-cost items should not be selected.
    ratios = []
    for i in range(n):
        c, r = costs[i], returns[i]
        if c == 0:
            ratios.append(float('inf') if r > 0 else float('-inf'))
        else:
            ratios.append(r / c)

    # Sort indices by ratio, descending
    order = sorted(range(n), key=lambda i: ratios[i], reverse=True)

    total_return = 0.0
    total_cost = 0
    selected = []

    for i in order:
        if total_cost + costs[i] <= budget:
            selected.append(i)
            total_cost += costs[i]
            total_return += returns[i]

    return total_return, selected


# ═══════════════════════════════════════════════════════════
#  6 – BRUTE-FORCE  (correctness verifier, small n only)
# ═══════════════════════════════════════════════════════════

def knapsack_brute(costs: list, returns: list, budget: int):
    """
    Enumerate all 2^n subsets and return the best feasible one.
    Only practical for n ≤ 20.  Used to verify DP correctness.

    Returns
    -------
    best_return  : float
    best_subset  : list of 0-based indices
    """
    n = len(costs)
    best_return = 0.0
    best_subset = []

    for r in range(n + 1):
        for subset in itertools.combinations(range(n), r):
            total_cost = sum(costs[i] for i in subset)
            total_return = sum(returns[i] for i in subset)
            if total_cost <= budget and total_return > best_return:
                best_return = total_return
                best_subset = list(subset)

    return best_return, best_subset


# ═══════════════════════════════════════════════════════════
#  7 – NAMED TEST-CASE RUNNER
# ═══════════════════════════════════════════════════════════

def run_test_case(name: str, costs: list, returns: list, budget: int,
                  verify_brute: bool = True) -> None:
    """
    Run DP, 1D DP, Greedy (and optionally Brute-Force) on a
    small named test case and print a comparison table.
    """
    n = len(costs)
    print(f"\n{'─'*60}")
    print(f"  TEST CASE: {name}")
    print(f"  n={n} items  |  Budget={budget}")
    print(f"  Costs  : {costs}")
    print(f"  Returns: {returns}")
    print(f"{'─'*60}")

    # DP
    dp_ret, dp_table = knapsack_dp_2d(costs, returns, budget)
    dp_sel = traceback(dp_table, costs, budget)
    dp1d_ret = knapsack_dp_1d(costs, returns, budget)

    # Greedy
    gr_ret, gr_sel = knapsack_greedy(costs, returns, budget)

    # Brute-force (verification)
    bf_ret = None
    if verify_brute and n <= 20:
        bf_ret, _ = knapsack_brute(costs, returns, budget)

    # Print results
    print(f"  {'Algorithm':<20} {'Return':>10}  {'Items chosen'}")
    print(f"  {'-'*55}")
    print(f"  {'DP (2D)':<20} {dp_ret:>10.2f}  {dp_sel}")
    print(f"  {'DP (1D space-opt)':<20} {dp1d_ret:>10.2f}  (no traceback)")
    print(f"  {'Greedy':<20} {gr_ret:>10.2f}  {gr_sel}")
    if bf_ret is not None:
        match = "✓ MATCH" if abs(bf_ret - dp_ret) < 1e-6 else "✗ MISMATCH"
        print(f"  {'Brute-Force':<20} {bf_ret:>10.2f}  [{match}]")

    gap = dp_ret - gr_ret
    pct = (gap / dp_ret * 100) if dp_ret > 0 else 0.0
    print(f"\n  Greedy gap vs DP : {gap:+.2f}  ({pct:.2f}% suboptimal)")


# ═══════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════

def _bar(width: int = 60) -> str:
    return "═" * width


def print_portfolio(label: str, max_ret: float, selected: list,
                    ids, names, costs, returns) -> None:
    total_cost = sum(costs[i] for i in selected)
    print(f"\n{_bar()}")
    print(f"  {label}")
    print(_bar())
    print(f"  Maximum Return  : ${max_ret:>10,.2f}K")
    print(f"  Total Cost Used : ${total_cost:>10,}K")
    print(f"  Items Selected  : {len(selected)}")
    print(f"\n  {'ID':<12} {'Name':<22} {'Cost':>6} {'Return':>8} "
          f"{'Ratio':>6}")
    print(f"  {'-'*58}")
    for i in selected:
        ratio = (
            returns[i] / costs[i]
            if costs[i] != 0
            else (float('inf') if returns[i] > 0 else 0.0)
        )
        print(f"  {ids[i]:<12} {names[i]:<22} {costs[i]:>6} "
              f"{returns[i]:>8.2f}  {ratio:>6.2f}")
    print(_bar())


def print_comparison(dp_ret, dp_sel, gr_ret, gr_sel, costs, returns) -> None:
    dp_cost = sum(costs[i] for i in dp_sel)
    gr_cost = sum(costs[i] for i in gr_sel)
    gap = dp_ret - gr_ret
    pct = (gap / dp_ret * 100) if dp_ret > 0 else 0.0

    print(f"\n{_bar()}")
    print("  DP vs GREEDY – FINAL COMPARISON")
    print(_bar())
    print(f"  {'Metric':<28} {'DP':>12} {'Greedy':>12}")
    print(f"  {'-'*55}")
    print(f"  {'Max Return ($K)':<28} {dp_ret:>12,.2f} {gr_ret:>12,.2f}")
    print(f"  {'Total Cost Used ($K)':<28} {dp_cost:>12,} {gr_cost:>12,}")
    print(f"  {'Items Selected':<28} {len(dp_sel):>12} {len(gr_sel):>12}")
    print(f"  {'Return Difference ($K)':<28} {gap:>12,.2f}")
    print(f"  {'Greedy Suboptimality':<28} {pct:>11.2f}%")
    verdict = "DP is STRICTLY BETTER" if gap > 1e-6 else \
              "Both found same value"
    print(f"\n  Verdict: {verdict}")
    print(_bar())


# ═══════════════════════════════════════════════════════════
#  8 – MAIN PIPELINE
# ═══════════════════════════════════════════════════════════

def main():
    CSV_FILE = "investments.csv"
    BUDGET = 500    # $500K total capital

    # ── Header ────────────────────────────────────────────
    print(_bar())
    print("  0/1 Knapsack – Investment Portfolio Optimizer")
    print("  Dynamic Programming  |  Python Implementation")
    print(_bar())

    # ══════════════════════════════════════════════════════
    #  PART A – Named Test Cases (small, verifiable)
    # ══════════════════════════════════════════════════════
    print("\n" + "═"*60)
    print("  PART A – NAMED TEST CASES  (brute-force verified)")
    print("═"*60)

    # Test 1: Classic textbook example
    run_test_case(
        name="Classic 5-item Textbook",
        costs=[2,  2,  3,  5,  7],
        returns=[6, 10, 12, 13, 20],
        budget=10
    )

    # Test 2: Greedy FAILS – one big item beats many small high-ratio items
    run_test_case(
        name="Greedy Failure Demo",
        costs=[1,  1,  1,  1,  1,  6],
        returns=[3,  3,  3,  3,  3, 16],
        budget=6
        # Greedy: picks 5 items of ratio 3.0 → return=15
        # DP:     picks the single item of cost 6 → return=16
    )

    # Test 3: All items fit – both algorithms must agree
    run_test_case(
        name="All Items Fit (edge case)",
        costs=[1, 2, 3],
        returns=[5, 8, 9],
        budget=100
    )

    # Test 4: Budget too tight – only one item can be chosen
    run_test_case(
        name="Tight Budget",
        costs=[10, 20, 30],
        returns=[60, 90, 50],
        budget=15
    )

    # Test 5: Single item
    run_test_case(
        name="Single Item",
        costs=[5],
        returns=[10],
        budget=10
    )

    # Test 6: Two items, choose the better one
    run_test_case(
        name="Two Items, Choose Better",
        costs=[5, 5],
        returns=[10, 8],
        budget=5
    )

    # Test 7: No items fit
    run_test_case(
        name="No Items Fit",
        costs=[10, 20],
        returns=[5, 8],
        budget=5
    )

    # Test 8: Large gap – DP clearly beats greedy
    run_test_case(
        name="Large Greedy Gap",
        costs=[3,  3,  3,  3,  10],
        returns=[4,  4,  4,  4,  20],
        budget=10
        # Greedy: picks 3 small items (ratio 1.33) → return=12
        # DP:     picks the single big item (return=20) → return=20
    )
    print("\n\n" + "═"*60)
    print("  PART B – FULL DATASET  (investments.csv)")
    print("═"*60)

    ids, names, costs, returns = load_investments(CSV_FILE)
    n = len(ids)
    print(f"  Items: {n}  |  Budget: ${BUDGET}K")

    # ── 2D DP ──────────────────────────────────────────────
    t0 = time.perf_counter()
    dp_ret, dp_table = knapsack_dp_2d(costs, returns, BUDGET)
    dp_time = (time.perf_counter() - t0) * 1000

    dp_sel = traceback(dp_table, costs, BUDGET)
    print_portfolio("DYNAMIC PROGRAMMING RESULT", dp_ret, dp_sel,
                    ids, names, costs, returns)
    print(f"\n  DP (2D) Runtime : {dp_time:.3f} ms")

    # ── 1D DP (verify + time) ──────────────────────────────
    t0 = time.perf_counter()
    dp1d_ret = knapsack_dp_1d(costs, returns, BUDGET)
    dp1d_time = (time.perf_counter() - t0) * 1000

    match = "✓ MATCH" if abs(dp_ret - dp1d_ret) < 1e-6 else "✗ MISMATCH"
    print(f"  DP (1D) Runtime : {dp1d_time:.3f} ms  →  "
          f"${dp1d_ret:,.2f}K  [{match}]")

    # ── Greedy ─────────────────────────────────────────────
    gr_ret, gr_sel = knapsack_greedy(costs, returns, BUDGET)
    print_portfolio("GREEDY RESULT", gr_ret, gr_sel,
                    ids, names, costs, returns)

    # ── Comparison ─────────────────────────────────────────
    print_comparison(dp_ret, dp_sel, gr_ret, gr_sel, costs, returns)

    # ── Complexity summary ─────────────────────────────────
    print("\n  COMPLEXITY SUMMARY")
    print(f"  {'─'*45}")
    print(f"  n  (number of investments) = {n}")
    print(f"  W  (budget capacity)       = {BUDGET}")
    print(f"  n × W                      = {n * BUDGET:,}  operations / cells")
    print(f"  2D DP space  O(n×W)        = {n * BUDGET:,}  float cells")
    print(f"  1D DP space  O(W)          = {BUDGET:,}  float cells  "
          f"(×{n} smaller)")
    print(f"  Greedy time  O(n log n)    = "
          f"{int(n * (n.bit_length()-1)):,}  comparisons (approx)")
    print(f"  DP time      O(n×W)        = {n * BUDGET:,}  operations")


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for s in self.streams:
            s.write(text)

    def flush(self):
        for s in self.streams:
            s.flush()


if __name__ == "__main__":
    output_path = "output_results.txt"
    with open(output_path, "w", encoding="utf-8") as out_file:
        tee = Tee(sys.stdout, out_file)
        with redirect_stdout(tee):
            main()
    print(f"\n[✓] Full output saved to '{output_path}'")
