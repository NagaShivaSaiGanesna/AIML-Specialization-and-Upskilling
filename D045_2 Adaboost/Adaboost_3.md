# AdaBoost: Sampling, Iteration & Final Prediction (Steps 5–7)

> **Prerequisites**: Steps 1–4 covered in the previous guide — stump selection, weight initialization, error calculation, alpha computation, weight update, and normalization.

---

## 1. Quick State Recap Before Step 5

After completing Steps 1–4 on our 7-record credit card dataset, we have:

| Record | Salary | Credit | Approved | Normalized Weight | Bin Range |
|---|---|---|---|---|---|
| 1 | ≤ 50K | Bad | No | 0.083 | 0.000 → 0.083 |
| 2 | ≤ 50K | Good | Yes | 0.083 | 0.083 → 0.166 |
| 3 | ≤ 50K | Normal | **Yes** ❌ | **0.500** | **0.166 → 0.666** |
| 4 | ≤ 50K | Bad | No | 0.083 | 0.666 → 0.749 |
| 5 | > 50K | Good | Yes | 0.083 | 0.749 → 0.832 |
| 6 | > 50K | Good | Yes | 0.083 | 0.832 → 0.915 |
| 7 | > 50K | Bad | No | 0.083 | 0.915 → 1.000 |

Record 3 (the misclassified one) occupies **50% of the [0, 1] range** — meaning any random draw has a 1-in-2 chance of picking it.

---

## 2. Step 5 — Weighted Random Sampling (Building the Next Dataset)

### 2.1 The Core Idea

We need to build a **new 7-record training dataset** for Stump 2. Instead of equal random sampling, we sample with probability proportional to normalized weights — so misclassified records appear more often.

**Mechanism**: Draw 7 random numbers $r \in [0, 1]$ uniformly. For each $r$, find which bin it falls into and select that record.

### 2.2 Sampling Walkthrough

| Draw | Random $r$ | Bin it falls in | Record Selected | Correctly Classified? |
|---|---|---|---|---|
| 1 | 0.50 | 0.166 → 0.666 | Record 3 (> 50K, Normal, Yes) | ❌ Wrong |
| 2 | 0.10 | 0.083 → 0.166 | Record 2 (≤ 50K, Good, Yes) | ✓ |
| 3 | 0.60 | 0.166 → 0.666 | Record 3 (> 50K, Normal, Yes) | ❌ Wrong |
| 4 | 0.75 | 0.749 → 0.832 | Record 5 (> 50K, Good, Yes) | ✓ |
| 5 | 0.24 | 0.166 → 0.666 | Record 3 (> 50K, Normal, Yes) | ❌ Wrong |
| 6 | 0.32 | 0.166 → 0.666 | Record 3 (> 50K, Normal, Yes) | ❌ Wrong |
| 7 | 0.87 | 0.832 → 0.915 | Record 6 (> 50K, Good, Yes) | ✓ |

**Outcome**: Record 3 was selected **4 out of 7 times**. The new dataset is dominated by the previously misclassified record — exactly as intended.

### 2.3 Why This Works

$$P(\text{Record } i \text{ selected}) = w_i^{\text{norm}}$$

A record with weight 0.500 has a 50% chance per draw. Over 7 draws, it appears ~3.5 times in expectation. This is **bootstrap sampling with replacement**, weighted by classification error.

---

## 3. Step 6 — Train the Next Stump (Full Iteration Repeat)

The new 7-record dataset is now passed to **Stump 2**. Crucially, **all Steps 1–5 repeat from scratch** on this new dataset:

```
New Dataset (7 records, Record 3 repeated 4x)
        │
        ▼
Assign equal weights: w_i = 1/7
        │
        ▼
Build candidate stumps → select best via entropy/Gini
        │
        ▼
Compute ε₂ = Σ weights of wrong records
        │
        ▼
Compute α₂ = ½ ln((1 - ε₂) / ε₂)
        │
        ▼
Update weights → Normalize → Assign bins → Sample → Repeat
```

