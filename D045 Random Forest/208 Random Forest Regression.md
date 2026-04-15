# Random Forest: Classification & Regression

## 1. What Is Random Forest?

**Random Forest** is a powerful **ensemble learning** algorithm that belongs to the family of **bagging (Bootstrap Aggregating)** techniques. Instead of relying on a single model, it builds a large collection of **decision trees**, each trained on a slightly different slice of your data, and then combines their predictions to produce a final, more robust result.

The core intuition: *a crowd of imperfect experts, each seeing a slightly different view of the problem, collectively makes better decisions than a single expert seeing everything.*

---

## 2. Foundational Concepts

### 2.1 Ensemble Learning & Bagging

**Ensemble learning** is the practice of combining multiple models to improve predictive performance beyond what any single model can achieve.

**Bagging** (Bootstrap Aggregating) is one ensemble strategy:
- Train several **base learners** independently and in parallel.
- Each base learner is trained on a **bootstrap sample** (random subset, drawn with replacement) of the training data.
- Aggregate predictions at the end.

Random Forest is bagging where **every base learner is a decision tree**.

### 2.2 Why Decision Trees as Base Learners?

Decision trees are ideal base learners for bagging because:
- They are **high-variance, low-bias** models — they overfit easily on their own but respond well to variance reduction via aggregation.
- They are fast to train individually.
- They are **non-parametric** — no assumptions about data distribution.

---

## 3. How Random Forest Works — Step by Step

Let the dataset have:
- $d$ total samples (rows)
- $m$ total features (columns: $f_1, f_2, \ldots, f_m$)

And suppose we want to build $T$ decision trees.

### Step 1 — Row Sampling (Bootstrap Sampling)

For each tree $t \in \{1, 2, \ldots, T\}$, draw $d' < d$ rows **with replacement** from the full dataset. This gives each tree its own training subset $D_t$.

$$D_t \sim \text{Bootstrap}(D,\ d')$$

Because sampling is done **with replacement**, some rows will appear multiple times in $D_t$ and others not at all. On average, roughly 63.2% of unique rows appear in any given bootstrap sample.

### Step 2 — Feature Sampling (Random Subspace Method)

At **each node** of tree $t$, instead of considering all $m$ features for the best split, randomly select a subset of $k$ features where:

$$k \ll m$$

Typical defaults:
$$k_{\text{classification}} = \sqrt{m}, \qquad k_{\text{regression}} = \frac{m}{3}$$

This is the key innovation that differentiates Random Forest from plain bagged trees — it **decorrelates** the trees, ensuring they learn from genuinely different perspectives.

### Step 3 — Train Each Decision Tree

Each tree is grown to its **full depth** (no pruning) on its bootstrap sample using only the randomly selected features at each split. This makes each individual tree a high-variance, low-bias learner.

- For **classification trees**: splits are chosen using **Gini impurity** or **Information Gain (Entropy)**.
- For **regression trees**: splits are chosen to minimize **Mean Squared Error (MSE)**.

$$\text{Gini Impurity} = 1 - \sum_{c=1}^{C} p_c^2$$

$$\text{Entropy} = -\sum_{c=1}^{C} p_c \log_2(p_c)$$

$$\text{MSE at node} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \bar{y})^2$$

### Step 4 — Aggregate Predictions

Given a new test point $x^*$, pass it through all $T$ trees and collect their predictions $\hat{y}_1, \hat{y}_2, \ldots, \hat{y}_T$.

**For Classification — Majority Voting:**

$$\hat{y}_{\text{final}} = \underset{c}{\operatorname{argmax}} \sum_{t=1}^{T} \mathbf{1}[\hat{y}_t = c]$$

The class that gets the most votes across all trees wins.

**For Regression — Averaging:**

$$\hat{y}_{\text{final}} = \frac{1}{T} \sum_{t=1}^{T} \hat{y}_t$$

---

## 4. The Bias-Variance Trade-off: Why Random Forest Works

This is the most important concept to understand deeply.

| Model | Bias | Variance | Generalization |
|---|---|---|---|
| Single Decision Tree (unpruned) | Low | **High** | Poor (overfits) |
| Random Forest | Low | **Low** | Strong |
| Overly simple model | High | Low | Poor (underfits) |

A single unpruned decision tree has:
- **Low bias** — it fits the training data very tightly.
- **High variance** — small changes in training data cause large changes in the model.

This leads to **overfitting**: high training accuracy, low test accuracy.

Random Forest **preserves the low bias** (each tree still fits well) while **reducing variance** through aggregation. Mathematically, if $T$ uncorrelated trees each have variance $\sigma^2$, the ensemble variance is:

$$\text{Var}\left(\frac{1}{T}\sum_{t=1}^{T}\hat{y}_t\right) = \frac{\sigma^2}{T}$$

