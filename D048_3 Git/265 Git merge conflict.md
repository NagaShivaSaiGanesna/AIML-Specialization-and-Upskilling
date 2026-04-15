# Git Merge Conflicts: Understanding, Simulating & Resolving

## Why Merge Conflicts Exist

In any real engineering team, multiple developers work on the same codebase simultaneously. Git is intelligent enough to automatically merge changes that touch *different* files or *different lines* of the same file. However, when two developers modify the **exact same lines** of the same file in separate branches and both try to merge into `main`, Git has no way of deciding whose version is correct — so it stops and asks you to decide. This is a **merge conflict**.

> Think of a merge conflict as two people trying to write different sentences on the same line of a shared document. Git hands the pen back to you and says: "You sort this out."

---

## The Anatomy of a Conflict: Two-Developer Scenario

Here is the canonical real-world setup that produces a conflict:

```
main (shared codebase):     A ──────────────────────── E (conflict!)
                             \           \             /
developer-A branch:          B ── C ─────────────────   (pushed to main first)
                              \
developer-B branch:            D ──────────────────────  (tries to push second → REJECTED)
```

| Step | Developer A | Developer B |
|---|---|---|
| 1 | Clones main repository | Clones main repository (same state) |
| 2 | Creates branch `developer-A` | Creates branch `developer-B` |
| 3 | Edits `README.md`, commits | Edits **same** `README.md`, commits |
| 4 | Merges to local `main`, pushes to GitHub | Merges to local `main`, tries to push |
| 5 | ✅ Success | ❌ **REJECTED** — remote has newer commits |

---

## Step-by-Step: Simulating the Conflict

### Setup: Clone the Repository (Both Developers)

Each developer clones the same GitHub repository into their own local folder. This simulates two separate machines:

```bash
# Developer A's terminal
git clone https://github.com/username/application.git

# Developer B's terminal (separate folder)
git clone https://github.com/username/application.git
```

### Developer A: Create Branch, Make Changes, Push

```bash
git branch developer-A
git checkout developer-A

# (edit README.md — add "Adding Developer A story")

git add .
git commit -m "Developer A story changes"
git checkout main
git merge developer-A
git push origin main
```

Developer A's push succeeds because `main` on GitHub had no newer commits. GitHub now contains Developer A's changes.

### Developer B: Create Branch, Make Changes, Try to Push

```bash
git branch developer-B
git checkout developer-B

# (edit same README.md — add "Developer B update")

git add .
git commit -m "Developer B commit"
git checkout main
git merge developer-B
git push origin main
```

**This push is rejected.** Git returns an error similar to:

```
! [rejected]  main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. Integrate the remote changes before pushing again.
```

This is not an error to fear — it is Git doing exactly its job.

---

## Resolving the Conflict

### Step 1: Pull the Remote Changes

```bash
git pull origin main
```

This fetches Developer A's already-merged commits and attempts to merge them with Developer B's local commits. Since both modified the same lines, the auto-merge fails and Git marks the conflict directly inside the file:

```
<<<<<<< HEAD
Developer B update
Application
=======
Adding Developer A story
Application
>>>>>>> origin/main
```

**Reading the conflict markers:**

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Start of **your** local changes (Developer B) |
| `=======` | Divider between the two conflicting versions |
| `>>>>>>> origin/main` | Start of the **remote** changes (Developer A) |

### Step 2: Manually Resolve the Conflict

Open the file in any editor. Delete the conflict markers and craft the final, correct version. In most cases on a real project, you would include **both** contributions after discussing with your teammate:

```
Adding Developer A story
Developer B update
Application
```

> **Critical warning:** In production code, never blindly keep or discard changes. Read both versions carefully. A function refactored by Developer A and extended by Developer B may require both parts to coexist correctly. Carelessly overriding a colleague's code is one of the most common and damaging mistakes a developer can make on a team.

### Step 3: Stage, Commit, and Push the Resolved File

```bash
git add .
git commit -m "Resolved merge conflict: combined Developer A and B changes"
git push origin main
```

The push now succeeds. GitHub's commit history reflects both developers' contributions.

---

## Full Conflict Resolution Workflow

