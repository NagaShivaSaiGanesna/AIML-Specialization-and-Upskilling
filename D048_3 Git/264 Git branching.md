# Git Branching, Merging & Snapshot Management

## Quick Recap: The Git Staging Pipeline

Before diving into branching, it helps to have the full pipeline firmly in mind:

```
Working Directory  →  git add  →  Staging Area  →  git commit  →  Local Repo  →  git push  →  GitHub
```

A **commit snapshot** is Git's way of saying: "At this moment in time, the code looked exactly like this." Every commit is an immutable, addressable point in your project's history.

---

## Unstaging Files: `git restore` vs `git reset`

Sometimes you run `git add` and immediately realize you staged the wrong file. You have two equivalent ways to unstage it — both send the file back to the **working directory** without deleting it.

### Option 1: `git restore --staged`

```bash
git restore --staged filename.txt
```

This is the **modern, recommended** approach (Git 2.23+). It removes the file from the staging area while leaving your actual file contents untouched.

### Option 2: `git reset`

```bash
git reset filename.txt
```

This is the older, equivalent command. It also unstages the file without touching its contents. Both commands produce the same outcome for this use case.

| Command | Effect on Staging Area | Effect on File Contents |
|---|---|---|
| `git restore --staged <file>` | Removes file from staging | Unchanged |
| `git reset <file>` | Removes file from staging | Unchanged |
| `git restore <file>` *(no flag)* | No effect | **Discards all edits — irreversible** |

> **Key distinction:** `git restore --staged` undoes the `git add`. `git restore` (without `--staged`) undoes the actual file edits. Never confuse the two.

---

## Inspecting Changes: `git diff`

Before committing, you often want to see *exactly* what changed. Git provides two levels of diff inspection:

| Command | What it shows |
|---|---|
| `git diff` | Changes in the **working directory** that are **not yet staged** |
| `git diff --staged` | Changes that **are staged** and will be included in the next commit |

Think of it this way: `git diff` shows what you've written since your last `git add`, while `git diff --staged` shows what your next commit will actually contain. Running both before committing is a powerful habit that prevents accidental commits.

---

## Branching Strategy

### Why Branches Exist

In a team, multiple developers work on different features simultaneously. If everyone commits directly to `main`, the codebase becomes unstable and conflicts become catastrophic. Branches solve this by giving each developer an **isolated copy of the codebase** to work in freely.

> Think of `main` as the production-ready trunk of a tree. Every feature or bug fix is a branch that grows off that trunk, is developed independently, and is grafted back in only when it is ready.

### Creating a Branch

```bash
git branch developer
```

This creates a new branch called `developer` that starts as an **exact copy** of whatever branch you are currently on (typically `main`). No files are changed — Git simply creates a new pointer.

### Switching to a Branch

```bash
git checkout developer
```

Now all your commits go to `developer`, not `main`. Verify with:

```bash
git branch
```

The active branch is marked with an asterisk (`*`).

> **Modern shorthand:** `git switch developer` is the newer, cleaner equivalent of `git checkout developer` for simply switching branches.

### Working Inside a Branch

Once on `developer`, your workflow is identical to working on `main`:

```bash
git add .
git commit -m "Completed feature: user login form"
```

These commits are **isolated** — `main` is completely unaware of them until you explicitly merge.

---

## Merging Branches

When your feature work is complete and tested, you merge it back into `main`.

### Step 1: Switch back to `main`

```bash
git checkout main
```

You must be on the **receiving** branch — the one you want to merge *into*.

### Step 2: Merge the feature branch

```bash
git merge developer
```

Git takes all commits from `developer` that don't exist in `main` and replays them. If there are no conflicting changes, this is a **fast-forward merge** and completes automatically.

### Step 3: Push to GitHub

```bash
git push origin main
```

The merged result is now on GitHub.

### Branch Lifecycle Visualized

```
main:       A --- B --- C ----------------------------- G (merged)
                         \                             /
developer:                D --- E --- F (feature work)
```

Each letter represents a commit. The merge at `G` brings `D`, `E`, `F` into `main`.

---

## Viewing Commit History: `git log`

### Full History

```bash
git log
```

Displays every commit in reverse chronological order with the commit hash, author, date, and message. Press `Q` to exit.

### Viewing the Last N Commits with Diffs

```bash
git log -p -3
```

- `-p` shows the **patch** (the actual line-by-line diff) for each commit
- `-3` limits output to the last **3 commits**

