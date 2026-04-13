# 0/1 Knapsack – Investment Portfolio Optimizer
### Algorithm Design & Analysis | Python Implementation

---

## What This Project Does

An investor has **$500,000** and 120 investment opportunities (stocks, bonds,
real estate, crypto, etc.). This program finds the **exact combination** that
maximizes total return without exceeding the budget — using Dynamic Programming.

---

## Project Files

```
knapsack_investment/
├── generate_dataset.py    → Step 1: creates investments.csv (120 items)
├── knapsack_dp.py         → Step 2: runs DP solver + greedy comparison
├── investments.csv        → Generated dataset (120 globally known investments)
├── Report.pdf             → Academic report (PDF for submission)
├── README.md              → This file
└── screenshoots/          → All 9 program output screenshots
```

---

## How to Run

### Step 1 — Generate the dataset
```bash
py generate_dataset.py
```
Creates `investments.csv` with 120 investments using globally known names
(Apple, Bitcoin, Toyota Bond, Gold, Los Angeles House, etc.)

### Step 2 — Run the solver
```bash
py knapsack_dp.py
```
Full output is also saved automatically to `output_results.txt`

---

## Requirements

- Python 3.7 or higher
- No external libraries — uses only `csv`, `time`, `itertools` (all built-in)

---

## What the Program Outputs

### Part A — 8 Named Test Cases (brute-force verified)

| Test Case | DP Result | Greedy Result | Gap |
|-----------|-----------|---------------|-----|
| Classic 5-item Textbook | 35.00 | 28.00 | 20% suboptimal |
| Greedy Failure Demo | 16.00 | 15.00 | 6.25% suboptimal |
| All Items Fit | 22.00 | 22.00 | 0% |
| Tight Budget | 60.00 | 60.00 | 0% |
| Single Item | 10.00 | 10.00 | 0% |
| Two Items, Choose Better | 10.00 | 10.00 | 0% |
| No Items Fit | 0.00 | 0.00 | 0% |
| Large Greedy Gap | 20.00 | 20.00 | 0% |

### Part B — Full 120-item Dataset ($500K budget)

```
Maximum Return  : $2,633.17K
Total Cost Used : $500K  (full budget used)
Items Selected  : 37

DP (2D) Runtime : 11.989 ms   Space: O(n×W) = 60,000 cells
DP (1D) Runtime :  6.771 ms   Space: O(W)   =    500 cells  [✓ MATCH]
```

---

## Screenshots

### Figure 1 – Test Cases: DP vs Greedy (Classic Example)
![Test Cases DP vs Greedy](screenshoots/Screenshot_01_Test_Cases_DP_vs_Greedy.jpg)

### Figure 2 – Greedy Failure Proof + Edge Case
![Greedy Failure and Edge Case](screenshoots/Screenshot_02_Greedy_Failure_and_Edge_Case.jpg)

### Figure 3 – Tight Budget & Single Item
![Tight Budget and Single Item](screenshoots/Screenshot_03_Tight_Budget_and_Single_Item.jpg)

### Figure 4 – Choose Better & No Items Fit
![Choose Better and No Items Fit](screenshoots/Screenshot_04_Choose_Better_and_No_Items_Fit.jpg)

### Figure 5 – Last Test Case + Full Dataset Begins
![Last TestCase and DP Result Summary](screenshoots/Screenshot_05_Last_TestCase_and_DP_Result_Summary.jpg)

### Figure 6 – DP Optimal Portfolio (All 37 Investments)
![DP Optimal Portfolio Full List](screenshoots/Screenshot_06_DP_Optimal_Portfolio_Full_List.jpg)

### Figure 7 – Runtime Comparison + 1D DP Verification
![Runtime and Greedy Summary](screenshoots/Screenshot_07_Runtime_and_Greedy_Summary.jpg)

### Figure 8 – Greedy Portfolio (All 37 Investments)
![Greedy Full Portfolio List](screenshoots/Screenshot_08_Greedy_Full_Portfolio_List.jpg)

### Figure 9 – Final Comparison Table + Complexity Summary
![Final Comparison and Complexity](screenshoots/Screenshot_09_Final_Comparison_and_Complexity.jpg)

---

## Algorithm Summary

| Algorithm | Time       | Space    | Optimal | Runtime  |
|-----------|------------|----------|---------|----------|
| DP (2D)   | O(n × W)   | O(n × W) | Yes     | 11.99 ms |
| DP (1D)   | O(n × W)   | O(W)     | Yes     | 6.77 ms  |
| Greedy    | O(n log n) | O(n)     | No      | < 1 ms   |

Where n = 120 investments, W = 500 ($500K budget)

---

## Key Result

> DP found the optimal portfolio of **$2,633,170 return** from 37 investments
> using exactly the full $500K budget. Greedy is proven suboptimal on
> crafted inputs (up to 20% worse) even though it matched DP on this dataset.

---

## Authors

| Name           | ID          |
|----------------|-------------|
| Elias Araya    | Aku1601720  |
| Mulu G/Medhin  | Aku1602465  |
| Arsema Birhane | Aku1602222  |

- University: Aksum University
- Course: Design and Analysis of Algorithms (DAA)
- Date: April 2026

---

## License

This project is for educational purposes only.
