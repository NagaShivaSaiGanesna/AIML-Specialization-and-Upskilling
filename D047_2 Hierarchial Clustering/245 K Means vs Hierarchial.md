# K-Means vs Hierarchical Clustering

## Overview

These two algorithms solve the same problem — grouping unlabelled data into clusters — but make fundamentally different trade-offs. Choosing the wrong one for your context leads to either unreadable results, wrong cluster counts, or outright failure on non-numerical data. The comparison below focuses on three dimensions that matter most in practice: **scalability**, **flexibility**, and **interpretability**.

---

## Head-to-Head Comparison

| Dimension | K-Means | Hierarchical |
|---|---|---|
| **Data size** | Large datasets ✓ | Small to medium datasets ✓ |
| **Data types** | Numerical only | Numerical + categorical + text + more |
| **Distance metric** | Euclidean / Manhattan | Euclidean, Manhattan, Cosine, or any valid similarity |
| **Centroids** | Required — one per cluster | Not used |
| **Cluster count** | Must specify $k$ upfront | Inferred from dendrogram |
| **Choosing $k$** | Elbow method (can be ambiguous) | Longest-gap rule on dendrogram (more visual) |
| **Complexity** | $O(n \cdot k \cdot t)$ — fast | $O(n^3)$ naive — slow at scale |
| **Output** | Flat partition | Nested tree (hierarchy) |
| **Interpretability** | Centroid positions | Full merge history visible |

---

## Deep Dive: Scalability

### Why K-Means wins on large data

K-Means runs in $O(n \cdot k \cdot t)$ time where $n$ is the number of points, $k$ is the number of clusters, and $t$ is the number of iterations. For a million points this is tractable.

Hierarchical clustering in its naive form requires computing and updating an $n \times n$ distance matrix:

$$\text{Space} = O(n^2), \quad \text{Time} = O(n^3)$$

Even more critically — a dendrogram with millions of leaves becomes visually unreadable. You cannot apply the longest-gap rule when every merge blurs into noise. So for **large datasets, K-Means is the clear winner by default**.

### Why Hierarchical wins on small data

For small datasets (typically $n < 10{,}000$), the dendrogram gives you something K-Means cannot: a **complete picture of every possible grouping at every level of granularity**, all at once. You do not need to rerun the algorithm to try different values of $k$.

---

## Deep Dive: Flexibility of Data Types

This is the most important practical distinction.

### K-Means: numerical data only

K-Means requires computing a **centroid** — the mean of all points in a cluster:

$$\mu_j = \frac{1}{|C_j|} \sum_{x_i \in C_j} x_i$$

This mean is only defined for numerical vectors. You cannot compute the "average" of two movie genres, two customer reviews, or two categorical labels. K-Means also relies exclusively on Euclidean or Manhattan distance, both of which require numerical coordinates.

### Hierarchical: works with any data where similarity is defined

Hierarchical clustering only needs one thing: a **pairwise similarity or distance measure** between any two data points. This makes it far more flexible:

| Data type | Suitable distance/similarity measure |
|---|---|
| Numerical vectors | Euclidean distance, Manhattan distance |
| Text documents | Cosine similarity |
| Categorical data | Hamming distance, Gower distance |
| Movie/item preferences | Cosine similarity, Jaccard similarity |
| Biological sequences | Edit distance (Levenshtein) |

#### Cosine Similarity — the key enabler

Cosine similarity measures the angle between two vectors in any dimensional space, making magnitude irrelevant. For two vectors $A$ and $B$:

$$\text{cosine similarity}(A, B) = \frac{A \cdot B}{\|A\| \cdot \|B\|} = \frac{\sum_{i} A_i B_i}{\sqrt{\sum_i A_i^2} \cdot \sqrt{\sum_i B_i^2}}$$

The similarity ranges from:

$$-1 \leq \text{cosine similarity} \leq 1$$

Where $1$ means identical direction (very similar), $0$ means orthogonal (unrelated), and $-1$ means opposite. This makes it ideal for comparing movies, documents, user preference vectors, and any sparse high-dimensional data — none of which K-Means can handle natively.

---

## Deep Dive: Choosing the Number of Clusters

### K-Means — the elbow method

You run K-Means repeatedly for $k = 1, 2, 3, \ldots$ and plot the **within-cluster sum of squares (WCSS)**:

$$\text{WCSS} = \sum_{j=1}^{k} \sum_{x_i \in C_j} \|x_i - \mu_j\|^2$$

