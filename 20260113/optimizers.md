Here are your detailed notes in Markdown format. This guide breaks down the mathematics and intuition behind each optimizer, focusing on *why* the equations are structured the way they are.

---

# Deep Learning Optimizers: In-Depth Notes

This document details the evolution of optimization algorithms from standard SGD to the state-of-the-art Adam optimizer.

## 1. Prerequisite: Exponential Weighted Moving Average (EWMA)

To understand Momentum, RMSprop, and Adam, you must understand **EWMA**. It is a method to smooth out noisy data (like a fluctuating stock price or a noisy gradient).

**The Formula:**


* ****: The current "smoothed" value (moving average).
* ****: The actual new data point (current observation).
* ** (Beta)**: The weight (hyperparameter), usually  or . It represents how much we trust the *past* history.
* If , we approximate the average over the last  days.
* If , we approximate the average over the last  days.



**Intuition:** It prevents the value from fluctuating wildly by relying heavily on the accumulated history () and only slightly on the new, potentially noisy data ().

---

## 2. SGD with Momentum

**The Problem with Vanilla SGD:**
In Stochastic Gradient Descent, we calculate the gradient using a small batch of data. This introduces "noise."

* **Vertical Oscillation:** The gradient might point steeply down one side of a valley and steeply up the other in a zigzag pattern, wasting time moving up and down rather than forward.
* **Horizontal Slowness:** The actual movement toward the global minimum (horizontal direction) is slow because the zigzagging cancels out forward progress.

**The Solution (Momentum):**
We apply EWMA to the **gradients**. Instead of updating weights using the current gradient (), we update using a "velocity" term () which is the moving average of past gradients.

**The Equations:**

1. **Calculate Velocity ():**



*(Note:  is the gradient at time .  is typically 0.9).*
2. **Update Weights ():**



*(Where  is the Learning Rate)*.

**Why this works:**

* **Vertical Direction:** The zigzags (positive and negative gradients) cancel each other out in the moving average, reducing oscillation.
* **Horizontal Direction:** The gradients point consistently toward the minimum, so the moving average accumulates speed (momentum), allowing the optimizer to accelerate in the correct direction.

---

## 3. Adagrad (Adaptive Gradient)

**The Problem with Constant Learning Rate:**
In SGD and Momentum, the Learning Rate () is fixed for all weights.

* However, in sparse datasets (e.g., text data), some features appear rarely (sparse) while others appear frequently (dense).
* **Frequent features** need a *small* learning rate (to avoid overshooting).
* **Rare features** need a *large* learning rate (to learn effectively when they essentially appear).

**The Solution:**
Adagrad adapts the learning rate **individually for every parameter** based on how much that parameter has been updated in the past.

**The Equations:**

1. **Accumulate Squared Gradients ():**



*We keep a running sum of the squared gradients for every weight.*
2. **Update Weights:**


* ** (Epsilon):** A tiny number (e.g., ) to prevent division by zero.
* ****: This is the adaptive term.



**Mechanism:**

* If a weight has frequent, high gradients,  becomes large  The effective learning rate () becomes **small**.
* If a weight is rarely updated,  stays small  The effective learning rate remains **high**.

**The Critical Flaw (Vanishing Learning Rate):**
Since we square the gradients,  is always positive and **monotonically increasing**.



Eventually, the denominator becomes so huge that the effective learning rate becomes effectively **zero**. The model stops learning completely.

---

## 4. RMSprop (Root Mean Square Propagation)

**The Problem:** Fixing Adagrad's aggressive learning rate decay.

**The Solution:**
Instead of accumulating the *sum* of all past squared gradients (which grows to infinity), RMSprop uses the **EWMA of squared gradients**. This restricts the accumulation to a "window" of recent updates.

**The Equations:**

1. **Calculate Moving Average of Squared Gradients ():**


* This is the same EWMA formula, but applied to the square of the gradient.
* This keeps the denominator from growing infinitely.


2. **Update Weights:**



**Result:**
The learning rate is still adaptive (handling sparse/dense features differently), but it no longer vanishes to zero, allowing the model to continue learning indefinitely.

---

## 5. Adam (Adaptive Moment Estimation)

**The Concept:**
Adam is the "Ultimate" optimizer because it combines the best of both worlds:

1. **Momentum:** Uses the average of gradients (First Moment).
2. **RMSprop:** Uses the average of squared gradients (Second Moment).

**The Algorithm (Step-by-Step):**

**Step 1: Calculate First Moment () [Like Momentum]**


*  is typically .
* This tracks the "mean" of the gradient (Momentum).

**Step 2: Calculate Second Moment () [Like RMSprop]**


*  is typically .
* This tracks the "uncentered variance" of the gradient.

**Step 3: Bias Correction**
*Why do we need this?*
 and  are initialized as vectors of 0s. At the very start of training (), the values will be very close to 0 (biased towards zero). We need to boost them up initially so the model starts learning immediately.

* As  increases (iterations increase),  approaches 0, and the bias correction term disappears (effectively dividing by 1), leaving the original  and .

**Step 4: Update Parameters**


### **Summary Table**

| Optimizer | Key Idea | Formula Helper |
| --- | --- | --- |
| **SGD** | Update using current batch gradient. |  |
| **Momentum** | Smooth the path using velocity. |  |
| **Adagrad** | Adapt learning rate (sq. gradients). |  |
| **RMSprop** | Fix Adagrad (windowed sq. gradients). |  |
| **Adam** | Combine Momentum + RMSprop + Bias Correction. | Uses  (Momentum) and  (RMSprop) |

---

### **Would you like me to:**

1. Generate a Python code snippet using PyTorch/TensorFlow to show how to implement these (and where the hyperparameters  go)?
2. Explain "Saddle Points" and why Adam escapes them better than SGD?