```
git pull origin main          ← fetch remote + attempt merge
# (conflict detected in file)
# open file, resolve markers manually
git add .                     ← mark conflict as resolved
git commit -m "Resolved conflict"
git push origin main          ← now succeeds
```

---

## Limitations, Assumptions & Pitfalls

**Limitations:**
- Git can only resolve conflicts in **text-based files**. Binary files (images, compiled artifacts) that conflict must be resolved by choosing one version entirely — Git cannot diff them line by line.
- `git pull` is shorthand for `git fetch` + `git merge`. In team workflows, `git pull --rebase` is often preferred as it produces a cleaner, linear history, but introduces its own complexities.

**Common Assumptions Beginners Make:**
- Developers assume that working in separate branches prevents conflicts. Branches delay conflicts — they do not eliminate them. Conflicts appear at merge time, not commit time.
- Developers assume that `git merge developer-B` on their local machine is sufficient before pushing. If the remote `main` received commits after your last `git pull`, the push will still be rejected.

**Critical Pitfalls:**
- **Accepting all incoming or outgoing changes blindly** using editor shortcuts (e.g., "Accept All Incoming") is dangerous — it silently discards your teammate's work.
- **Forgetting `git add .` after resolving a conflict** leaves Git in a broken mid-merge state. Always stage the resolved file before committing.
- **Long-lived feature branches** are the primary cause of large, complex conflicts. The longer a branch lives without syncing to `main`, the more painful its eventual merge becomes. Pull from `main` into your feature branch frequently using `git merge main` or `git rebase main`.
- Never resolve a conflict by overriding a colleague's changes without communicating. In a production codebase, this can silently break features that were already tested and approved.

---

## FAANG-Level Q&A

**Q1. What if three developers all modify the same file in three separate branches, and all three try to merge into `main` at the same time — how does Git handle this?**

Git processes merges sequentially, not in parallel. The first push succeeds cleanly. The second developer encounters a conflict with the first, resolves it, and pushes. The third developer must now `git pull` a `main` that already contains *both* previous developers' changes, potentially facing a more complex three-way conflict in the same file. This is precisely why teams use Pull Requests with sequential review queues — only one PR merges at a time, and CI re-runs on each merge to catch cascading integration issues.

**Q2. What if you start resolving a conflict and realize mid-way that you've made it worse — can you abort and start over?**

Yes. If you have not yet run `git commit` after the conflicted `git merge` or `git pull`, you can completely abort the in-progress merge with `git merge --abort`. This resets your working directory to the exact state it was in before you ran `git pull`, discarding all conflict marker edits. You can then re-pull, take a cleaner approach, or coordinate with your teammate before trying again.

**Q3. What if the same line was deleted by Developer A but modified by Developer B — what does the conflict look like?**

Git still surfaces this as a conflict: Developer B's modification appears under `HEAD`, while Developer A's deletion means that section is simply absent in the `origin/main` side. The developer resolving the conflict must decide whether the line should exist at all and in what form — there is no automatic answer. This class of conflict (modify vs. delete) is particularly subtle and dangerous because the intent behind the deletion may not be obvious from the diff alone, making communication between developers essential.

**Q4. Design a Git workflow for a 50-person engineering organization where merge conflicts must be minimized, all changes are auditable for compliance, and no broken code can ever reach the `main` branch.**

Adopt a **protected trunk with enforced PR gates**. The `main` branch requires: a passing CI pipeline (unit, integration, and security tests), a minimum of two peer-reviewed approvals, and linear history enforced via **squash merges** — this keeps `main` readable and bisectable. Each engineer syncs their feature branch daily via `git rebase main` rather than `git merge main`, which keeps branches current and minimizes divergence. To minimize same-file conflicts structurally, enforce **vertical slice ownership** — each team owns distinct modules or services, and cross-team file edits go through a designated reviewer. For compliance, every squash commit message must reference a ticket ID, and branch protection rules log all merges with timestamps and approver identities in GitHub's audit log. A mandatory `CODEOWNERS` file ensures that changes to sensitive files (auth, payments, PII handlers) require approval from the designated security or compliance owner before any merge can proceed.