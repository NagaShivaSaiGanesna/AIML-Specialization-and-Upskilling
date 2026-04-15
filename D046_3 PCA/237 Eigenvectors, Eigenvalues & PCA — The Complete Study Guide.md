# Eigenvectors, Eigenvalues & PCA — The Complete Study Guide

---

## 1. The Core Intuition: Why Do We Need This?

In **Principal Component Analysis (PCA)**, the central challenge is finding the best line (or plane) through your data such that projecting data onto it preserves the **maximum variance**. Losing variance means losing information, so we want to lose as little as possible.

The mathematical tools that solve this problem are **eigenvectors** and **eigenvalues** of the **covariance matrix**.

> **Key Insight:** The eigenvector with the largest corresponding eigenvalue points in the direction of greatest variance in the data. That direction becomes **Principal Component 1 (PC1)**.

---

## 2. Linear Transformation — The Foundation

### 2.1 What is a Linear Transformation?

Imagine your data lives on a grid. A **linear transformation** is a mathematical operation (represented by a matrix) that stretches, rotates, shears, or flips that entire grid in a consistent way. Every point in the space moves according to the same rule.

Mathematically, if $\mathbf{A}$ is a transformation matrix and $\mathbf{v}$ is a vector, the transformed vector is simply:

$$\mathbf{A}\mathbf{v}$$

### 2.2 What Makes Eigenvectors Special?

For *most* vectors $\mathbf{v}$, applying a transformation $\mathbf{A}$ will change both the **direction** and the **magnitude** of the vector. Eigenvectors are the rare, special vectors for which the transformation only scales them — their **direction does not change**.

This is captured by the **fundamental eigenvalue equation**:

$$\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$$

| Symbol | Meaning |
|--------|---------|
| $\mathbf{A}$ | The transformation matrix (in PCA: the covariance matrix) |
| $\mathbf{v}$ | The **eigenvector** — direction does not change under $\mathbf{A}$ |
| $\lambda$ | The **eigenvalue** — the scalar factor by which $\mathbf{v}$ is stretched or compressed |

**Intuition:** If you push a piece of dough in a random direction, it squishes in a complicated way. But eigenvectors are the "natural axes" of the transformation — push dough along them and it only stretches or compresses cleanly.

---

## 3. Step-by-Step: How PCA Uses Eigenvalues & Eigenvectors

### Step 1 — Standardize the Data

Before anything else, **standardize** each feature so it has mean $= 0$ and standard deviation $= 1$:

$$z = \frac{x - \mu}{\sigma}$$

This centers the data at the origin and prevents features with larger numeric ranges from dominating the analysis.

### Step 2 — Compute the Covariance Matrix

The **covariance matrix** $\mathbf{\Sigma}$ captures how every feature varies with every other feature. For two features $x$ and $y$:

$$\text{Cov}(x, y) = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{n - 1}$$

For a dataset with two features, the full covariance matrix is the $2 \times 2$ symmetric matrix:

$$\mathbf{\Sigma} = \begin{bmatrix} \text{Var}(x) & \text{Cov}(x,y) \\ \text{Cov}(y,x) & \text{Var}(y) \end{bmatrix}$$

**Key properties:**
- **Diagonal elements** are the variances of each individual feature.
- **Off-diagonal elements** are the covariances between feature pairs.
- The matrix is always **symmetric**: $\text{Cov}(x,y) = \text{Cov}(y,x)$.

For $d$ features, you get a $d \times d$ covariance matrix.

### Step 3 — Eigen Decomposition of the Covariance Matrix

This is called **eigen decomposition**. We solve the eigenvalue equation:

$$\mathbf{\Sigma}\mathbf{v} = \lambda\mathbf{v}$$

Rearranging to find $\lambda$:

$$(\mathbf{\Sigma} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}$$

For a non-trivial solution ($\mathbf{v} \neq \mathbf{0}$), the **characteristic equation** must hold:

$$\det(\mathbf{\Sigma} - \lambda\mathbf{I}) = 0$$

Solving this gives you the eigenvalues $\lambda_1, \lambda_2, \ldots, \lambda_d$. Substituting each $\lambda_i$ back gives the corresponding eigenvector $\mathbf{v}_i$.

### Step 4 — Rank by Eigenvalue Magnitude

| Eigenvalue Rank | Principal Component | Variance Captured |
|---|---|---|
| Largest $\lambda_1$ | PC1 | Maximum |
| 2nd largest $\lambda_2$ | PC2 | 2nd most |
| Smallest $\lambda_d$ | PC$d$ | Minimum |

### Step 5 — Project the Data

**Projection** means expressing each original data point in terms of the new principal component axes. If you want to reduce from $d$ dimensions to $k$ dimensions, you keep the top $k$ eigenvectors and project:

$$\mathbf{X}_{\text{reduced}} = \mathbf{X} \cdot \mathbf{V}_k$$

where $\mathbf{V}_k$ is the matrix of the top $k$ eigenvectors (each as a column).

---

## 4. Dimensionality Reduction — Putting It All Together

### From 2D to 1D

