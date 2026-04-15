# End-to-End Machine Learning Project Setup: A Complete Study Guide

## Introduction & Why This Matters

Before writing a single line of model code, a professional data scientist establishes a solid project foundation. This is what separates someone who "knows ML" from someone who *works in ML*. In the industry, machine learning projects are collaborative, version-controlled, and packaged — not just a collection of notebooks on a local machine.

This guide walks you through the complete project setup phase: version control with GitHub, Python environment management, project packaging with `setup.py`, and dependency management with `requirements.txt`.

---

## Section 1: Version Control with GitHub

### Why GitHub First?

When working on any real ML project, your code lives in a **Git repository**. This enables:

- **Collaboration** — multiple engineers commit and merge code simultaneously
- **Version history** — every change is tracked and reversible
- **Deployment pipelines** — CI/CD tools trigger on commits
- **Portfolio** — interviewers look at your GitHub before your resume

> **Interview Insight:** Candidates who can walk through a real, committed GitHub project always outperform those who only talk about theory.

### Setting Up a New Repository (Step-by-Step)

**Step 1 — Create the repository on GitHub**

Go to [github.com](https://github.com), click *New Repository*, name it `ml-project`, set it to Public, and click *Create Repository* without adding any files yet.

**Step 2 — Open your project folder in VS Code**

```bash
# Navigate to your project directory
cd E:/ml-projects

# Launch VS Code from the terminal
code .
```

**Step 3 — Initialize Git locally**

```bash
git init
```

This creates a hidden `.git/` folder that tracks all changes. Your project directory is now a **local Git repository**.

**Step 4 — Create and commit your first file**

Create a `README.md` file with a brief project description:

```markdown
# End-to-End Machine Learning Project
```

Then stage and commit it:

```bash
git add README.md
git commit -m "first commit"
```

**Step 5 — Connect your local repo to GitHub**

```bash
# Set the default branch to main
git branch -M main

# Point your local repo to the remote GitHub repo
git remote add origin https://github.com/your-username/ml-project.git

# Verify the connection
git remote -v

# Push your code
git push -u origin main
```

**Step 6 — Configure your Git identity (one-time setup)**

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

This is required so GitHub knows who authored each commit.

---

### The `.gitignore` File

A `.gitignore` file tells Git which files and folders to **never track or commit**. This is critical because your virtual environment folder can contain thousands of files that have no place in a repository.

GitHub can auto-generate this for Python. Key entries it includes:

```
# Virtual environment
venv/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Distribution artifacts
*.egg-info/
dist/
build/
```

After GitHub creates it remotely, pull it down to sync:

```bash
git pull
```

---

## Section 2: Python Environment Management

### Why Create an Isolated Environment?

Every project has its own dependency requirements. Without isolation:

- Project A needing `numpy==1.21` breaks Project B needing `numpy==1.24`
- Your global Python gets polluted with conflicting packages
- There is no clean way to reproduce your setup on another machine

An isolated environment solves all of this.

### Creating a Project-Local Virtual Environment with Conda

The following command creates the environment **inside your project folder** rather than in Conda's global environments directory. This keeps everything self-contained.

```bash
conda create -p ./venv python=3.8 -y
```

| Flag | Meaning |
|------|---------|
| `-p ./venv` | Creates the environment in a local `venv/` subfolder |
| `python=3.8` | Pins the Python version |
| `-y` | Auto-confirms all prompts |

**Activate the environment:**

```bash
conda activate ./venv
```

Your terminal prompt will now show the environment path, confirming activation.

> **Why project-local?** When you freeze your dependencies later, you can reference them directly from the folder. It also makes the project fully portable.

---

## Section 3: Project Structure and Packaging

### The `src` Layout and `__init__.py`

Professional Python projects organize source code under a `src/` directory. To make Python treat any folder as a **package** (importable module), you must place an `__init__.py` file inside it.

```
ml-project/
│
├── src/
│   └── __init__.py        ← Makes src/ a Python package
│
├── setup.py
├── requirements.txt
└── README.md
```

The `__init__.py` can be completely empty. Its presence is the signal Python uses to recognize the folder as a package.

---

### Understanding `setup.py`

`setup.py` is the build script for your Python project. It allows you to:

1. **Package your ML application** as an installable Python module
2. **Publish it to PyPI** (Python Package Index) so others can `pip install` it
3. **Auto-discover all sub-packages** inside your project

Think of it this way: just as you run `pip install seaborn` to use Seaborn, your `setup.py` is what would allow someone to run `pip install ml-project` to use your application.

**Basic `setup.py` structure:**

```python
from setuptools import find_packages, setup

setup(
    name="ml-project",
    version="0.0.1",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
```

**What each parameter does:**

| Parameter | Purpose |
|-----------|---------|
| `name` | The package name as it appears on PyPI |
| `version` | Semantic version — update this with each release |
| `author` / `author_email` | Metadata shown on PyPI |
| `packages` | List of all packages to include |
| `install_requires` | Dependencies that get installed automatically |

**How `find_packages()` works:**

`find_packages()` scans your entire project directory and returns a list of every folder that contains an `__init__.py` file. This is how it automatically discovers `src/` and any nested sub-packages — you never have to list them manually.

---

### Understanding `requirements.txt`

`requirements.txt` is a plain-text file listing every library your project needs:

```
numpy
pandas
seaborn
scikit-learn
-e .
```

The last line, `-e .`, is important and deserves its own explanation.

#### What Does `-e .` Mean?

`-e .` stands for **editable install**, and the `.` refers to the current directory.

When you run:

```bash
pip install -r requirements.txt
```

The `-e .` line tells pip to find `setup.py` in the current directory and install your own project as a package in editable mode. This means:

- Your project's `src/` code becomes importable from anywhere in the environment
- Changes you make to `src/` are immediately reflected without reinstalling
- `setup.py` is automatically triggered and the package is built

---

### Writing the `get_requirements()` Helper Function

Rather than hardcoding dependencies inside `setup.py`, it's best practice to read them from `requirements.txt` programmatically. This keeps a single source of truth.

```python
from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads requirements.txt and returns a clean list of package names.
    The '-e .' entry is removed because it is a pip directive,
    not an actual package name.
    """
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="ml-project",
    version="0.0.1",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
```

**Why remove `-e .` from the list?**

`install_requires` in `setup.py` expects a list of package names like `["numpy", "pandas"]`. The string `"-e ."` is a pip-specific directive — not a package name — and passing it to `install_requires` would cause an error. We strip it out before returning the list.

**The `\n` replacement explained:**

`readlines()` preserves the newline character at the end of each line. Without the `.replace("\n", "")`, your list would look like `["numpy\n", "pandas\n"]`, and pip would fail to resolve those package names. The list comprehension cleans this up in one line.

---

## Section 4: The Complete Setup Flow — Visualized

```
requirements.txt
      │
      │  pip install -r requirements.txt
      ▼
pip reads each line
      │
      ├── numpy  ──────────────────────► installed
      ├── pandas ──────────────────────► installed
      ├── seaborn ─────────────────────► installed
      │
      └── -e .  ───► triggers setup.py
                           │
                           ├── find_packages() scans for __init__.py
                           ├── get_requirements() reads requirements.txt
                           └── Builds ml-project as an installable package
```

---

## Section 5: Committing Your Work

Once setup is complete, commit everything to GitHub:

```bash
# Stage all new files
git add .

# Check what will be committed
git status

# Commit with a meaningful message
git commit -m "Add setup.py, requirements.txt, and src package structure"

# Push to GitHub
git push -u origin main
```

---

## Summary: What We Built and Why

| Component | File | Purpose |
|-----------|------|---------|
| Version control | `.git/`, `.gitignore` | Track changes, collaborate, exclude junk files |
| Isolated environment | `venv/` (conda) | Prevent dependency conflicts across projects |
| Package builder | `setup.py` | Turn the ML app into an installable Python package |
| Dependency list | `requirements.txt` | Declare all libraries; reproducible installs |
| Package marker | `src/__init__.py` | Tell Python that `src/` is an importable package |

---

## Key Takeaways for Interviews

- Always mention that you version-controlled your project with Git and can walk through commit history
- Explain that you used a virtual environment to isolate dependencies
- Describe `setup.py` as the mechanism that allows your ML codebase to be treated as a first-class Python package
- Mention that `-e .` enables editable installs so development changes are immediately reflected without reinstalling

---

## What Comes Next

In the next phase of this project, we will implement:

1. **Logging** — capturing runtime events to files for debugging and monitoring
2. **Exception handling** — a structured approach to catching and reporting errors gracefully
3. **Formal project structure** — organizing components like data ingestion, transformation, model training, and evaluation into clean, maintainable modules