**Important**: The $1/7$ weight re-initialization on the new dataset is correct — weights always start equal for a fresh dataset. The "memory" of past mistakes is already encoded in the **composition of the new dataset** (Record 3 appears multiple times), not in the starting weights.

Let's say after training Stump 2, we get:

$$\alpha_2 = 0.650$$

This gets appended to our growing model:

$$F(x) = 0.896 \cdot h_1(x) + 0.650 \cdot h_2(x) + \ldots$$

By default, most AdaBoost implementations run for **100 rounds** ($N = 100$ stumps), though this is a hyperparameter you tune.

---

## 4. Step 7 — Final Prediction on New Test Data

### 4.1 The Test Input

New test record: **Salary ≤ 50K, Credit Score = Good**

We pass this through all trained stumps and collect each stump's prediction and its $\alpha$ weight.

### 4.2 Collecting Votes

Let's say we trained 4 stumps:

| Stump | $\alpha_m$ | Prediction for test record |
|---|---|---|
| $h_1$ | 0.896 | **Yes** |
| $h_2$ | 0.650 | **No** |
| $h_3$ | 0.244 | **Yes** |
| $h_4$ | −0.300 | **No** |

### 4.3 Weighted Vote Aggregation

Accumulate the weighted sum for each class:

**Score for Yes** (stumps predicting Yes get $+\alpha$):

$$S_{\text{Yes}} = \alpha_1 + \alpha_3 = 0.896 + 0.244 = 1.140$$

**Score for No** (stumps predicting No get $+\alpha$):

$$S_{\text{No}} = \alpha_2 + \alpha_4 = 0.650 + (-0.300) = 0.350$$

### 4.4 Final Decision

$$\hat{y} = \text{sign}(S_{\text{Yes}} - S_{\text{No}}) = \text{sign}(1.140 - 0.350) = \text{sign}(0.790) = \textbf{Yes}$$

Since $S_{\text{Yes}} = 1.140 > S_{\text{No}} = 0.350$, the model predicts **Credit Card Approved: Yes**.

> Notice that $h_4$ had a **negative alpha** (−0.300). This means that stump was worse than random guessing — its vote is literally inverted. When it says "No," that actually nudges the score toward "Yes."

---

## 5. Classification vs. Regression: Key Differences

| Aspect | Classification | Regression |
|---|---|---|
| **Stump selection metric** | Entropy or Gini Impurity | Mean Squared Error (MSE) |
| **Final aggregation** | $\text{sign}(\sum \alpha_m h_m(x))$ | $\sum \alpha_m h_m(x)$ (continuous value) |
| **Leaf node output** | Class label (Yes/No) | Continuous number (e.g., predicted salary) |
| **Error $\epsilon_m$** | Weighted misclassification rate | Weighted residual error |

Everything else — weight initialization, alpha computation, weight update, normalization, bin sampling — is identical.

---

## 6. The Complete AdaBoost Algorithm (End-to-End)

$$\boxed{F(x) = \text{sign}\left(\sum_{m=1}^{N} \alpha_m \cdot h_m(x)\right)}$$

**Step-by-step:**

1. Initialize $w_i = \frac{1}{n}$ for all $n$ records
2. **For** $m = 1$ to $N$:
   - Build candidate stumps; pick best $h_m$ via entropy/Gini
   - $\epsilon_m = \sum_{i:\text{wrong}} w_i$
   - $\alpha_m = \frac{1}{2}\ln\!\left(\dfrac{1-\epsilon_m}{\epsilon_m}\right)$
   - Update weights: $w_i \leftarrow w_i \cdot e^{-\alpha_m}$ (correct), $w_i \cdot e^{+\alpha_m}$ (wrong)
   - Normalize: $w_i \leftarrow \dfrac{w_i}{\sum_j w_j}$
   - Assign bins → draw $n$ random numbers → build new dataset
   - Re-initialize weights to $1/n$ on new dataset