You look for the "elbow" — the point where adding another cluster stops producing a significant drop in WCSS. In practice this elbow can be **ambiguous** — the curve sometimes bends gradually rather than sharply, leaving the optimal $k$ unclear.

### Hierarchical — the dendrogram longest-gap rule

As covered in the previous section:

> Find the longest vertical line through which no horizontal merge line passes. Cut there.

This is more visually decisive than the elbow method for small to medium datasets. You see all possible values of $k$ simultaneously and the natural separation between clusters is literally visible as the size of the gap.

---

## Limitations, Assumptions & Pitfalls

**Limitations of K-Means:**
- Cannot handle non-numerical data without first encoding it (which may distort relationships).
- The elbow method gives ambiguous guidance when cluster separations are gradual.
- Sensitive to initialisation — different random seeds can yield different final clusters.
- Assumes roughly spherical, equally-sized clusters due to the centroid mechanism.

**Limitations of Hierarchical:**
- Completely unscalable to large data — both the $O(n^3)$ compute and the unreadable dendrogram make it impractical beyond ~10K points.
- Merges are irreversible — a poor early merge cascades through the entire tree.
- Choice of **linkage method** (single, complete, average, Ward's) dramatically changes results and must be justified.

**Pitfalls:**
- Using K-Means on one-hot-encoded categorical data produces mathematically valid but semantically meaningless centroids.
- Assuming the elbow is always obvious — on real-world noisy data it often is not.
- Assuming cosine similarity is always appropriate for hierarchical clustering — it measures direction, not magnitude, so two items can appear "similar" even if one is vastly more prominent than the other.

---

## FAANG-Level Q&A

**Q1. What if your dataset is mixed — some features are numerical and some are categorical? Which algorithm do you use, and how?**

Pure K-Means fails on categorical features because computing a mean over categories is undefined. The standard approach is to use **Gower distance**, which computes a normalized distance per feature using the appropriate sub-metric (Manhattan for numerical, simple matching for categorical), then averages them:

$$D_{\text{Gower}}(i,j) = \frac{1}{p} \sum_{k=1}^{p} d_k(x_{ik}, x_{jk})$$

Hierarchical clustering handles this naturally since it only needs pairwise distances. Alternatively, K-Prototypes (a variant of K-Means designed for mixed data) can be used at scale. Never use K-Means on raw mixed data without transformation.

**Q2. What if cosine similarity gives unexpected cluster assignments — two items end up in the same cluster even though they seem different?**

Cosine similarity ignores magnitude and only measures **directional alignment** in feature space. Two items with completely different absolute values but proportionally similar feature distributions will have cosine similarity near $1$. The fix is to decide whether direction or magnitude matters for your problem — if magnitude matters (e.g., document length, total ratings count), switch to a distance metric that encodes it, such as Euclidean distance on $\ell_2$-normalised vectors combined with a magnitude penalty, or use BM25-weighted vectors for text. Additionally, extremely sparse vectors (e.g., a user who rated only one movie) produce unreliable cosine values that should be filtered or smoothed before clustering.

**Q3. What if neither the elbow method nor the dendrogram gives a clear answer for the optimal k?**

When both methods are ambiguous, use **external validation** rather than internal heuristics. If labelled ground truth exists for a sample, compute the Adjusted Rand Index (ARI) against it for different values of $k$. Without labels, use the **Silhouette Score**:

$$S(i) = \frac{b(i) - a(i)}{\max(a(i),\ b(i))}$$

where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance. The $k$ that maximises the average silhouette score is the most internally consistent. If scores remain flat across all $k$, this is a signal the data may not have meaningful cluster structure at all.

**Q4. System design: You are building a content recommendation engine at a music streaming platform with 200 million tracks. Each track has both audio features (numerical) and genre/mood tags (categorical). How do you cluster tracks for "similar songs" recommendations?**

At 200M tracks, hierarchical clustering is infeasible — use it only in an offline prototype phase to discover the natural $k$ on a 50K-track sample. For production, use **K-Prototypes** or encode the mixed data into a unified dense embedding space using a trained model (e.g., a contrastive audio encoder fine-tuned on user co-listen behaviour), then apply **Mini-Batch K-Means** at scale on the resulting numerical embeddings — reducing the problem to pure-numerical clustering. Cluster assignment runs nightly as a batch job on Spark, storing each track's cluster ID in a low-latency feature store. At serving time, "similar songs" retrieves tracks within the same cluster, then re-ranks by cosine similarity in the embedding space for precision. The offline hierarchical prototype run informs the initial $k$ used by K-Means and is re-run quarterly as the music catalogue evolves.