# Naïve Bayes Algorithm — Complete Study Guide

---

## 1. Prerequisites: Probability Essentials

Before understanding Naïve Bayes, you must understand two fundamental types of events and the concept of **conditional probability**.

### 1.1 Independent Events

Two events are **independent** if the outcome of one does not affect the probability of the other.

**Example — Rolling a Die:**

The sample space is $\{1, 2, 3, 4, 5, 6\}$.

$$P(\text{outcome} = k) = \frac{1}{6} \quad \text{for any } k \in \{1, 2, 3, 4, 5, 6\}$$

No matter how many times you roll, the probability of any outcome stays $\frac{1}{6}$. One roll does not influence the next.

---

### 1.2 Dependent Events

Two events are **dependent** if the outcome of the first event changes the probability of the second.

**Example — Bag of Marbles:**

Suppose a bag contains **3 orange** and **2 yellow** marbles. You draw one marble, do not replace it, and then draw again.

**Event 1:** Probability of drawing an orange marble first:

$$P(\text{orange}) = \frac{3}{5}$$

**Event 2:** After removing one orange marble, only 4 marbles remain (2 orange, 2 yellow). Now the probability of drawing a yellow marble:

$$P(\text{yellow} \mid \text{orange drawn first}) = \frac{2}{4} = \frac{1}{2}$$

Notice how the first event **changed** the sample space for the second event — this is the essence of dependency.

---

### 1.3 Conditional Probability

**Conditional probability** is the probability of event $B$ occurring *given* that event $A$ has already occurred.

$$P(B \mid A) = \frac{P(A \cap B)}{P(A)}$$

From the marble example, the combined probability of drawing orange *then* yellow is:

$$P(\text{orange} \cap \text{yellow}) = P(\text{orange}) \times P(\text{yellow} \mid \text{orange})$$

$$= \frac{3}{5} \times \frac{2}{4} = \frac{3}{5} \times \frac{1}{2} = \frac{3}{10}$$

**General rule for dependent events:**

$$\boxed{P(A \cap B) = P(A) \times P(B \mid A)}$$

This equation is the seed from which Bayes' Theorem is derived.

---

## 2. Bayes' Theorem — Derivation

Starting from the general rule above, observe that $P(A \cap B) = P(B \cap A)$. We can expand both sides:

$$P(A) \times P(B \mid A) = P(B) \times P(A \mid B)$$

Rearranging to isolate $P(A \mid B)$:

$$\boxed{P(A \mid B) = \frac{P(A) \times P(B \mid A)}{P(B)}}$$

This is **Bayes' Theorem**. Let's name each component:

| Term | Name | Meaning |
|------|------|---------|
| $P(A \mid B)$ | **Posterior** | Probability of $A$ *after* observing $B$ |
| $P(A)$ | **Prior** | Initial probability of $A$ before any observation |
| $P(B \mid A)$ | **Likelihood** | Probability of observing $B$ given $A$ is true |
| $P(B)$ | **Evidence** | Total probability of observing $B$ (normalising constant) |

---

## 3. From Bayes' Theorem to the Naïve Bayes Algorithm

### 3.1 The Machine Learning Setup

Consider a supervised classification dataset with:
- **Independent features:** $X_1, X_2, X_3$
- **Target (dependent) variable:** $y \in \{\text{Yes}, \text{No}\}$ (or any finite set of classes)

Our goal is to predict the class label $y$ for a new data point given its feature values.

Using Bayes' Theorem, we ask:

$$P(y \mid X_1, X_2, X_3) = \frac{P(y) \times P(X_1, X_2, X_3 \mid y)}{P(X_1, X_2, X_3)}$$

### 3.2 The Naïve Independence Assumption

The term $P(X_1, X_2, X_3 \mid y)$ is difficult to compute because it requires knowing the joint distribution of all features together. This is where the **"naïve"** assumption saves us:

> **Naïve Bayes assumes that all features are conditionally independent of each other given the class label.**

This means:

$$P(X_1, X_2, X_3 \mid y) = P(X_1 \mid y) \times P(X_2 \mid y) \times P(X_3 \mid y)$$

So the full formula becomes:

$$\boxed{P(y \mid X_1, X_2, X_3) \propto P(y) \times P(X_1 \mid y) \times P(X_2 \mid y) \times P(X_3 \mid y)}$$

The $\propto$ symbol ("proportional to") replaces the equality because we drop the denominator $P(X_1, X_2, X_3)$. Since the denominator is a constant across all classes, it does not affect which class has the highest probability — we only need to compare numerators.

### 3.3 The Decision Rule

For **binary classification** (Yes / No), we compute both:

$$\text{Score}(\text{Yes}) = P(\text{Yes}) \times \prod_{i} P(X_i \mid \text{Yes})$$

$$\text{Score}(\text{No}) = P(\text{No}) \times \prod_{i} P(X_i \mid \text{No})$$

The predicted class is whichever score is higher. To convert to proper probabilities that sum to 1:

