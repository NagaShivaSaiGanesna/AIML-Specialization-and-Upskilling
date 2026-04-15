# K-Means Clustering — Selecting K, WCSS, and Distance Metrics — Complete Study Guide

---

## 1. The Central Problem — How Do We Choose K?

In K-Means clustering, $k$ is the number of clusters you instruct the algorithm to find. In toy examples, you can visually inspect the data and make an educated guess. But in the real world:

- Data lives in dozens or hundreds of dimensions — no visual inspection possible
- Data points heavily overlap
- There is no label to tell you how many true groups exist

We need a **principled, mathematical method** to choose $k$. That method is built on a metric called **WCSS** and a technique called the **Elbow Method**.

---

## 2. Within-Cluster Sum of Squares (WCSS)

### 2.1 Definition

**WCSS** (Within-Cluster Sum of Squares) measures how **compact** your clusters are — i.e., how close each data point is to its assigned centroid. The lower the WCSS, the tighter and better-defined the clusters.

$$\text{WCSS} = \sum_{j=1}^{k} \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \boldsymbol{\mu}_j\|^2$$

where:
- $k$ = number of clusters
- $C_j$ = the set of all points assigned to cluster $j$
- $\boldsymbol{\mu}_j$ = centroid (mean) of cluster $j$
- $\|\mathbf{x}_i - \boldsymbol{\mu}_j\|^2$ = squared Euclidean distance from point $\mathbf{x}_i$ to its centroid

### 2.2 Intuition — Why Does WCSS Decrease as K Increases?

| $k$ | What happens | WCSS |
|---|---|---|
| $k=1$ | One centroid tries to represent all data | Very high — all points far from a single centre |
| $k=2$ | Two centroids split the data | Significantly lower |
| $k=3$ | Three centroids, tighter groupings | Lower still |
| $k=n$ | Every point is its own centroid | Zero — perfectly "compact" but meaningless |

As $k$ increases, each centroid has fewer points to represent, so every point is closer to its centroid. WCSS **monotonically decreases** as $k$ grows. But a WCSS of zero at $k = n$ gives us no useful grouping at all — we've simply memorised the data.

This leads to the key question: **where is the sweet spot?**

---

## 3. The Elbow Method

### 3.1 Core Idea

Plot WCSS against $k$ (from $k = 1$ to some maximum, e.g., 20). The curve will look like this:

```
WCSS
  │
  │*
  │  *
  │    *
  │      * ← Elbow point
  │         * * * * * * *  (stabilises)
  └──────────────────────── k
     1  2  3  4  5  6  7
```

The curve drops steeply at first, then **bends and flattens** — resembling a human elbow. The bend point is where:
- Adding one more centroid produces a **large reduction** in WCSS up to this point
- After this point, adding more centroids yields **diminishing returns** — the WCSS barely improves

**The optimal $k$ is at the elbow — the point of abrupt decrease followed by stabilisation.**

### 3.2 Why This Makes Sense

Before the elbow: each new centroid is capturing a genuinely distinct group in the data — real structure is being discovered.

After the elbow: each new centroid is splitting an already-compact cluster into arbitrary sub-clusters — you're fitting noise, not structure.

### 3.3 Algorithm for Applying the Elbow Method

```
For k = 1 to k_max (e.g., 20):
    1. Run K-Means with k clusters
    2. Compute WCSS for this k
    3. Plot (k, WCSS)

Find the "elbow" — the k where WCSS drops sharply
and then plateaus → this is your optimal k
```

---

## 4. Distance Metrics in K-Means

K-Means relies on a **distance function** to assign each point to its nearest centroid. The choice of distance metric has significant practical implications.

### 4.1 Euclidean Distance

**Euclidean distance** is the straight-line distance between two points — the most natural notion of "how far apart" two things are in geometric space.

For two points $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$ in 2D:

$$d_{\text{Euclidean}}(P_1, P_2) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

Generalised to $n$ dimensions:

