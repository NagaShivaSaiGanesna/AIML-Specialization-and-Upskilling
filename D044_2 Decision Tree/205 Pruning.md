# Pre-Pruning & Post-Pruning in Decision Trees

## 1. Why Pruning Exists — The Overfitting Problem

A Decision Tree left to grow without any constraints will keep splitting until **every single leaf node is pure** — meaning it perfectly classifies every training example. This sounds great, but it is actually the definition of **overfitting**.

Think of it like a student who memorises every answer in the textbook word for word. They score 100% on practice papers but fail in the actual exam because they never learnt to *generalise*.

| Scenario | Training Accuracy | Test Accuracy | Problem |
|---|---|---|---|
| Fully grown tree (default) | Very High (~100%) | Low | Overfitting |
| Pruned / controlled tree | Slightly Lower | Higher & Stable | Generalises well |

In bias-variance terms:
- A fully grown tree has **low bias** (fits training data perfectly) but **high variance** (wildly wrong on new data).
- Pruning deliberately introduces a small amount of bias to dramatically reduce variance.

---

## 2. The Gardener Analogy

A gardener prunes a plant not because the branches are wrong — but because **uncontrolled growth leads to a tangled mess** that looks chaotic and cannot survive long term. Cutting specific branches forces the plant into a healthier, more robust shape.

Pruning a Decision Tree works the same way: we cut branches where the additional splitting is doing more harm (overfitting noise) than good (learning signal).

---

## 3. Post-Pruning

### 3.1 What It Is

**Post-pruning** = build the complete tree first, *then* go back and remove branches that are not adding meaningful value.

### 3.2 How It Works — Step by Step

```
Step 1: Train the decision tree fully to its maximum depth
        (all leaves are pure or cannot be split further)

Step 2: Walk back up the tree from the leaves

Step 3: At each internal node, ask:
        "If I collapsed this entire sub-tree into a single leaf,
         would the accuracy on a validation set get worse?"

Step 4: If collapsing it does NOT significantly hurt accuracy → PRUNE it
        Replace the sub-tree with a single leaf predicting the majority class

Step 5: Repeat until no more pruning improves (or maintains) accuracy
```

### 3.3 Concrete Example

Suppose at a node we have **9 Yes and 2 No** remaining:

```
Before post-pruning:
         [9Y, 2N]
        /        \
   [9Y, 0N]    [0Y, 2N]
   (leaf=Yes)  (leaf=No)

After post-pruning:
         [9Y, 2N]
          leaf = Yes   ← majority class wins
```

The further split was technically correct but unnecessary — 9 out of 11 examples were already Yes. The marginal gain from splitting was tiny but the cost (added complexity, overfitting to those 2 No examples) was real. Post-pruning collapses it into a single majority-class leaf.

### 3.4 When to Use Post-Pruning

Post-pruning is most appropriate for **smaller datasets** because:
- You build the full tree first (expensive on large data)
- Then scan it top-down or bottom-up to prune
- The two-phase approach has higher time cost but gives you a complete picture before deciding what to cut

$$\text{Time Cost} = \underbrace{O(\text{Build full tree})}_{\text{Phase 1}} + \underbrace{O(\text{Prune passes})}_{\text{Phase 2}}$$

> **Rule of thumb:** If your dataset fits comfortably in memory and training takes seconds to minutes, post-pruning is safe. For millions of records, look at pre-pruning instead.

---

## 4. Pre-Pruning

### 4.1 What It Is

**Pre-pruning** = set constraints *before* building the tree so that it never grows beyond a controlled size in the first place. The tree stops splitting a node when a stopping condition is met — even if the node is still impure.

### 4.2 How It Works

Instead of building and then cutting, you install **guardrails** at construction time via hyperparameters. The tree simply stops growing when it hits any of these limits.

```
At each node during construction:
    → Check all stopping conditions
    → If ANY condition is met → make this node a leaf (majority class)
    → If no condition is met → continue splitting normally
```

### 4.3 Key Hyperparameters (sklearn `DecisionTreeClassifier`)

| Hyperparameter | What It Controls | Effect of Smaller Value |
|---|---|---|
| `max_depth` | Maximum levels the tree can grow | Tree stays shallow, more generalised |
| `min_samples_split` | Minimum examples a node must have to attempt a split | Prevents splitting on tiny groups |
| `min_samples_leaf` | Minimum examples that must exist in any leaf | Stops one-example leaf nodes |
| `max_features` | How many features to consider at each split | Adds randomness, reduces overfitting |
| `min_impurity_decrease` | A split only happens if it reduces impurity by at least this amount | Ignores trivially small gains |
| `criterion` | `gini` (default), `entropy`, or `log_loss` | Changes the impurity metric |
| `splitter` | `best` (evaluate all) or `random` (random subset) | `random` is faster, slightly less accurate |

### 4.4 When to Use Pre-Pruning

Pre-pruning is preferred for **large datasets** because:
- You never build the full tree → saves enormous computation time
- Hyperparameters are tuned using **GridSearchCV** or **RandomizedSearchCV**
- Each combination of parameters is evaluated via cross-validation

$$\text{Best params} = \underset{d,\, m_s,\, m_l}{\arg\max} \; \text{CV Accuracy}(d,\, m_s,\, m_l)$$

---

## 5. Post-Pruning vs Pre-Pruning — Full Comparison

| Property | Post-Pruning | Pre-Pruning |
|---|---|---|
| When it acts | After the tree is fully built | During tree construction |
| Approach | Build full → trim back | Set limits → stop early |
| Time cost | Higher (builds full tree first) | Lower (never builds full tree) |
| Best for | Smaller datasets | Large datasets |
| How tuned | Validation set accuracy | GridSearchCV / hyperparameter tuning |
| Risk | Can be slow on large data | May stop too early if params are too aggressive |
| Common method | Cost-Complexity Pruning (`ccp_alpha` in sklearn) | `max_depth`, `min_samples_leaf`, etc. |