You have two features, so you get two eigenvalues $\lambda_1 > \lambda_2$ and two eigenvectors (PC1, PC2). To reduce to 1D, you project all points onto PC1 — the direction of maximum variance.

$$\text{2 features} \xrightarrow{\text{PCA}} \lambda_1 \text{ (PC1)}, \lambda_2 \text{ (PC2)} \xrightarrow{\text{keep top 1}} \text{1D representation}$$

### From 3D to 2D

$$\text{3 features} \xrightarrow{\text{PCA}} \lambda_1, \lambda_2, \lambda_3 \xrightarrow{\text{keep top 2}} \text{2D representation (PC1 + PC2)}$$

### General Rule

To reduce from $d$ dimensions to $k$ dimensions, keep the $k$ eigenvectors with the **largest** $k$ eigenvalues and discard the rest.

---

## 5. Variance Explained — How Much Information Do You Keep?

The **proportion of variance explained** by the $i$-th principal component is:

$$\text{Variance Explained by PC}_i = \frac{\lambda_i}{\sum_{j=1}^{d} \lambda_j}$$

The **cumulative variance explained** by the top $k$ components is:

$$\text{Cumulative Variance} = \frac{\sum_{i=1}^{k} \lambda_i}{\sum_{j=1}^{d} \lambda_j}$$

A common practice is to choose $k$ such that the cumulative variance $\geq 95\%$.

---

## 6. Limitations, Assumptions & Pitfalls

### Assumptions
- **Linearity:** PCA assumes that the principal components are linear combinations of the original features. It cannot capture non-linear structure in data.
- **Variance = Information:** PCA assumes directions of high variance are the most informative. This is not always true (e.g., in classification tasks where low-variance directions may be discriminative).
- **Gaussian distribution:** PCA works best when features are roughly normally distributed.

### Limitations
- **Interpretability loss:** After PCA, the new components are abstract combinations of original features — they lose direct physical meaning.
- **Sensitive to outliers:** Because variance is heavily influenced by outliers, PCA components can be skewed by anomalous data points.
- **Scale sensitivity:** If data is not standardized first, features with larger numerical ranges will dominate the principal components, producing misleading results.

### Common Pitfalls
- **Applying PCA before train/test split:** You must fit PCA only on the training data and then transform both train and test sets separately. Fitting on the full dataset causes **data leakage**.
- **Discarding too many components:** Always check the cumulative variance explained before deciding how many components to keep.
- **Confusing eigenvectors with eigenvalues:** The eigenvector gives the **direction** of the component; the eigenvalue gives its **magnitude** (importance).

---

## 7. FAANG-Level Q&A

**Q1. What if two eigenvalues are exactly equal? How does PCA behave?**

When $\lambda_i = \lambda_j$, the data has equal variance in those two directions, forming a **degenerate subspace**. Any orthogonal pair of vectors within that subspace is a valid solution, so the eigenvectors are not uniquely determined. In practice, numerical algorithms will still return *some* valid orthogonal pair, but small perturbations in data can cause completely different eigenvectors to be selected. This instability rarely causes issues for dimensionality reduction since the total variance captured is the same regardless of which basis is chosen within that subspace.

---

**Q2. What if the covariance matrix has a negative eigenvalue?**

A properly computed covariance matrix is always **positive semi-definite**, meaning all eigenvalues satisfy $\lambda \geq 0$. Negative eigenvalues in practice signal a numerical precision error (common in very high-dimensional, near-singular matrices) or a programming bug. The fix is typically to use a numerically stable algorithm such as **Singular Value Decomposition (SVD)**, which is what most production PCA implementations (e.g., `sklearn.decomposition.PCA`) use internally instead of explicit eigen decomposition.

---

**Q3. What if you apply PCA to a dataset where features are completely uncorrelated?**

If all features are uncorrelated, the covariance matrix is already **diagonal** — its off-diagonal entries are all zero. The eigenvectors are simply the original feature axes (standard basis vectors), and the eigenvalues are exactly the variances of each feature. PCA adds no rotational benefit here; it only reorders features by variance. This is a useful sanity check: if PCA returns the original axes, your features were already independent.

---

**Q4. System Design: How would you design a real-time anomaly detection pipeline for high-dimensional sensor data (1000+ features) at a large-scale IoT company, incorporating PCA?**

Fit a PCA model offline on a representative historical window of sensor data, retaining enough components to explain ~95% of variance. Deploy the frozen PCA transform (not retrained in real-time) in a streaming pipeline — tools like Apache Kafka + Flink can apply the projection to each incoming sensor reading with low latency. Anomaly detection works by computing the **reconstruction error**: project a new reading into the PCA subspace and then reconstruct it back; a high $\|x - \hat{x}\|^2$ indicates the reading lies outside the learned normal manifold and is flagged as an anomaly. Periodically (e.g., weekly), retrain the PCA model on fresh data to handle **concept drift** in sensor behavior, deploying the new model with a blue-green switch to avoid downtime. Store eigenvalues alongside the model to dynamically adjust the number of components if the variance structure of the data shifts significantly over time.