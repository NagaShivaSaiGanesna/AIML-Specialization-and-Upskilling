# Principal Component Analysis (PCA) & Dimensionality Reduction — Complete Study Guide

---

## 1. The Problem: Why Do We Need PCA?

Before understanding PCA itself, you must deeply understand the problem it solves — the **Curse of Dimensionality**.

---

## 2. Curse of Dimensionality

### 2.1 What is a "Dimension"?

In machine learning, **dimensionality** simply means the number of **features** in your dataset. A dataset with 500 columns lives in a 500-dimensional space. As features grow, so does the complexity of the mathematical space your model must navigate.

### 2.2 The Core Paradox — More Features ≠ Better Model

Intuitively, you might think: *"More information → better predictions."* This is true — but only up to a point. Beyond that point, adding more features actively **hurts** your model. This degradation is the Curse of Dimensionality.

Consider training six models on a house price dataset with 500 available features, each model receiving progressively more features:

| Model | Features Used | Accuracy Trend | Reason |
|---|---|---|---|
| M1 | 3 (most important) | $A_1$ — baseline | Core signal captured |
| M2 | 6 (all important) | $A_2 > A_1$ | More relevant signal added |
| M3 | 15 (still relevant) | $A_3 > A_2$ | Accuracy keeps improving |
| M4 | 50 (mixed relevance) | $A_4 < A_3$ ⬇ | Noise begins entering |
| M5 | 100 (many irrelevant) | $A_5 < A_4$ ⬇ | Overfitting intensifies |
| M6 | 500 (all features) | $A_6 \ll A_3$ ⬇⬇ | Model severely confused |

This behaviour follows an **inverted U-curve**:

$$\text{Model Accuracy} \propto f(\text{features}) \quad \text{rises, then falls}$$

### 2.3 Why Does Accuracy Fall? Two Root Causes

**Cause 1 — Overfitting**

A machine learning model is fundamentally a mathematical equation. When you feed it irrelevant or redundant features, the model attempts to learn patterns from noise. It fits the training data perfectly but generalises poorly to unseen data. This is **overfitting**.

Think of it this way: a student who memorises every irrelevant detail in a textbook performs worse on new exam questions than a student who understood the key concepts.

**Cause 2 — Computational & Mathematical Degradation**

As dimensions increase, the mathematical operations (matrix multiplications, distance calculations, gradient computations) scale in complexity. In high-dimensional spaces, a deeply counterintuitive phenomenon occurs — **all data points become approximately equidistant from each other**, making distance-based reasoning meaningless:

$$\lim_{d \to \infty} \frac{\text{dist}_{\max} - \text{dist}_{\min}}{\text{dist}_{\min}} \to 0$$

This means the model loses its ability to distinguish "near" from "far," and its decision boundaries become unreliable.

### 2.4 The Human Expert Analogy

Imagine asking a real estate expert: *"What is the price of this house?"*

- You say **location** → Expert gives a range: \$450K–\$500K ✅
- You add **3 BHK** → Range adjusts to \$500K–\$600K ✅
- You add **beachfront** → Price rises further ✅
- You add **near a celebrity's house** → Still manageable ✅
- You add **proximity to grocery shops** → Minor, creates slight confusion ⚠️
- You add **number of surrounding schools, traffic density, satellite visibility...** → Expert becomes completely confused ❌

The expert's **prediction accuracy degrades** because they're overloaded with inputs — many of which are correlated, redundant, or irrelevant. Your machine learning model experiences the exact same phenomenon.

---

## 3. Two Ways to Remove the Curse of Dimensionality

There are two fundamentally different strategies to tackle this problem:

| Strategy | Technique Name | What It Does | What Happens to Original Features |
|---|---|---|---|
| **Strategy 1** | Feature Selection | Identify and keep only the most important original features | Original features retained as-is; unimportant ones discarded |
| **Strategy 2** | Feature Extraction (PCA & others) | Derive new, compact features from the original set | Original features are **transformed** into new dimensions |

### 3.1 Feature Selection

You evaluate each feature's importance (using correlation, mutual information, tree-based importance scores, etc.) and simply **drop the least useful ones**. The surviving features are unchanged — they are still interpretable (e.g., "number of bedrooms" remains "number of bedrooms").

### 3.2 Feature Extraction — The PCA Approach

**Feature extraction** is conceptually more powerful. Instead of selecting or discarding original features, you **derive entirely new features** that are mathematical combinations of the originals — capturing the maximum possible information in fewer dimensions.

$$\{f_1, f_2, f_3, \ldots, f_n\} \xrightarrow{\text{PCA}} \{D_1, D_2\} \quad \text{where } 2 \ll n$$

The new derived features $D_1, D_2$ are called **principal components**. They are constructed so that:
- $D_1$ captures the **most variance** in the data.
- $D_2$ captures the **second most variance**, and is orthogonal (uncorrelated) to $D_1$.
- Each subsequent component captures less and less variance.

This means with just 2–3 principal components, you can often retain 90–95% of the information that was spread across hundreds of original features.

---

## 4. What is Principal Component Analysis (PCA)?

**PCA** is a dimensionality reduction algorithm that transforms a high-dimensional dataset into a lower-dimensional space by finding new axes (principal components) along which the **variance of the data is maximised**.

The key insight: **variance = information**. Directions in which your data varies the most are the directions that carry the most signal. PCA finds these directions mathematically and projects your data onto them.

The transformation can be expressed as:

$$\mathbf{D} = \mathbf{X} \cdot \mathbf{W}$$

