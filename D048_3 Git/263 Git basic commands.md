# Git Version Control: Fundamentals & Best Practices

## What is Git?

**Git** is a free, open-source **distributed version control system (DVCS)** that tracks changes in your source code over time. Unlike centralized systems, every developer has a complete copy of the repository — including its full history — on their local machine.

> Think of Git as a time machine for your code. Every commit is a snapshot you can return to at any point.

**Why Git matters in a team setting:**

In a real-world engineering team, you have frontend developers, backend developers, AI/ML engineers, and more — all writing code simultaneously. Git ensures:
- Changes don't overwrite each other
- Every modification is traceable to a person and time
- Broken code can be rolled back instantly

---

## Setting Up Git

### Step 1: Install Git

Download the Git CLI from the official site and install it for your OS (Windows, macOS, Linux/Unix). Verify the installation by running:

```bash
git version
```

If a version number appears, Git is installed correctly.

### Step 2: Configure Global Identity

Before making any commits, Git needs to know who you are. This identity is attached to every commit you make.

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

> **Critical:** The email must match the email address associated with your GitHub account. This is used for authentication when pushing code.

To verify your configuration:

```bash
git config --global user.name
git config --global user.email
```

---

## Core Git Concepts

### The Three Stages of a File in Git

Understanding these three stages is the foundation of everything in Git:

| Stage | Name | Description |
|---|---|---|
| 1 | **Working Directory** | Your local files — untracked or modified, not yet told to Git |
| 2 | **Staging Area (Index)** | Files marked to be included in the next commit — a "pre-commit checkpoint" |
| 3 | **Repository (Local/Remote)** | The committed snapshot, stored permanently in Git history |

Think of the **staging area** like a packing box. You decide *what* goes into the box before you seal and ship it (commit and push).

### The Hidden `.git` Folder

When you run `git init`, Git creates a hidden folder called `.git` in your project directory. This folder contains all of Git's internal data — commit history, configuration, object database. **Never delete it, and never commit it to GitHub.** It stays local.

---

## The Complete Git Workflow

### Initializing a Repository

```bash
git init
```

This turns any folder into a Git-tracked project by creating the `.git` directory.

### Checking File Status

```bash
git status
```

