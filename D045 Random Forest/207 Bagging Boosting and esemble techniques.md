# Ensemble Techniques: Bagging & Boosting

## What Are Ensemble Techniques?

A single machine learning model — whether a decision tree, logistic regression, or SVM — is inherently limited. It may overfit, underfit, or be sensitive to noise in the training data. **Ensemble techniques** address this by **combining multiple models** to produce a single, stronger prediction.

The core intuition: a crowd of diverse experts makes fewer mistakes than any single expert alone.

Ensemble methods are a staple of competitive machine learning (e.g., Kaggle) because they consistently deliver state-of-the-art accuracy on both **classification** and **regression** tasks.

There are two fundamental ensemble strategies:

| Property | Bagging | Boosting |
|---|---|---|
| Full name | Bootstrap Aggregating | Adaptive Boosting / Gradient Boosting |
| Learner type | Base learners (strong) | Weak learners |
| Training order | **Parallel** | **Sequential** |
| Data sampling | Random subsets (with replacement) | Weighted / error-focused subsets |
| Goal | Reduce **variance** | Reduce **bias** |
| Final output | Majority vote / Average | Weighted vote / Average |
| Key algorithms | Random Forest | AdaBoost, Gradient Boost, XGBoost |

---

## Part 1: Bagging (Bootstrap Aggregating)

### The Core Idea

Given a training dataset $\mathcal{D}$ of $n$ samples, bagging creates $k$ different models by training each one on a **randomly sampled subset** (drawn **with replacement** — this is called a *bootstrap sample*) of $\mathcal{D}$.

Because each model sees a slightly different slice of the data, each becomes an expert on its own subset. Their errors tend to be **uncorrelated**, so averaging them out cancels the noise.

### How It Works — Step by Step

1. Start with the full training dataset $\mathcal{D}$.
2. Create $k$ bootstrap samples: $\mathcal{D}_1, \mathcal{D}_2, \ldots, \mathcal{D}_k$ (each by sampling $n$ points **with replacement** from $\mathcal{D}$).
3. Train a separate **base learner** $M_i$ on each $\mathcal{D}_i$ — **all in parallel**.
4. At prediction time, pass the test point through all $k$ models.
5. Combine predictions using:

**For classification (majority voting):**

$$\hat{y} = \underset{c}{\mathrm{argmax}} \sum_{i=1}^{k} \mathbf{1}[M_i(\mathbf{x}) = c]$$

The class predicted by the **most models** wins.

**For regression (averaging):**

$$\hat{y} = \frac{1}{k} \sum_{i=1}^{k} M_i(\mathbf{x})$$

### Key Properties of Bagging