where:
- $\mathbf{X} \in \mathbb{R}^{n \times p}$ is the original data matrix ($n$ samples, $p$ features)
- $\mathbf{W} \in \mathbb{R}^{p \times k}$ is the matrix of the top $k$ eigenvectors (principal components)
- $\mathbf{D} \in \mathbb{R}^{n \times k}$ is the transformed, lower-dimensional data

The high-level steps PCA performs internally:
1. **Standardise** the data (zero mean, unit variance)
2. Compute the **covariance matrix**: $\Sigma = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$
3. Compute **eigenvectors and eigenvalues** of $\Sigma$
4. Sort eigenvectors by **descending eigenvalue** (highest variance first)
5. Select the top $k$ eigenvectors as your principal components
6. **Project** original data onto these components

---

## 5. Feature Selection vs. Feature Extraction — Side-by-Side

| Property | Feature Selection | Feature Extraction (PCA) |
|---|---|---|
| Output features | Subset of original features | Brand new, derived features |
| Interpretability | High — features retain meaning | Low — components are abstract combinations |
| Information retained | Only from selected features | Compressed essence from **all** features |
| Handles multicollinearity | No | Yes — components are orthogonal by construction |
| Use when | Features are independently meaningful | Features are correlated and high-dimensional |

---

## 6. Limitations, Assumptions & Pitfalls

### Limitations
- **Loss of interpretability:** Principal components are linear combinations of original features. You can no longer say *"this axis means number of bedrooms"* — the axes become abstract. This is a serious problem in regulated industries (banking, healthcare) where model explanations are legally required.
- **Linear assumption:** Standard PCA only captures **linear** relationships. If your data has complex non-linear structure, PCA will miss it. Kernel PCA or autoencoders are needed instead.
- **Information loss is irreversible:** Reducing from 500 dimensions to 2 means some information is permanently discarded. The art is choosing $k$ such that the loss is acceptable.

### Assumptions
- **Features must be standardised:** PCA is variance-based. A feature with a large numerical scale (e.g., salary in dollars) will dominate all others if you don't standardise first. Always apply **z-score standardisation** before PCA.
- **Linear separability:** PCA assumes the most meaningful structure in data lies along linear directions of maximum variance.

### Pitfalls
- **Applying PCA before train/test split:** Fitting PCA on the full dataset (including test data) causes **data leakage**. Always fit PCA on training data only, then transform both train and test sets.
- **Choosing $k$ arbitrarily:** Use the **explained variance ratio** to choose $k$. A common rule is to retain components that together explain ≥ 95% of total variance: $\sum_{i=1}^{k} \lambda_i \Big/ \sum_{i=1}^{p} \lambda_i \geq 0.95$
- **Using PCA to fix bad data:** PCA does not remove noise — it compresses structure. Feeding it uncleaned data with outliers will cause misleading components, since outliers inflate variance along spurious directions.
- **Assuming PCA always helps:** If your features are already uncorrelated and all equally important, PCA provides no benefit and only costs you interpretability.

---

## 7. FAANG-Level Q&A

**Q1. What if your dataset has features on wildly different scales — say, income (\$20K–\$500K) and age (18–80) — and you apply PCA without standardisation?**

PCA finds directions of maximum variance, so income (with a range ~25× larger than age) will completely dominate the first principal component, making age essentially invisible. The resulting components will reflect the scale of the data rather than its true structure, producing meaningless dimensionality reduction. Always apply z-score standardisation before PCA so every feature contributes proportionally: $z = (x - \mu)/\sigma$. This is one of the most common and costly mistakes practitioners make with PCA in production pipelines.

---

**Q2. What if the relationship between your features and target is highly non-linear — for example, pixel intensities in facial recognition?**

Standard PCA, being a linear technique, can only find linear directions of maximum variance and will fail to capture curved manifolds or non-linear feature interactions. In such cases, **Kernel PCA** (using RBF or polynomial kernels) implicitly maps data into a higher-dimensional space where linear PCA is applied, capturing non-linear structure. For very high-dimensional non-linear data like images, **autoencoders** (deep learning-based) are generally superior, as they learn compressed non-linear representations end-to-end. The general principle: if residual variance after PCA is high and structure clearly exists, non-linear methods are warranted.

---

**Q3. What if after applying PCA you retain 2 principal components that explain 95% of variance, but your downstream model's accuracy drops significantly compared to using all features?**

The 5% discarded variance may contain class-discriminative information even though it represents low overall variance — variance and predictive power are not the same thing. This is a known failure mode of unsupervised PCA when applied to supervised problems. The solution is **supervised dimensionality reduction** — techniques like **Linear Discriminant Analysis (LDA)** maximise class separability rather than total variance, explicitly preserving the signal relevant to your labels. Alternatively, tune $k$ upward or use cross-validation to find the minimum $k$ that preserves downstream model performance.

---

**Q4. [System Design] Design a real-time fraud detection system for a payments company that receives 100,000 transactions per second, where each transaction has 800 raw features.**

Offline, train a PCA model on a representative historical sample of transactions, retaining components that explain 95% of variance (typically reducing 800 features to ~50–80 components); store the fitted PCA transformation matrix in a low-latency model registry. At inference time, incoming transactions stream through Kafka, are feature-engineered in a stream processor (e.g., Flink), and then the PCA transform is applied in-memory in under 2 ms before passing the compressed 50-dimensional vector to a fraud classifier (e.g., XGBoost or a small neural network). The system must enforce strict **train/test separation** — the PCA is never refit on live data to avoid leakage, but is retrained monthly on fresh batches in a controlled offline pipeline. Monitor **explained variance ratio** weekly via a drift-detection job; if new fraud patterns introduce feature distributions that reduce explained variance below a threshold (e.g., below 90%), trigger a PCA retraining alert and A/B test the updated model before promoting it to production.