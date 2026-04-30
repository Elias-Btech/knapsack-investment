<div align="center">

# 💼 Investment Portfolio Optimizer
### 0/1 Knapsack — Dynamic Programming vs Greedy

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-Dynamic%20Programming-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)
![University](https://img.shields.io/badge/University-Aksum-blue?style=for-the-badge)

> **Given $500,000 and 120 investment opportunities — find the exact combination that maximizes return.**

</div>

---

## 🧠 The Problem

An investor cannot partially buy a house or take half a bond position. Each opportunity is either **fully taken or skipped** — that's the 0/1 constraint.

| Knapsack Term | Investment Term | Description |
|---|---|---|
| Weight | Cost | Capital required ($1K units) |
| Value | Return | Expected profit |
| Capacity | Budget | $500,000 total |
| Item | Opportunity | Stock, bond, crypto, real estate... |

Brute force checks **2¹²⁰ ≈ 1.3 × 10³⁶** combinations — impossible. Dynamic Programming solves it in milliseconds.

---

## 📁 Project Structure

```
knapsack_investment/
│
├── 🐍 knapsack_dp.py           → Core solver: DP (2D & 1D), Greedy, Brute-Force
├── 🐍 generate_dataset.py      → Generates investments.csv (120 items, 3 tiers)
├── 🐍 visualize_results.py     → Produces 6 polished comparison charts
│
├── 📊 investments.csv          → 120 globally known investments (cost & return)
├── 📄 output_results.txt       → Full console output saved automatically
├── 📋 requirements.txt         → Python dependencies (matplotlib)
│
├── 📊 charts/                  → 6 generated PNG charts (300 DPI)
│   ├── comparison_dp_vs_greedy.png   → Return & budget utilization bar chart
│   ├── portfolio_dp.png              → DP optimal portfolio breakdown
│   ├── portfolio_greedy.png          → Greedy portfolio breakdown
│   ├── test_cases_comparison.png     → All 8 test cases side by side
│   ├── complexity_comparison.png     → Runtime & memory usage comparison
│   └── investment_distribution.png  → Cost vs Return scatter (120 items)
│
├── 📸 screenshoots/            → 9 program output screenshots
├── 📄 Report .pdf              → Full academic report
└── 📖 README.md                → You are here
```

---

## 🚀 How to Run

**Step 1 — Generate the dataset**
```bash
py generate_dataset.py
```

**Step 2 — Run the solver**
```bash
py knapsack_dp.py
```
> Output is automatically saved to `output_results.txt`

**Step 3 — Generate visualization charts (optional)**
```bash
pip install matplotlib
py visualize_results.py
```
> Creates 6 charts in the `charts/` folder

**Requirements:** Python 3.7+ · No external libraries for core solver · `matplotlib` optional for charts

---

## 📊 Results

### Part A — 8 Named Test Cases (brute-force verified)

| Test Case | DP | Greedy | Gap |
|---|---|---|---|
| Classic 5-item Textbook | 35.00 | 28.00 | ⚠️ 20% suboptimal |
| Greedy Failure Demo | 16.00 | 15.00 | ⚠️ 6.25% suboptimal |
| All Items Fit | 22.00 | 22.00 | ✅ 0% |
| Tight Budget | 60.00 | 60.00 | ✅ 0% |
| Single Item | 10.00 | 10.00 | ✅ 0% |
| Two Items, Choose Better | 10.00 | 10.00 | ✅ 0% |
| No Items Fit | 0.00 | 0.00 | ✅ 0% |
| Large Greedy Gap | 20.00 | 20.00 | ✅ 0% |

### Part B — Full 120-item Dataset ($500K budget)

```
╔══════════════════════════════════════════╗
║  Maximum Return  :  $2,633.17K           ║
║  Total Cost Used :  $500K  (full budget) ║
║  Items Selected  :  37 investments       ║
╠══════════════════════════════════════════╣
║  DP (2D) Runtime :  11.989 ms            ║
║  DP (1D) Runtime :   6.771 ms  ✓ MATCH  ║
╚══════════════════════════════════════════╝
```

---

## ⚡ Time & Space Complexity Analysis

### Summary Table

| Algorithm | Time Complexity | Space Complexity | Optimal? | Measured Runtime |
|---|---|---|---|---|
| DP (2D) | O(n × W) | O(n × W) | ✅ Yes | 11.99 ms |
| DP (1D) | O(n × W) | O(W) | ✅ Yes | 6.77 ms |
| Greedy | O(n log n) | O(n) | ❌ No | < 1 ms |
| Brute-Force | O(2ⁿ) | O(n) | ✅ Yes | Infeasible (n>20) |

> n = 120 investments · W = 500 ($500K budget) · n × W = 60,000 cells

---

### 1. Dynamic Programming — 2D Table

**Time: O(n × W)**

The algorithm fills a table of `(n+1)` rows and `(W+1)` columns.
For each item `i` from `1` to `n`, and each budget `w` from `0` to `W`,
it performs exactly one comparison:

```
dp[i][w] = max(dp[i-1][w],  dp[i-1][w - cost[i]] + return[i])
```

This gives **n × W** total operations.
With n=120 and W=500: **120 × 500 = 60,000 operations**.

**Space: O(n × W)**

The full table is kept in memory for traceback — all `(n+1) × (W+1)` cells.
With n=120 and W=500: **121 × 501 = 60,621 float cells ≈ 473 KB**.

---

### 2. Dynamic Programming — 1D Space-Optimised

**Time: O(n × W)**

Identical recurrence to 2D DP — still fills n × W values.
The key difference is the traversal direction: **right-to-left** (W down to cost[i]).

This is mandatory for the 0/1 constraint. Left-to-right traversal would allow
an item to be selected multiple times (unbounded knapsack), which is incorrect here.

**Space: O(W)**

Only a single array of size `W+1` is maintained — the previous row is overwritten in-place.
With W=500: **501 float cells** — **120× more memory-efficient** than the 2D version.

> Trade-off: the 1D version cannot perform traceback (no history of which items were chosen).
> It is used here to verify the optimal value and measure the space saving.

---

### 3. Greedy Algorithm

**Time: O(n log n)**

The greedy approach has two steps:
1. Compute the return/cost ratio for each item — **O(n)**
2. Sort all items by ratio in descending order — **O(n log n)**
3. Scan sorted items and pick each one if it fits — **O(n)**

The dominant step is sorting, giving **O(n log n)** overall.
With n=120: approximately **120 × log₂(120) ≈ 120 × 6.9 ≈ 828 comparisons**.

**Space: O(n)**

Only the ratio array and sorted index list are stored — both of size n.

> ⚠️ Greedy is NOT guaranteed optimal for 0/1 Knapsack.
> It fails when a combination of lower-ratio items yields a higher total return
> than the top-ratio items alone. Proven by the "Greedy Failure" test case:
> 5 items of ratio 3.0 → return=15, but 1 item of ratio 2.67 → return=16.

---

### 4. Brute-Force (Correctness Verifier)

**Time: O(2ⁿ)**

Enumerates all possible subsets of n items.
With n=120: **2¹²⁰ ≈ 1.3 × 10³⁶** subsets — completely infeasible.
Used only on the 8 small test cases (n ≤ 6) to verify DP correctness.
All 8 test cases confirmed ✓ MATCH.

---

### 5. Why DP Beats Greedy

Greedy works correctly for the **Fractional Knapsack** (where items can be split),
because the ratio-based ordering is provably optimal when partial selection is allowed.

For **0/1 Knapsack** (no splitting), greedy breaks down because:
- It makes locally optimal choices (highest ratio first)
- But local optimality does not guarantee global optimality
- A single large-return item may be skipped in favour of many small high-ratio items

DP avoids this by evaluating **every possible combination implicitly** through the
recurrence table — guaranteeing the global optimum in polynomial time.

---

## � Visualization Charts

Run `py visualize_results.py` to generate 6 professional charts:

1. **DP vs Greedy Comparison** — side-by-side bar charts (return & cost)
2. **DP Portfolio Allocation** — pie chart of top 10 investments
3. **Greedy Portfolio Allocation** — pie chart of top 10 investments
4. **Test Case Results** — bar chart showing all 8 test cases
5. **Complexity Comparison** — runtime and memory usage
6. **Investment Distribution** — scatter plot of all 120 investments (cost vs return)

All charts saved to `charts/` folder as high-resolution PNG files (300 DPI).

---


## 🏆 Key Result

> DP found the **optimal portfolio of $2,633,170 return** from 37 investments using exactly the full $500K budget.
> Greedy is proven **up to 20% suboptimal** on crafted inputs — even when it matches DP on this dataset, it is never guaranteed.

---

## 👥 Authors

<div align="center">

| Name | Student ID |
|---|---|
| Elias Araya | Aku1601720 |
| Mulu G/Medhin | Aku1602465 |
| Arsema Birhane | Aku1602222 |

**Aksum University · Design and Analysis of Algorithms (DAA) · April 2026**

</div>

---

<div align="center">

*This project is for educational purposes only.*

</div>
