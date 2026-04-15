# Mathematical Intuition Behind PCA — Complete Study Guide

---

## 1. Recapping the Goal

From the geometric intuition, we established that PCA's mission is:

> **Find the best unit vector (direction) onto which projecting all data points yields maximum variance.**

The mathematical challenge is: there are infinitely many possible directions in $n$-dimensional space. We cannot try them all by brute force. This lecture explains the two mathematical pillars that make PCA tractable — **projections** and a **variance-based cost function** — and introduces **eigendecomposition** as the efficient solver.

---

## 2. Pillar 1 — Projections

### 2.1 Setting Up the Problem

Consider a 2D dataset. Pick any single data point $P_1 = (x_1, y_1)$. Treat it as a **vector** from the origin.

Now suppose we have a candidate direction represented as a **unit vector** $\mathbf{u} = (u_1, u_2)$.

A unit vector satisfies:

$$\|\mathbf{u}\| = \sqrt{u_1^2 + u_2^2} = 1$$

We want to project $P_1$ onto this candidate direction $\mathbf{u}$ to find where $P_1$ "lands" on that line.

### 2.2 The Projection Formula

The projection of vector $\mathbf{p}_1$ onto unit vector $\mathbf{u}$ is:

$$\text{proj}_{\mathbf{u}}(\mathbf{p}_1) = \frac{\mathbf{p}_1 \cdot \mathbf{u}}{\|\mathbf{u}\|}$$

Since $\mathbf{u}$ is a unit vector, $\|\mathbf{u}\| = 1$, so this simplifies beautifully to just the **dot product**:

$$p_1' = \mathbf{p}_1 \cdot \mathbf{u} = x_1 u_1 + y_1 u_2$$

This scalar $p_1'$ is the **signed distance** from the origin to the projected point along $\mathbf{u}$.

### 2.3 Projecting All Data Points

We apply this to every point in the dataset:

$$p_i' = \mathbf{p}_i \cdot \mathbf{u} \quad \text{for } i = 1, 2, \ldots, n$$

After projecting all $n$ points, we obtain a 1D set of scalar values:

$$\{p_1',\ p_2',\ p_3',\ \ldots,\ p_n'\}$$

We now rename these for clarity as:

$$\{x_0',\ x_1',\ x_2',\ \ldots,\ x_n'\}$$

Each value represents how far along $\mathbf{u}$ a particular data point lies. We have successfully collapsed 2D data into 1D — the question is whether we chose the **best** direction $\mathbf{u}$.

---

## 3. Pillar 2 — The Cost Function: Maximise Variance

### 3.1 Computing Variance on Projected Points