$$d_{\text{Euclidean}}(\mathbf{p}, \mathbf{q}) = \sqrt{\sum_{i=1}^{n}(q_i - p_i)^2}$$

**Real-world analogy:** A drone flying directly from point A to point B in open air — it takes the shortest straight-line path with no obstacles.

### 4.2 Manhattan Distance

**Manhattan distance** (also called L1 distance or taxicab distance) sums the absolute differences along each axis — it measures distance as if you can only move along grid lines, not diagonally.

$$d_{\text{Manhattan}}(P_1, P_2) = |x_2 - x_1| + |y_2 - y_1|$$

Generalised to $n$ dimensions:

$$d_{\text{Manhattan}}(\mathbf{p}, \mathbf{q}) = \sum_{i=1}^{n} |q_i - p_i|$$

**Real-world analogy:** A taxi navigating a city grid (like Manhattan, New York) — it must travel along streets, not cut through buildings. The path is horizontal then vertical, not diagonal.

### 4.3 Euclidean vs. Manhattan — When to Use Which

| Property | Euclidean Distance | Manhattan Distance |
|---|---|---|
| **Path shape** | Straight line (diagonal allowed) | Grid-only (horizontal + vertical) |
| **Formula** | $\sqrt{\sum (q_i - p_i)^2}$ | $\sum \|q_i - p_i\|$ |
| **Sensitivity to outliers** | High — squaring amplifies large differences | Lower — absolute value is more robust |
| **Use when** | Space is continuous and unconstrained | Movement is grid-constrained, or data has outliers |
| **Real example** | Air traffic control, drone paths | Ride-share routing in city grids, network routing |
| **High-dimensional data** | Can suffer from distance concentration | More stable in high dimensions |

### 4.4 General Distance Formula — Minkowski

Both Euclidean and Manhattan are special cases of the **Minkowski distance**:

$$d_{\text{Minkowski}}(\mathbf{p}, \mathbf{q}) = \left(\sum_{i=1}^{n} |q_i - p_i|^r\right)^{1/r}$$

- When $r = 1$: **Manhattan distance**
- When $r = 2$: **Euclidean distance**
- When $r \to \infty$: **Chebyshev distance** (maximum coordinate difference)

---

## 5. Complete K-Means Workflow with Elbow Method

```
Step 1: Standardise/normalise features
         ↓
Step 2: Run Elbow Method (k = 1 to k_max)
        → Plot WCSS vs. k
        → Identify elbow point → optimal k*
         ↓
Step 3: Run K-Means with k = k*
        → Initialise k* centroids
        → Assign each point to nearest centroid (by Euclidean distance)
        → Recompute centroids as cluster means
        → Repeat until convergence
         ↓
Step 4: Validate with Silhouette Score
         ↓
Step 5: Interpret and label clusters
```

---

## 6. Limitations, Assumptions & Pitfalls

### Limitations
- **The elbow is not always obvious.** In many real datasets the WCSS curve decreases gradually with no sharp bend. In such cases, the elbow is ambiguous and you must supplement it with Silhouette Scoring or domain knowledge.
- **WCSS cannot compare across different datasets or different feature spaces.** WCSS is scale-dependent — a WCSS of 500 means nothing in isolation; it only has meaning relative to other WCSS values for the same dataset with different $k$.

### Assumptions
- **K-Means with Euclidean distance assumes spherical, roughly equal-sized clusters.** If true clusters are elongated, crescent-shaped, or vastly different in size, WCSS minimisation will produce misleading cluster assignments.
- **All features are equally important.** WCSS treats all dimensions symmetrically. Irrelevant features inflate distances and distort cluster assignments. Feature selection or scaling is essential.