In practice the trees are not fully uncorrelated (feature sampling reduces, but doesn't eliminate correlation), so the actual variance reduction is:

$$\rho \sigma^2 + \frac{1-\rho}{T}\sigma^2$$

where $\rho$ is the average pairwise correlation between trees. Feature sampling drives $\rho$ toward zero, which is why it's essential.

---

## 5. Out-of-Bag (OOB) Error Estimation

Because each tree is trained on roughly 63.2% of the data, the remaining ~36.8% of samples — called **out-of-bag (OOB) samples** — can be used as a built-in validation set **without needing a separate hold-out set**.

For each sample $x_i$, only the trees that did **not** see $x_i$ during training make a prediction. The OOB error is the aggregated error across all such predictions:

$$\text{OOB Error} = \frac{1}{d} \sum_{i=1}^{d} \mathbf{1}[\hat{y}_i^{\text{OOB}} \neq y_i]$$

This is a nearly unbiased estimate of the generalization error.

---

## 6. Feature Importance

Random Forest naturally provides a measure of **feature importance** — how much each feature contributes to reducing impurity (or MSE) across all trees:

$$\text{Importance}(f_j) = \frac{1}{T} \sum_{t=1}^{T} \sum_{\text{nodes using } f_j} \Delta \text{Impurity}$$

Features that appear high in trees and produce large impurity reductions get higher importance scores.

---

## 7. Key Hyperparameters

| Hyperparameter | Description | Typical Default |
|---|---|---|
| `n_estimators` | Number of trees $T$ | 100–500 |
| `max_features` | Features per split $k$ | $\sqrt{m}$ (clf), $m/3$ (reg) |
| `max_depth` | Max depth of each tree | None (full depth) |
| `min_samples_split` | Min samples to split a node | 2 |
| `min_samples_leaf` | Min samples at a leaf node | 1 |
| `bootstrap` | Whether to use bootstrap sampling | True |

---

## 8. Limitations, Assumptions & Pitfalls

### Limitations

- **High training time**: Training $T$ deep trees is expensive. Time complexity is roughly $O(T \cdot d \cdot m \cdot \log d)$ where $d$ = samples and $m$ = features.
- **Memory intensive**: Storing hundreds of full-depth trees requires significant RAM.
- **Black box**: Compared to a single decision tree, a forest is much harder to interpret.
- **Not great for very high-dimensional sparse data**: e.g., raw text with bag-of-words features. Gradient boosting often outperforms here.
- **Slow at inference**: Prediction requires passing input through all $T$ trees.

### Assumptions

- The dataset is large enough that bootstrap samples are meaningful.
- Features are at least somewhat informative — random forests cannot manufacture signal from pure noise.
- Trees are assumed to be diverse; if all trees are nearly identical (high $\rho$), variance reduction is minimal.

### Common Pitfalls

- **Too few trees**: With very small $T$ (e.g., $T < 10$), the forest is unstable and noisy. Always validate with OOB error as $T$ grows.
- **Ignoring class imbalance**: In classification, majority classes dominate voting. Use `class_weight='balanced'` or oversampling.
- **Feature importance bias**: Features with many unique values (high cardinality) tend to get inflated importance scores. Use permutation importance for more reliable estimates.
- **Assuming more trees always help**: After a point (usually 200–500 trees), additional trees yield diminishing returns and only increase cost.
- **Not tuning `max_features`**: The default is a good starting point but can often be improved with cross-validation.

---

## 9. Random Forest vs. Decision Tree — Summary

| Criterion | Decision Tree | Random Forest |
|---|---|---|
| Bias | Low | Low |
| Variance | High | Low |
| Overfitting tendency | High (without pruning) | Low |
| Interpretability | High | Low |
| Training speed | Fast | Slower |
| Prediction speed | Fast | Slower |
| Handles noisy features | Poorly | Well (feature sampling helps) |
| Built-in validation | No | Yes (OOB error) |

---

## 10. FAANG-Level Q&A

**Q1. What if all features are highly correlated with each other? Does Random Forest still reduce variance effectively?**

When features are highly correlated, random subsets of features at each node tend to produce similar splits regardless of which features are chosen. This means the resulting trees remain highly correlated ($\rho \approx 1$), and the variance reduction formula $\rho\sigma^2 + \frac{1-\rho}{T}\sigma^2$ approaches $\sigma^2$ — giving little improvement over a single tree. In such cases, consider dimensionality reduction (PCA) before training, or switch to Gradient Boosting which handles correlated features more gracefully by focusing on residuals.

---

**Q2. What if the dataset is severely class-imbalanced (e.g., 99% negative, 1% positive)? How does majority voting fail, and how do you fix it?**

Majority voting naturally favors the dominant class — trees trained on bootstrap samples will mostly see the majority class, so the minority class gets overwhelmed at the voting stage. This causes the model to achieve high accuracy by simply predicting the majority class for almost every test point. Fix this using `class_weight='balanced'` (which re-weights the impurity criterion), stratified bootstrap sampling, or by using predicted class probabilities with a tuned threshold instead of raw majority vote.

---

**Q3. What if you add a large batch of new training data after the model is already trained? Can you update incrementally?**

Standard Random Forest is not an online or incremental learner — you cannot efficiently update individual trees with new data. However, the ensemble structure provides a practical workaround: train a new sub-forest on the new data batch and merge it with the existing forest (add its trees to the pool). This avoids full retraining. The impact on any single tree is small because new records are distributed across many trees via sampling — no individual tree's behavior changes dramatically, keeping the ensemble stable.

---

**Q4. System Design: You need to serve a Random Forest model trained on 500 million records with 500 trees to 10 million users per day with sub-100ms latency. How do you architect this?**

Train the forest offline using distributed frameworks (Spark MLlib or Dask) partitioned across a cluster, then serialize each tree as a compact binary format (e.g., ONNX or a custom byte-packed structure) to minimize memory footprint. Deploy the model as a stateless microservice behind a load balancer, where each node holds the full forest in RAM (a 500-tree forest of shallow depth typically fits in 1–4 GB). For inference, trees can be evaluated in parallel using thread pools, reducing per-request latency well below 100ms. Cache repeated or near-duplicate predictions using a feature-hash-keyed Redis layer to further reduce compute load at peak traffic. Horizontal scaling of inference nodes handles traffic spikes with no model changes required.