Once we have all projected scalar values $\{x_0', x_1', \ldots, x_n'\}$, we compute their variance using the standard formula:

$$\text{Var} = \frac{\sum_{i=1}^{n}(x_i' - \bar{x}')^2}{n}$$

where $\bar{x}' = \frac{1}{n}\sum_{i=1}^{n} x_i'$ is the mean of the projected values.

### 3.2 The Optimisation Objective

PCA frames its entire mission as an optimisation problem:

$$\mathbf{u}^* = \underset{\mathbf{u},\ \|\mathbf{u}\|=1}{\arg\max}\ \text{Var}(\mathbf{p}_1 \cdot \mathbf{u},\ \mathbf{p}_2 \cdot \mathbf{u},\ \ldots,\ \mathbf{p}_n \cdot \mathbf{u})$$

In plain English: **find the unit vector $\mathbf{u}$ such that after projecting all data points onto it, the resulting 1D values have the highest possible variance.**

This is the **cost function** of PCA — and the direction that maximises it becomes **Principal Component 1 (PC1)**.

### 3.3 Why Maximising Variance = Minimising Information Loss

There is an elegant dual way to understand this. When you project a point onto a line, you incur a **reconstruction error** — the perpendicular distance from the original point to its projection. It can be mathematically shown that:

$$\underbrace{\text{Maximise projected variance}}_{\text{PCA's objective}} \iff \underbrace{\text{Minimise reconstruction error}}_{\text{information loss}}$$

These two objectives are equivalent. PCA simultaneously maximises what it keeps and minimises what it throws away.

---

## 4. The Problem With Brute Force

We cannot try every possible direction to find the maximum variance. Even in 2D, there are infinitely many unit vectors. In 500 dimensions, the search space is astronomically large.

We need a smarter approach — and that is **Eigendecomposition**.

---

## 5. The PCA Algorithm — Step by Step

### Step 1: Standardise the Data

Before anything else, subtract the mean and divide by the standard deviation for each feature:

$$z_i = \frac{x_i - \mu}{\sigma}$$

This ensures no single feature dominates due to scale differences.

### Step 2: Compute the Covariance Matrix

For a dataset with $d$ features, compute the $d \times d$ **covariance matrix** $\Sigma$:

$$\Sigma = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$$

Each entry $\Sigma_{ij}$ measures how much features $i$ and $j$ vary together. The diagonal entries are the individual feature variances.

For 2 features (house size $X_1$, number of rooms $X_2$):

$$\Sigma = \begin{bmatrix} \text{Var}(X_1) & \text{Cov}(X_1, X_2) \\ \text{Cov}(X_2, X_1) & \text{Var}(X_2) \end{bmatrix}$$

### Step 3: Perform Eigendecomposition

Solve the fundamental **eigenvalue equation**:

$$\Sigma \mathbf{v} = \lambda \mathbf{v}$$

where:
- $\mathbf{v}$ = **eigenvector** — a direction in feature space (a candidate principal component)
- $\lambda$ = **eigenvalue** — a scalar quantifying how much variance is captured along $\mathbf{v}$

This equation says: *"Find directions $\mathbf{v}$ such that multiplying by the covariance matrix $\Sigma$ only stretches $\mathbf{v}$ (by factor $\lambda$) without rotating it."* These special directions are the natural axes of the data's variance structure.

For a $d \times d$ covariance matrix, there are exactly $d$ eigenvector–eigenvalue pairs.

### Step 4: Sort by Eigenvalue (Descending)

$$\lambda_1 \geq \lambda_2 \geq \lambda_3 \geq \cdots \geq \lambda_d$$

The eigenvector $\mathbf{v}_1$ corresponding to $\lambda_1$ (the largest eigenvalue) **is PC1** — the direction of maximum variance. This is mathematically proven via the Rayleigh quotient theorem from linear algebra.

| Eigenvector | Eigenvalue | Principal Component | Variance Captured |
|---|---|---|---|
| $\mathbf{v}_1$ | $\lambda_1$ (largest) | PC1 | Maximum |
| $\mathbf{v}_2$ | $\lambda_2$ | PC2 | Second maximum |
| $\mathbf{v}_3$ | $\lambda_3$ | PC3 | Third maximum |
| $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |
| $\mathbf{v}_d$ | $\lambda_d$ (smallest) | PC$d$ | Minimum |

### Step 5: Select Top $k$ Eigenvectors

Choose the top $k$ eigenvectors (PCs) based on how much cumulative variance you want to retain:

$$\text{Explained Variance Ratio for PC}_i = \frac{\lambda_i}{\sum_{j=1}^{d} \lambda_j}$$

$$\text{Cumulative Explained Variance} = \frac{\sum_{i=1}^{k} \lambda_i}{\sum_{j=1}^{d} \lambda_j} \geq 0.95$$

### Step 6: Project Data onto Selected Components

Form the **projection matrix** $\mathbf{W} \in \mathbb{R}^{d \times k}$ by stacking the top $k$ eigenvectors as columns:

$$\mathbf{W} = [\mathbf{v}_1\ |\ \mathbf{v}_2\ |\ \cdots\ |\ \mathbf{v}_k]$$

Project the standardised data:

$$\mathbf{Z} = \mathbf{X} \cdot \mathbf{W} \quad \in \mathbb{R}^{n \times k}$$

$\mathbf{Z}$ is your final reduced dataset — $n$ samples, each described by $k$ principal components instead of $d$ original features.

---

## 6. The Full Mathematical Flow — Visual Summary

```
Original Data X (n × d)
        ↓
  Standardise each feature (zero mean, unit variance)
        ↓
  Compute Covariance Matrix Σ (d × d)
        ↓
  Eigendecomposition: Σv = λv
  → d eigenvectors v₁, v₂, ..., vd
  → d eigenvalues  λ₁ ≥ λ₂ ≥ ... ≥ λd
        ↓
  Select top k eigenvectors by eigenvalue magnitude
  (PC1 = v₁, PC2 = v₂, ..., PCk = vk)
        ↓
  Project: Z = X · W  (n × k matrix)
        ↓
  Reduced Dataset Z — ready for modelling or visualisation
```

---

## 7. Connecting Geometry to Mathematics

| Geometric Concept | Mathematical Counterpart |
|---|---|
| "Rotate axes to align with data spread" | Eigendecomposition of covariance matrix |
| "Best direction of maximum spread" | Eigenvector with largest eigenvalue |
| "Amount of spread along a direction" | Eigenvalue $\lambda$ |
| "Project point onto new axis" | Dot product $\mathbf{p}_i \cdot \mathbf{u}$ |
| "How much information is retained" | Cumulative explained variance ratio |
| "Perpendicular new axes (PC1 ⊥ PC2)" | Eigenvectors of a symmetric matrix are orthogonal |

---

## 8. Limitations, Assumptions & Pitfalls

### Limitations
- **Eigendecomposition scales as $O(d^3)$** — for very high-dimensional data (e.g., $d = 100{,}000$ raw text features), full PCA becomes computationally prohibitive. Use **Truncated SVD** (also called Randomised PCA) which approximates only the top $k$ components efficiently.
- **Covariance matrix assumes linearity.** If features have complex non-linear interactions, the covariance matrix misses them entirely, and the eigenvectors will not find meaningful structure.

### Assumptions
- **Data must be centred (zero mean) before computing the covariance matrix.** If you skip standardisation, the covariance matrix is distorted by scale, and the resulting eigenvectors will point in misleading directions.
- **Eigenvectors are only unique up to sign.** PC1 pointing "up-right" and PC1 pointing "down-left" are the same component. This does not affect variance calculations but can confuse interpretation.

### Pitfalls
- **Confusing eigenvalues with variance percentage.** The eigenvalue $\lambda_i$ is the raw variance along PC$i$, not a percentage. Always divide by $\sum \lambda_j$ to get the explained variance ratio before making retention decisions.
- **Retaining too few components blindly.** A common mistake is always reducing to 2D for visualisation without checking the explained variance — if 2 components explain only 40% of variance, the 2D plot is deeply misleading and should not drive conclusions.
- **Applying PCA to categorical features.** PCA requires continuous, numeric input. Applying it to one-hot encoded or ordinal variables produces geometrically meaningless covariance matrices. Use **Multiple Correspondence Analysis (MCA)** for categorical data instead.

---

## 9. FAANG-Level Q&A

**Q1. What if the covariance matrix has two eigenvalues that are exactly equal? What does this mean geometrically and how does PCA handle it?**

Equal eigenvalues mean the data has identical variance in two (or more) directions — the data cloud is perfectly circular (isotropic) in that subspace, with no single "most important" axis. PCA can still proceed, but any orthogonal basis in that subspace is equally valid as a solution — the choice of eigenvectors becomes numerically arbitrary. In practice, this rarely occurs with real data due to floating-point noise, but it signals that the features in that subspace are exchangeable and carry equal information. The downstream impact is that the ordering of the corresponding PCs is meaningless, and you should retain either all or none of them based on the cumulative explained variance threshold.

---

**Q2. What if you have far more features than data samples — for instance, 50,000 gene expression features and only 200 patient samples? Can you still apply PCA?**

In this $d \gg n$ regime (called the "fat matrix" problem), the $d \times d$ covariance matrix has at most $n - 1$ non-zero eigenvalues — the remaining $d - n + 1$ eigenvalues are exactly zero, meaning most directions are completely uninformative. Full eigendecomposition of a $50{,}000 \times 50{,}000$ matrix is computationally infeasible ($O(d^3)$). The correct approach is **Truncated SVD** applied directly to the $n \times d$ data matrix $\mathbf{X}$, which computes only the top $k$ singular vectors in $O(ndk)$ time — far more tractable. This is how scikit-learn's `TruncatedSVD` and `PCA(svd_solver='randomized')` handle genomics and NLP datasets efficiently.

---

**Q3. What if after PCA you want to reconstruct the original data from the reduced representation? How much error should you expect?**

Reconstruction is achieved by projecting back through the eigenvector matrix: $\hat{\mathbf{X}} = \mathbf{Z} \cdot \mathbf{W}^T$, then reversing standardisation. The reconstruction error equals the variance captured by the **discarded** components:

$$\text{Reconstruction Error} = \sum_{i=k+1}^{d} \lambda_i$$

If you retained components explaining 95% of variance, reconstruction error corresponds to the remaining 5%. This error is spread evenly across all data points (not concentrated in outliers), which means PCA reconstructions look "blurry" rather than having specific localised errors — this is why PCA-based image compression produces uniformly soft images rather than blocky artefacts like JPEG.

---

**Q4. [System Design] Design a PCA-based anomaly detection system for network intrusion detection that processes 1 million network packets per second, each with 200 features, with a latency requirement of under 1 ms per packet.**

Offline, collect a representative baseline of normal traffic and fit PCA retaining enough components to explain 95% of variance (typically 20–40 components for network data); store the eigenvector matrix $\mathbf{W}$ and per-feature standardisation parameters in shared memory on inference nodes. The anomaly signal is the **reconstruction error** per packet: a packet is flagged as anomalous if $\|\mathbf{x} - \hat{\mathbf{x}}\|^2 > \theta$, where $\theta$ is a threshold calibrated on validation data at a desired false-positive rate — anomalous packets (intrusions) have feature patterns that PCA's normal-traffic eigenvectors cannot reconstruct well. At inference time, the pipeline is: receive raw packet features → vectorised standardisation (SIMD operations) → single matrix multiply $\mathbf{z} = \mathbf{x} \cdot \mathbf{W}$ → reconstruction $\hat{\mathbf{x}} = \mathbf{z} \cdot \mathbf{W}^T$ → compute L2 error → threshold check; on modern hardware this executes in under 0.1 ms for a 200×40 matrix, well within budget. Retrain PCA monthly on recent normal traffic to adapt to network drift, using a canary deployment that A/B tests the new threshold against the previous model before full rollout.