### Pitfalls
- **Never skip feature standardisation.** If salary ranges from \$20K–\$500K and age ranges from 20–60, Euclidean distance is completely dominated by salary. Standardise all features to zero mean and unit variance before running K-Means.
- **Running K-Means only once.** K-Means is sensitive to centroid initialisation (the subject of the next lecture). A single run may converge to a local minimum. Always run multiple times with different random seeds and take the result with lowest WCSS (use `n_init=10` or higher in scikit-learn).
- **Trusting the elbow blindly without validation.** The elbow method is a heuristic, not a proof. Always cross-validate the chosen $k$ using Silhouette Scoring and domain interpretation before deploying cluster assignments.
- **Using Euclidean distance on high-dimensional sparse data** (e.g., text TF-IDF vectors). In high dimensions, Euclidean distances concentrate — all points become roughly equidistant. Use **cosine similarity** instead for text and sparse data.

---

## 7. FAANG-Level Q&A

**Q1. What if the elbow plot shows no clear elbow — WCSS decreases smoothly without any sharp bend? How do you choose $k$?**

A smooth elbow plot typically means the data has no strongly separated natural cluster structure — points are distributed continuously without clear gaps. In this scenario, supplementing with **Silhouette Scoring** is the correct move: compute the average silhouette score for each $k$ and select the $k$ that maximises it, since it directly measures cluster quality (cohesion vs. separation) rather than just compactness. Additionally, examine whether the problem actually requires hard clustering — **Gaussian Mixture Models** with BIC/AIC model selection handle ambiguous cluster boundaries more gracefully. Domain knowledge should also anchor the decision: if a business stakeholder needs exactly 4 customer segments for operational reasons, that constraint can override the statistical optimum.

---

**Q2. What if two very different distance metrics (Euclidean vs. Manhattan) produce completely different cluster assignments on the same data? Which do you trust?**

Different cluster assignments indicate the data's geometry is sensitive to the distance function, meaning the clusters are not robustly spherical and compact — a warning sign that K-Means may not be the right algorithm regardless of metric. Evaluate both solutions using Silhouette Scoring under each respective distance definition; the configuration with higher silhouette score is better aligned with its own distance notion. If the data has outliers, Manhattan is likely more reliable since it is less sensitive to extreme values. For elongated or non-spherical clusters, switch to **DBSCAN** or **Gaussian Mixture Models** which do not assume spherical cluster geometry.

---

**Q3. What if WCSS is very low but the clusters are not useful for the business problem — for example, all customers in one cluster live on the same street but have nothing else in common?**

Low WCSS guarantees geometric compactness, not semantic meaningfulness. This is the fundamental limitation of optimising WCSS without business context — the algorithm finds the most spatially tight groupings, which may have no actionable interpretation. The solution is to include only **business-relevant features** in the clustering input (e.g., purchase frequency, average spend, product category) and exclude geographic co-ordinates if location is not a relevant segmentation criterion. Post-clustering validation must always include domain expert review of cluster profiles — examine cluster centroids and ask whether each cluster tells a meaningfully different business story before deploying the segmentation.

---

**Q4. [System Design] Design a K-Means-based customer segmentation system for a global e-commerce platform with 50 million customers, 200 behavioural features, and a weekly retraining requirement.**

Preprocess 50M customer records weekly using a distributed compute layer (Apache Spark on EMR or Databricks): apply z-score standardisation per feature, compute it on training data only, and store scaler parameters in a versioned feature store. Run the Elbow Method on a **stratified 1% sample** (~500K customers) for $k = 2$ to $15$ using Mini-Batch K-Means (scikit-learn's `MiniBatchKMeans`), which approximates full K-Means in $O(b \cdot k \cdot d)$ time per batch rather than $O(n \cdot k \cdot d)$; supplement with Silhouette Scoring to resolve ambiguous elbows. Train the final K-Means model at the chosen $k^*$ on the full 50M records using distributed Mini-Batch K-Means, storing the centroid matrix in a model registry (MLflow). Push cluster IDs to a low-latency key-value store (Redis or DynamoDB) keyed by customer ID for real-time lookup by recommendation, pricing, and marketing services. Monitor cluster drift weekly using a **centroid stability score** (cosine similarity between this week's and last week's centroids); if any centroid shifts beyond a threshold or Silhouette score drops below 0.35, trigger an automated retraining alert before the weekly job runs.