This command is your best friend. It tells you:
- Which files are **untracked** (Git doesn't know about them yet)
- Which files are **modified** (changed since last commit)
- Which files are **staged** (ready to be committed)

### Adding Files to the Staging Area

To track a specific file:
```bash
git add filename.md
```

To stage **all** changes at once (new files + modifications):
```bash
git add .
```

### Committing to the Staging Area

```bash
git commit -m "Your descriptive commit message"
```

This takes everything in the staging area and creates a permanent snapshot in your **local** repository. Nothing has gone to GitHub yet at this point.

### Renaming the Default Branch

GitHub's default branch is called `main`. Older Git versions default to `master`. To rename your local branch to match:

```bash
git branch -m main
```

Verify with:
```bash
git branch
```

### Connecting to a Remote Repository

Your local Git doesn't automatically know where on the internet to push your code. You must link it to a remote URL:

```bash
git remote add origin https://github.com/username/repository.git
```

Here, **`origin`** is simply an alias (a nickname) for that long URL. You could name it anything, but `origin` is the universal convention.

Verify the remote connection:
```bash
git remote -v
```

This shows the `fetch` and `push` URLs — both pointing to `origin`.

### Pushing Code to GitHub

```bash
git push origin main
```

This sends your committed snapshots from your local repository to GitHub under the `main` branch. Git may ask for authentication (username + password or token) the first time.

---

## Cloning an Existing Repository

If a repository already exists on GitHub and you want to work on it locally:

```bash
git clone https://github.com/username/repository.git
```

This downloads the entire repository — all files, all history, all branches — into a new folder on your machine. After cloning, the remote `origin` is automatically configured, so you can start committing and pushing immediately without `git remote add`.

---

## Undoing Changes: `git restore`

Made a mistake you haven't staged yet? Restore the file to its last committed state:

```bash
git restore filename.md
```

This discards all uncommitted edits to that file. **Use with caution — this action is irreversible.**

---

## Full Workflow Summary

```
Working Directory  →  git add  →  Staging Area  →  git commit  →  Local Repo  →  git push  →  Remote (GitHub)
```

| Command | Purpose |
|---|---|
| `git init` | Initialize a new local repository |
| `git config --global` | Set your identity for all repositories |
| `git status` | See the current state of your files |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Snapshot staged changes locally |
| `git branch -m main` | Rename branch |
| `git remote add origin <url>` | Link local repo to GitHub |
| `git remote -v` | Verify remote connections |
| `git push origin main` | Upload commits to GitHub |
| `git clone <url>` | Download a full remote repo locally |
| `git restore <file>` | Discard uncommitted local changes |

---

## Limitations, Assumptions & Pitfalls

**Limitations:**
- Git tracks **text-based changes** efficiently. Large binary files (videos, datasets) bloat the repository and are poorly handled — use Git LFS for those.
- Git does not automatically sync. You must manually `push` and `pull`.

**Common Assumptions Beginners Make:**
- `git commit` does **not** upload to GitHub. It only saves locally. You still need `git push`.
- The staging area is not optional — it exists between every `add` and `push` and gives you precise control over what gets committed.
- `git init` and `git clone` are mutually exclusive starting points. Don't run `git init` inside a cloned folder.

**Critical Pitfalls:**
- **Never commit secrets** (API keys, passwords) to a public repository. Even if you delete the file later, Git history retains it.
- Forgetting to set `user.email` to match your GitHub account can cause push authentication issues.
- Using `git add .` carelessly can stage files you didn't intend to commit (e.g., build artifacts, `.env` files). Always use a `.gitignore` file to exclude them.
- The `.git` folder should never be manually edited or deleted. Doing so corrupts your repository.

---

## FAANG-Level Q&A

**Q1. What if two developers clone the same repository, both modify the same file, and one pushes first — what happens when the second tries to push?**

Git will reject the second push with a "non-fast-forward" error because the remote has commits the second developer doesn't have locally. The second developer must first run `git pull origin main` to fetch and merge the latest changes. If both edits touch the same lines, Git will raise a **merge conflict** that must be resolved manually before the push can succeed. This is why frequent pulls and small, focused commits are a core best practice in team workflows.

**Q2. What if you accidentally commit a file containing an API key and push it to a public GitHub repository?**

The file must be removed and the secret must be **immediately rotated** (revoked and regenerated) on the service provider's platform — because Git history is permanent and the key is already exposed. Removing the file in a new commit does not erase it from history; tools like `git filter-repo` or GitHub's secret scanning alerts can help scrub the history, but this is complex and destructive. The only safe assumption after such a push to a public repo is that the secret is compromised.

**Q3. What if you run `git init` inside a folder that was already created by `git clone`?**

Running `git init` inside an already-cloned repository reinitializes the `.git` directory, which can corrupt metadata and confuse Git about the remote configuration. You may lose your `origin` remote link or create conflicting references. The correct practice is: if a repo came from `git clone`, it is already initialized — simply `cd` into it and start working.

**Q4. Design a Git branching and commit workflow for a 20-person engineering team shipping a web application with weekly releases.**

Use a **trunk-based development** model with short-lived feature branches. The `main` branch is always production-ready and protected — no direct pushes allowed. Each developer creates a branch named `feature/<ticket-id>-description`, commits small and frequently, and opens a **Pull Request (PR)** into `main` when done. Automated CI/CD pipelines run tests on every PR; only passing PRs can be merged via a required code review. A `release/<version>` branch is cut from `main` weekly for final QA, and hotfixes go through a `hotfix/<issue>` branch merged into both `main` and the active release branch. This keeps history clean, enables parallel development, and ensures `main` is always deployable.