3. Predict: $\hat{y} = \text{sign}\!\left(\sum_m \alpha_m h_m(x)\right)$

---

## 7. Limitations, Assumptions & Pitfalls

**Limitations**
- With enough rounds, repeated selection of the same misclassified records can cause **overfitting on noise**.
- The random sampling step introduces **variance across runs** — results are not fully deterministic unless a random seed is fixed.
- Negative $\alpha$ values (stumps worse than random) can destabilize training if they appear early.

**Assumptions**
- The sampling procedure assumes weights form a valid probability distribution (sum = 1) — broken if normalization is skipped.
- Bin sampling assumes the random number generator is uniform over $[0, 1]$.

**Common Pitfalls**
- **Forgetting to re-initialize weights** to $1/n$ on each new dataset. The bias correction is in the dataset composition, not the starting weights.
- **Misinterpreting negative alpha**: a stump with $\alpha < 0$ is not useless — its prediction is simply inverted. Removing it would break the model.
- **Not fixing the random seed** in production: different runs produce different datasets at each step, leading to irreproducible models.

---

## 8. FAANG-Level Q&A

**Q1. What if the same misclassified record gets sampled all 7 times in the new dataset — does the next stump just memorize it?**

If a single record fills the entire new dataset, the next stump can only learn a trivial rule that classifies that one record correctly and everything else randomly. Its weighted error $\epsilon$ will be close to 0.5, making $\alpha \approx 0$ and rendering it useless. In practice this extreme is rare — the probability of all 7 draws landing on one record (even at weight 0.5) is $0.5^7 \approx 0.78\%$. If it does occur, implementations detect $\epsilon \approx 0.5$ and skip that round.

**Q2. What if a stump produces a negative alpha — should it be discarded from the final ensemble?**

No, discarding it would be incorrect. A negative $\alpha_m$ means the stump's raw predictions should be **inverted** — wherever it says "Yes," the model treats it as evidence for "No," and vice versa. This is mathematically equivalent to flipping the stump's labels. The negative weight is automatically handled in the weighted sum $\sum \alpha_m h_m(x)$ — the stump still contributes useful signal, just in the opposite direction. Discarding it would introduce bias.

**Q3. What if we use 1000 stumps instead of 100 — will accuracy keep improving?**

Not necessarily. AdaBoost is empirically more resistant to overfitting than other methods as rounds increase — a property related to maximizing the margin of the training data. However, with noisy labels, adding more rounds will eventually overfit as mislabeled records get exponentially upweighted. The practical rule is: monitor validation loss and use early stopping. For clean data, 200–500 stumps often saturates performance; beyond that, gains are negligible and inference slows linearly.

**Q4. System Design: How would you deploy an AdaBoost model for real-time credit card approval with sub-10ms latency SLA and full audit logging of every decision?**

Serialize the trained model as an ordered list of $(\alpha_m, \text{feature\_index}, \text{threshold}, \text{left\_value}, \text{right\_value})$ tuples — for 100 stumps this is under 10KB, easily held in L1 cache. Implement inference as a tight loop in a compiled language (Go/Rust/C++): iterate over stumps, evaluate one comparison per stump, accumulate the weighted sum, apply `sign()`. On modern hardware, 100 stump evaluations complete in under 100 microseconds — well within the 10ms SLA. For audit logging, emit a structured log entry per decision containing the input features, each stump's prediction and $\alpha$, the final $S_{\text{Yes}}$ and $S_{\text{No}}$ scores, and the outcome. Ship logs asynchronously to an append-only store (Kafka → S3/BigQuery) to avoid adding latency to the critical path. Version the model artifact with a hash and include it in every log entry to ensure decisions are reproducible and traceable during audits or regulatory review.