---

## 6. Hyperparameter Tuning with GridSearchCV (Pre-Pruning in Practice)

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth':        [3, 5, 7, 10, None],
    'min_samples_split':[2, 5, 10, 20],
    'min_samples_leaf': [1, 2, 5, 10],
    'criterion':        ['gini', 'entropy']
}

dt = DecisionTreeClassifier(random_state=42)
grid = GridSearchCV(dt, param_grid, cv=5, scoring='accuracy')
grid.fit(X_train, y_train)

print(grid.best_params_)
```

GridSearchCV tries every combination of parameters, evaluates each on 5-fold cross-validation, and returns the combination that gives the best generalisation. This is the standard pre-pruning workflow.

---

## 7. Post-Pruning with `ccp_alpha` (Cost-Complexity Pruning)

sklearn implements post-pruning via the `ccp_alpha` parameter. Larger `ccp_alpha` → more pruning:

```python
# Step 1: Find the right alpha values
path = DecisionTreeClassifier().cost_complexity_pruning_path(X_train, y_train)
alphas = path.ccp_alphas

# Step 2: Build one tree per alpha and evaluate on validation set
train_scores, test_scores = [], []
for alpha in alphas:
    dt = DecisionTreeClassifier(ccp_alpha=alpha)
    dt.fit(X_train, y_train)
    train_scores.append(dt.score(X_train, y_train))
    test_scores.append(dt.score(X_test, y_test))

# Step 3: Pick the alpha where test accuracy peaks
```

---

## 8. Limitations, Assumptions & Pitfalls

| Pitfall | What Goes Wrong | Fix |
|---|---|---|
| Over-aggressive pre-pruning | `max_depth=2` on a complex dataset → underfitting (high bias) | Tune via cross-validation, don't guess |
| Not pruning at all | Default `max_depth=None` always overfits on training data | Always set at least one stopping criterion |
| Post-pruning on huge data | Building a full tree on millions of rows is prohibitively slow | Switch to pre-pruning or ensemble methods |
| Ignoring `min_samples_leaf` | Single-example leaves — the tree memorises noise | Set `min_samples_leaf ≥ 5` as a starting point |
| Pruning majority-class nodes incorrectly | If 9Y/2N, collapsing to Yes loses the 2N cases entirely | Acceptable trade-off — the goal is generalisation, not perfect training fit |

---

## 9. FAANG-Level Q&A

**Q1. What if you set `max_depth=1` — what does the tree become, and when is that actually useful?**

A tree of depth 1 produces exactly one split with two leaves — this is called a **decision stump**. It is the weakest possible Decision Tree, with very high bias, but it has a critical role: decision stumps are the base learners used inside **AdaBoost**, one of the most powerful ensemble algorithms. Each stump focuses on the single most informative feature at that iteration, and hundreds of stumps combined via weighted voting outperform a single deep tree. So `max_depth=1` is not a mistake — it is deliberately used when you intend to combine many weak learners into a strong ensemble.

---

**Q2. What if the dataset is perfectly balanced (50/50 classes) — does pruning behave differently?**

With a perfectly balanced dataset the root entropy is always exactly 1.0 and Gini is 0.5, so the tree has maximum initial impurity to work with. Paradoxically, balanced data makes overfitting *more* likely because there is no dominant majority class to collapse a node to — every near-pure branch feels meaningful and the tree grows deeper. Post-pruning becomes more aggressive in this scenario because collapsing a 6Y/4N node to "majority = Yes" is a rougher approximation than collapsing a 9Y/1N node. The fix is to be more conservative with `min_impurity_decrease` — only allow splits that reduce impurity by a meaningful threshold, not just by any nonzero amount.

---

**Q3. What if two different `max_depth` values give nearly identical cross-validation accuracy — which one should you pick?**

Always pick the **shallower tree** (lower `max_depth`). The principle here is **Occam's Razor** applied to ML: among models with equal performance, prefer the simpler one. A shallower tree is faster at inference, easier to interpret, and more stable under small data shifts — it generalises better even when CV scores look the same. In sklearn, if `max_depth=5` and `max_depth=8` give the same CV accuracy within one standard deviation, choose `max_depth=5`. This is also the reason `GridSearchCV` should be evaluated with `refit=True` and a scoring metric that penalises complexity (like `neg_log_loss` instead of raw accuracy).

---

**Q4. How would you design a pruning strategy for a fraud detection Decision Tree serving 200 million transactions per day with strict latency requirements?**

At this scale, pre-pruning is non-negotiable — post-pruning requires building a full tree first, which is computationally infeasible on hundreds of millions of daily transactions. The tree would be trained offline on a rolling 30-day window using distributed Spark jobs, with `max_depth` capped at 8–10 (empirically chosen via cross-validation) and `min_samples_leaf` set high enough (≥ 500 examples) to prevent the tree from fitting rare noise patterns. Inference is the easy part: a depth-10 tree requires at most 10 comparisons per transaction, making it sub-microsecond in a compiled ONNX runtime — well within any latency SLA. The harder engineering problem is **model drift**: a fraud tree trained on last month's patterns degrades quickly as fraudsters adapt, so the system needs weekly automated retraining with drift-detection alerts (PSI on feature distributions) to trigger emergency retrains. A single Decision Tree would likely be replaced by XGBoost in production for accuracy, but the pruning principles are identical — `max_depth`, `min_child_weight`, and `gamma` in XGBoost are all pre-pruning parameters serving the same role.