$$P(\text{Yes} \mid \mathbf{X}) = \frac{\text{Score}(\text{Yes})}{\text{Score}(\text{Yes}) + \text{Score}(\text{No})}$$

---

## 4. Worked Example — Play Tennis Dataset

### 4.1 The Dataset

| Outlook  | Temperature | Humidity | Wind   | Play? |
|----------|-------------|----------|--------|-------|
| Sunny    | Hot         | High     | Weak   | No    |
| Sunny    | Hot         | High     | Strong | No    |
| Overcast | Hot         | High     | Weak   | Yes   |
| Rain     | Mild        | High     | Weak   | Yes   |
| Rain     | Cool        | Normal   | Weak   | Yes   |
| Rain     | Cool        | Normal   | Strong | No    |
| Overcast | Cool        | Normal   | Strong | Yes   |
| Sunny    | Mild        | High     | Weak   | No    |
| Sunny    | Cool        | Normal   | Weak   | Yes   |
| Rain     | Mild        | Normal   | Weak   | Yes   |
| Sunny    | Mild        | Normal   | Strong | Yes   |
| Overcast | Mild        | High     | Strong | Yes   |
| Overcast | Hot         | Normal   | Weak   | Yes   |
| Rain     | Mild        | High     | Strong | No    |

Total records: **14** → 9 "Yes", 5 "No"

---

### 4.2 Step 1 — Class Priors

$$P(\text{Yes}) = \frac{9}{14}, \quad P(\text{No}) = \frac{5}{14}$$

---

### 4.3 Step 2 — Feature Likelihoods

**Feature: Outlook**

| Outlook  | Count (Yes) | Count (No) | $P(\text{Outlook} \mid \text{Yes})$ | $P(\text{Outlook} \mid \text{No})$ |
|----------|-------------|------------|--------------------------------------|------------------------------------|
| Sunny    | 2           | 3          | $\frac{2}{9}$                        | $\frac{3}{5}$                      |
| Overcast | 4           | 0          | $\frac{4}{9}$                        | $\frac{0}{5}$                      |
| Rain     | 3           | 2          | $\frac{3}{9}$                        | $\frac{2}{5}$                      |

**Feature: Temperature**

| Temperature | Count (Yes) | Count (No) | $P(\text{Temp} \mid \text{Yes})$ | $P(\text{Temp} \mid \text{No})$ |
|-------------|-------------|------------|-----------------------------------|---------------------------------|
| Hot         | 2           | 2          | $\frac{2}{9}$                     | $\frac{2}{5}$                   |
| Mild        | 4           | 2          | $\frac{4}{9}$                     | $\frac{2}{5}$                   |
| Cool        | 3           | 1          | $\frac{3}{9}$                     | $\frac{1}{5}$                   |

---

### 4.4 Step 3 — Predict for a New Data Point

**Query:** Outlook = Sunny, Temperature = Hot → Predict Play?

**Score(Yes):**

$$\text{Score}(\text{Yes}) = P(\text{Yes}) \times P(\text{Sunny} \mid \text{Yes}) \times P(\text{Hot} \mid \text{Yes})$$

$$= \frac{9}{14} \times \frac{2}{9} \times \frac{2}{9} = \frac{9 \times 2 \times 2}{14 \times 9 \times 9} = \frac{36}{1134} = \frac{2}{63} \approx 0.0317$$

**Score(No):**

$$\text{Score}(\text{No}) = P(\text{No}) \times P(\text{Sunny} \mid \text{No}) \times P(\text{Hot} \mid \text{No})$$

$$= \frac{5}{14} \times \frac{3}{5} \times \frac{2}{5} = \frac{5 \times 3 \times 2}{14 \times 5 \times 5} = \frac{30}{350} = \frac{3}{35} \approx 0.0857$$

**Normalise to get proper probabilities:**

$$P(\text{Yes} \mid \text{Sunny, Hot}) = \frac{0.0317}{0.0317 + 0.0857} \approx 0.27 \quad (27\%)$$

$$P(\text{No} \mid \text{Sunny, Hot}) = \frac{0.0857}{0.0317 + 0.0857} \approx 0.73 \quad (73\%)$$

**Prediction:** $\boxed{\text{No}}$ — The person will **not** play tennis (73% probability).

---

## 5. Variants of Naïve Bayes

Different variants exist to handle different feature types:

| Variant | Feature Type | How Likelihood is Estimated |
|---|---|---|
| **Gaussian NB** | Continuous (e.g., height, weight) | Assumes $P(X_i \mid y)$ follows a Normal distribution; estimates mean $\mu$ and variance $\sigma^2$ per class |
| **Multinomial NB** | Discrete counts (e.g., word counts in text) | Counts occurrences; commonly used in document classification |
| **Bernoulli NB** | Binary features (e.g., word present/absent) | Models each feature as a Bernoulli trial |
| **Complement NB** | Imbalanced text data | Trains on the complement of each class to reduce bias |

---