- All base learners train **in parallel** — computationally efficient and easy to distribute.
- Base learners can be the **same algorithm** (e.g., all decision trees) or **different algorithms**.
- By default, many bagging implementations use **100 base learners** (e.g., Random Forest's `n_estimators=100`).
- Bagging primarily reduces **variance** — it works best when the base learner is a high-variance, low-bias model (like a fully grown decision tree).

### Primary Algorithm: Random Forest

**Random Forest** is the most prominent bagging algorithm. It builds an ensemble of decision trees, each trained on a bootstrap sample. It adds an extra layer of randomness: at each split in a tree, only a **random subset of features** is considered. This further decorrelates the trees and reduces variance even more.

---

## Part 2: Boosting

### The Core Idea

Boosting takes a completely different approach. Instead of training models independently in parallel, boosting trains models **sequentially**, where **each new model focuses on fixing the mistakes** of the previous one.

Each individual model is intentionally kept simple (a "**weak learner**" — typically a shallow decision tree). A weak learner only needs to be slightly better than random guessing. The magic of boosting is that chaining many such weak learners together in a smart way produces a powerful **strong learner**.

### How It Works — Step by Step

1. Train model $M_1$ on the full training dataset $\mathcal{D}$.
2. Identify the records $M_1$ **predicted incorrectly**.
3. Pass those misclassified records (along with additional data points) to $M_2$ — giving them higher priority so $M_2$ focuses on hard cases.
4. $M_2$ trains, makes its own errors, and passes those forward to $M_3$.
5. This chain continues for $n$ models: $M_1 \to M_2 \to M_3 \to \cdots \to M_n$.
6. Final prediction combines all models (weighted voting for classification, weighted average for regression):

$$\hat{y} = \sum_{i=1}^{n} \alpha_i \cdot M_i(\mathbf{x})$$

where $\alpha_i$ is the **weight** (confidence) assigned to model $M_i$ based on its accuracy.

### Intuition: The Specialist Team Analogy

Think of a complex exam covering Physics, Chemistry, and Geography.

- $M_1$ is great at Geography → answers geography questions well, struggles with the rest.
- $M_2$ specialises in Physics → picks up where $M_1$ failed.
- $M_3$ is a Chemistry expert → handles what both previous models missed.

Individually, each is a weak specialist. Combined sequentially, they cover every domain — forming a strong generalist.

### Key Properties of Boosting

- Models are trained **sequentially** — one cannot start until the previous one is complete.
- Each model is a **weak learner** (high bias, low variance) — usually a decision stump (depth-1 tree).
- Boosting primarily reduces **bias**.
- The final model is called a **strong learner**.

### Primary Boosting Algorithms

| Algorithm | Key Idea |
|---|---|
| **AdaBoost** | Re-weights misclassified samples so the next model focuses on them |
| **Gradient Boosting** | Each model fits the **residual errors** (gradients) of the previous model |
| **XGBoost** (Extreme Gradient Boost) | Highly optimised gradient boosting with regularisation, parallelism, and missing value handling |

---

## Bagging vs. Boosting: Deep Comparison

| Dimension | Bagging | Boosting |
|---|---|---|
| Problem solved | High variance (overfitting) | High bias (underfitting) |
| Training | Parallel | Sequential |
| Data used | Random bootstrap samples | Error-weighted samples |
| Learner strength | Strong base learners | Weak learners (e.g., stumps) |
| Sensitivity to noise | More robust | Can overfit noisy data |
| Interpretability | Low | Very low |
| Speed | Faster (parallelisable) | Slower (sequential dependency) |
| Typical use case | Noisy datasets, high variance models | Clean data, underfitting models |

---

## Limitations, Assumptions & Pitfalls

### Bagging
- **Pitfall**: Bagging does **not** reduce bias. If your base learner is already underfitting (high bias), bagging won't help.
- **Assumption**: Base learners must be sufficiently **diverse** (via different data subsets) for variance reduction to work.
- **Limitation**: Can be **memory-intensive** — storing $k$ separate models scales linearly.

### Boosting
- **Pitfall**: Boosting is **sensitive to noisy data and outliers**. Because it focuses on misclassified points, it can over-emphasise noisy samples and overfit.
- **Assumption**: Weak learners must be at least slightly better than random chance (accuracy $> 0.5$ for binary classification).
- **Limitation**: Sequential training makes boosting **slower** and harder to parallelise than bagging.
- **Pitfall**: More hyperparameters to tune (learning rate, number of estimators, tree depth) — requires careful cross-validation.

### General
- Both methods produce **black-box models** with limited interpretability compared to a single decision tree.
- Neither method eliminates the need for **good feature engineering** and **data preprocessing**.

---

## FAANG-Level Q&A

**Q1. What if all your base learners in a bagging ensemble are trained on nearly identical bootstrap samples due to a very small dataset?**

When the dataset is tiny, bootstrap samples drawn with replacement will heavily overlap, producing highly correlated models. Correlated errors do not cancel out when averaged, so the variance-reduction benefit of bagging essentially disappears. In this scenario, the ensemble will barely outperform a single model. The fix is to either collect more data, use aggressive feature subsampling (as Random Forest does), or switch to a cross-validation-based strategy like k-fold bagging.

---

**Q2. What if you apply boosting to a dataset with 20% mislabelled (noisy) training samples?**

Boosting will progressively assign higher weights to the mislabelled samples because they are consistently misclassified — they are *hard* examples by definition. The later models in the sequence will overfit these noise points. The final strong learner will have artificially inflated error on clean test data. Solutions include using **robust boosting variants** (e.g., BrownBoost, or XGBoost's built-in regularisation), cleaning the labels first, or switching to a more noise-tolerant method like bagging.

---

**Q3. What if the number of base learners in bagging is set to 1 — does it degenerate to a single model?**

Yes, exactly. With $k = 1$, bagging trains a single model on one bootstrap sample of the data — which is itself a random subset of the original training set. This is actually **worse** than a standard single model trained on the full data, because the single bootstrap sample omits roughly $1 - (1 - 1/n)^n \approx 36.8\%$ of unique training points. The key takeaway: the ensemble benefit only emerges as $k$ grows, with diminishing returns typically plateauing around $k = 100$–$500$ trees.

---

**Q4. You are building a real-time fraud detection system that must score 50 million transactions per day with sub-10ms latency. How would you deploy an XGBoost ensemble at this scale?**

Train XGBoost offline in batch and **serialise the final model** (e.g., using ONNX or the native XGBoost binary format) to avoid prediction overhead from Python runtime. Deploy the model behind a **horizontally scalable inference service** (e.g., Kubernetes with multiple pods), since XGBoost predictions are stateless and trivially parallelisable across requests — unlike training, prediction does not need to be sequential. Use **feature stores** (e.g., Feast, Redis) to pre-compute and cache expensive features so the online feature vector is assembled in $O(1)$ time. Monitor prediction latency with p99 SLOs and use model quantisation or tree pruning if the ensemble depth grows too large; at 50M transactions/day (~580 TPS), a well-tuned XGBoost model with 100–300 trees and depth 6 comfortably fits within 10ms on commodity hardware.