This is extremely useful for code reviews and debugging — you can see not just *that* a change happened, but *what* changed.

| Command | Output |
|---|---|
| `git log` | All commits, metadata only |
| `git log -p` | All commits with full diffs |
| `git log -p -3` | Last 3 commits with full diffs |
| `git log --oneline` | Compact one-line-per-commit view |

---

## Complete Command Reference for This Module

| Command | Purpose |
|---|---|
| `git restore --staged <file>` | Unstage a file (modern syntax) |
| `git reset <file>` | Unstage a file (classic syntax) |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes pending commit |
| `git branch <name>` | Create a new branch |
| `git checkout <branch>` | Switch to a branch |
| `git merge <branch>` | Merge a branch into the current branch |
| `git log -p -<n>` | Show last *n* commits with diffs |

---

## Limitations, Assumptions & Pitfalls

**Limitations:**
- `git log -p` on a large repository with many commits can produce enormous output. Pipe it through `| less` or use `--oneline` for navigation.
- Local branches exist only on your machine until explicitly pushed with `git push origin <branch-name>`. Creating a branch locally does not create it on GitHub.

**Common Assumptions Beginners Make:**
- Merging is assumed to be automatic. It is — *only when there are no conflicts*. If two branches modify the same lines of the same file, Git pauses and demands a **manual conflict resolution** before the merge can complete.
- `git branch <name>` only *creates* a branch. It does not switch you to it. You must follow up with `git checkout <name>` (or use the shorthand `git checkout -b <name>` to create and switch in one step).

**Critical Pitfalls:**
- **Never merge directly on GitHub's `main` without a Pull Request in a team setting.** Local merges bypass code review and CI checks.
- Running `git push origin main` after a local merge pushes all merged content. If the merge included bad code, it is now in production history.
- Forgetting to `git checkout main` before merging means you may merge into the wrong branch entirely. Always verify with `git branch` before running `git merge`.
- Long-lived branches diverge significantly from `main` over time, making merges increasingly painful. Keep branches **short-lived** and merge frequently.

---

## FAANG-Level Q&A

**Q1. What if two developers create branches from `main`, both modify the same function in the same file, and both try to merge — what happens to the second merge?**

The first merge into `main` succeeds cleanly. When the second developer tries to merge, Git detects that the same lines were modified by both branches and raises a **merge conflict**. Git pauses the merge, marks the conflicting sections in the file with `<<<<<<<`, `=======`, and `>>>>>>>` markers, and requires a human to decide which version to keep. After manually resolving and saving the file, the developer runs `git add <file>` followed by `git commit` to complete the merge. This is why small, focused branches that touch distinct parts of the codebase are strongly preferred.

**Q2. What if you run `git merge developer` while still on the `developer` branch instead of `main`?**

Git will report that the branch is already up to date with itself and do nothing harmful — but nothing useful either. The merge operation requires you to be on the **destination** branch (the one receiving the changes). The correct sequence is always: switch to `main` first, then merge the feature branch into it. A helpful mental model is that `git merge X` means "bring X's changes into wherever I am right now."

**Q3. What if you need to see what changed between two specific branches before merging?**

You can use `git diff main..developer` to see all the line-by-line differences between the tip of `main` and the tip of `developer` without performing the merge. For a higher-level summary of which commits are in `developer` but not in `main`, use `git log main..developer --oneline`. Reviewing these outputs before merging is a best practice that helps catch accidental changes, debug regressions, and prepare cleaner Pull Request descriptions.

**Q4. Design a Git workflow for a fintech startup with 15 engineers shipping daily to production, where any broken commit to `main` triggers a regulatory compliance incident.**

Use a **GitHub Flow** variant with mandatory protection rules. The `main` branch is fully protected: direct pushes are disabled, and all changes must enter through a Pull Request. Each engineer creates a branch named `<ticket-id>/<short-description>`, e.g. `JIRA-412/add-kyc-validation`, and opens a PR when ready. The PR triggers an automated pipeline — unit tests, integration tests, static analysis, and a security scan — and requires at least two engineer approvals before merging. Merges use **squash-and-merge** to keep `main`'s history linear and readable, with each squashed commit message containing the ticket ID for audit traceability. Deployments are triggered automatically on every merge to `main` via CD pipelines, with automated rollback if error-rate thresholds are breached post-deploy — ensuring `main` is always both deployable and regulatorily auditable.