## 6. Laplace (Additive) Smoothing

A critical practical issue: if a feature value never appears with a given class in the training data (e.g., 0 count), its likelihood is **zero**, which zeros out the entire product.

$$P(\text{Overcast} \mid \text{No}) = \frac{0}{5} = 0 \implies \text{Score}(\text{No}) = 0 \quad \text{(wrong!)}$$

**Laplace Smoothing** fixes this by adding a small pseudocount $\alpha$ (typically 1) to every count:

$$P(X_i = v \mid y) = \frac{\text{count}(X_i = v, y) + \alpha}{\text{count}(y) + \alpha \times |\mathcal{V}|}$$

where $|\mathcal{V}|$ is the number of unique values of feature $X_i$.

---

## 7. Limitations, Assumptions & Pitfalls

**1. The Independence Assumption is Rarely True**
Features in real data are often correlated. For example, "temperature" and "humidity" are related. Naïve Bayes ignores this, which is why it's called *naïve*. Surprisingly, the algorithm still performs well in practice even when this assumption is violated — but its probability estimates become unreliable.

**2. Zero-Frequency Problem**
As shown above, unseen feature-class combinations during training produce zero probabilities and kill the entire prediction. Always apply Laplace smoothing.

**3. Poor Probability Calibration**
Naïve Bayes produces biased probability estimates (often pushed toward 0 or 1) due to the independence assumption. Use it for classification decisions, not when you need well-calibrated probabilities.

**4. Feature Scaling Does Not Matter**
Unlike SVM or KNN, Naïve Bayes does not use distance metrics, so feature normalisation/standardisation has no effect.

**5. Cannot Capture Feature Interactions**
Because each feature is treated independently, complex relationships between features (e.g., $X_1 \times X_2$ patterns) are completely ignored.

**6. Continuous Features Require Distribution Assumptions**
For real-valued features, Gaussian NB assumes a Normal distribution, which may not hold. Violations degrade performance.

---

## 8. FAANG-Level Q&A

---

**Q1. What if two features are perfectly correlated — say, `temperature_celsius` and `temperature_fahrenheit` are both in the dataset? How does Naïve Bayes handle this?**

Naïve Bayes treats them as independent, so their likelihood terms are multiplied together as if they provide separate, non-overlapping evidence. This causes the algorithm to **double-count** the information from that feature, artificially inflating confidence in predictions and pushing probabilities toward 0 or 1 even further than usual. The fix is to detect and remove redundant features before training — use correlation analysis or PCA to pre-process the dataset. In practice, for text classification (where word co-occurrence is common), Complement Naïve Bayes partially mitigates this.

---

**Q2. What if all training examples for a class have the same value for a feature — say, every "No" example has `Wind = Strong`? What happens at prediction time when `Wind = Weak` appears in the test data?**

Without smoothing, $P(\text{Weak} \mid \text{No}) = \frac{0}{5} = 0$, which makes the entire $\text{Score}(\text{No}) = 0$ regardless of all other features. This is the **zero-frequency problem**, and it causes the classifier to become overconfident in the wrong class. Laplace smoothing resolves this: with $\alpha = 1$ and $|\mathcal{V}| = 2$ (Strong, Weak), the smoothed probability becomes $\frac{0 + 1}{5 + 2} = \frac{1}{7}$ instead of zero, preserving the influence of all features.

---

**Q3. What if the target variable has a severe class imbalance — say 99% "No" and 1% "Yes"? How does this affect Naïve Bayes?**

The **prior probability** $P(y)$ directly encodes this imbalance, so the algorithm will be heavily biased toward predicting "No." Even when the likelihoods strongly favour "Yes," the tiny prior $P(\text{Yes}) = 0.01$ can overwhelm them. Remedies include: (a) resampling — oversample the minority class or undersample the majority class before training; (b) using a threshold different from 0.5 to classify based on the posterior; or (c) setting a custom prior that reflects the desired operating point rather than the training distribution.

---

**Q4. How would you design a real-time spam detection system using Naïve Bayes that serves 100 million emails per day?**

The design would have three layers. First, an **offline training pipeline** runs nightly (or on a rolling window) using Spark/Hadoop to compute and store word-frequency tables per class; Laplace-smoothed log-probabilities are precomputed and written to a low-latency key-value store (e.g., Redis) since log-probabilities convert the product $\prod P(X_i \mid y)$ into a sum $\sum \log P(X_i \mid y)$, avoiding floating-point underflow. Second, a **stateless inference service** (deployed on Kubernetes behind a load balancer) tokenises the incoming email, looks up each token's log-likelihood in Redis, sums them with the log-prior, and returns the classification — this is a pure arithmetic operation that runs in microseconds per email. Third, a **feedback loop** captures user-reported false positives and false negatives to retrain the model periodically. At 100M emails/day (~1,200 per second), the bottleneck is typically the Redis read throughput; this is solved by replicating the store across multiple read replicas and caching the most frequent tokens locally per inference node.

---