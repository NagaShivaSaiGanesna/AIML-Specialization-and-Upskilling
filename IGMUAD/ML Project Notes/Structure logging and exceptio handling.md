# End-to-End ML Project: Structure, Logging & Exception Handling

## Introduction & What We're Building

A professional ML codebase is not a single script — it is a **system of interconnected modules**, each with a single, clear responsibility. This session covers two foundational pillars:

1. **Project structure** — where each type of code lives and why
2. **Cross-cutting concerns** — logging and exception handling that work uniformly across the entire application

Understanding this skeleton deeply means you can drop *any* dataset or problem into it and know exactly where every piece of code belongs.

---

## Section 1: The Professional ML Project Structure

### The Core Philosophy — Modular Programming

Every component of an ML pipeline has a distinct job. When you separate these jobs into individual files and folders, you get:

- **Readability** — anyone joining the team immediately knows where to look
- **Testability** — each module can be tested in isolation
- **Reusability** — a data transformation module written well can be reused across projects
- **Industry alignment** — this mirrors how real engineering teams structure ML systems

### The Complete Folder Layout

```
ml-project/
│
├── src/
│   ├── __init__.py
│   │
│   ├── components/                  ← Training pipeline building blocks
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/                    ← Orchestrates the components
│   │   ├── __init__.py
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   │
│   ├── logger.py                    ← Centralised logging setup
│   ├── exception.py                 ← Custom exception class
│   └── utils.py                     ← Shared helper functions
│
├── setup.py
├── requirements.txt
└── README.md
```

Every folder contains an `__init__.py` so Python treats it as an importable package.

---

### Understanding `components/`

Components are the **individual stages of your ML pipeline**. Think of them as assembly-line stations — each does one job and passes its output to the next.

| File | Responsibility |
|------|---------------|
| `data_ingestion.py` | Read raw data from databases, files, or APIs; split into train/test sets |
| `data_transformation.py` | Encode categoricals, scale numerics, handle missing values, engineer features |
| `model_trainer.py` | Train models, evaluate metrics (R², confusion matrix, etc.), select the best model |

### Understanding `pipeline/`

Pipelines are the **directors** — they call components in the right order.

| File | Responsibility |
|------|---------------|
| `train_pipeline.py` | Triggers ingestion → transformation → training in sequence |
| `predict_pipeline.py` | Loads saved model artifacts and generates predictions for new data |

### Understanding `utils.py`

Any function that is used by **more than one component** lives here. Examples:

- Connecting to MongoDB
- Saving and loading model pickle files to/from cloud storage
- Generic data reading utilities

This prevents code duplication and creates a single place to update shared logic.

---

## Section 2: Custom Exception Handling

### Why Not Use Python's Built-in Exceptions Directly?

Python's default exceptions tell you *what* went wrong, but not precisely *where* in a large multi-file project. A `ZeroDivisionError` with no file name or line number context is nearly useless when debugging a system with 15+ files.

A **custom exception** enriches every error with:
- The exact **script filename** where the error occurred
- The exact **line number** of the failure
- The **original error message**

### The `sys` Module — The Key to Error Introspection

The `sys` module gives Python access to its own runtime internals. The critical function is `sys.exc_info()`, which returns a tuple of three values when called inside an exception handler:

```
(exception_type, exception_value, traceback_object)
```

We are only interested in the third element — the **traceback object** — because it contains the file name and line number.

### Complete `exception.py` with Explanation

```python
import sys
from src.logger import logging


def error_message_detail(error, error_detail: sys) -> str:
    """
    Extracts a rich error message from the current exception context.

    Parameters:
        error        : The exception object caught in the except block
        error_detail : The sys module, passed in to access exc_info()

    Returns:
        A formatted string with script name, line number, and error message
    """
    # exc_info() returns (type, value, traceback). We only need the traceback.
    _, _, exc_tb = error_detail.exc_info()

    # Navigate the traceback object to find the source file and line number
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = (
        "Error occurred in Python script: [{0}] "
        "at line number: [{1}] "
        "with message: [{2}]"
    ).format(file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    """
    A project-wide custom exception that enriches error messages
    with file name and line number context.
    """

    def __init__(self, error_message, error_detail: sys):
        # Initialise the parent Exception class with the raw message
        super().__init__(error_message)

        # Enrich the message using our helper function
        self.error_message = error_message_detail(
            error=error_message,
            error_detail=error_detail
        )

    def __str__(self):
        # When the exception is printed, show the enriched message
        return self.error_message
```

### How the Traceback Object Properties Work

```
sys.exc_info()
    └── [2] → traceback object (exc_tb)
                  └── .tb_frame         → current stack frame
                            └── .f_code → code object for the frame
                                    └── .co_filename  → script file path
                  └── .tb_lineno        → line number of the error
```

### How to Use `CustomException` Anywhere in the Project

```python
from src.exception import CustomException
from src.logger import logging
import sys

try:
    result = 1 / 0  # Deliberately trigger a ZeroDivisionError
except Exception as e:
    raise CustomException(e, sys)
```

**Output you will see:**

```
Error occurred in Python script: [src/components/data_ingestion.py]
at line number: [47]
with message: [division by zero]
```

---

## Section 3: Centralised Logging

### Why Logging Instead of `print()`?

| `print()` | `logging` |
|-----------|-----------|
| Only visible in the terminal | Saved to a persistent file |
| Disappears when the session ends | Reviewable after the fact |
| No timestamp or context | Includes timestamp, level, line number |
| Cannot be filtered by severity | Filter by DEBUG, INFO, WARNING, ERROR |
| Useless in production | Industry standard for monitoring |

### Log File Naming Convention

Each run of the application creates a **new, timestamped log file** so logs from different runs never overwrite each other.

```
logs/
├── 06_15_2024_10_30_45.log
├── 06_15_2024_14_22_11.log
└── 06_16_2024_09_05_33.log
```

### Complete `logger.py` with Explanation

```python
import logging
import os
from datetime import datetime

# --- Step 1: Generate a unique log file name for this run ---
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# --- Step 2: Build the full directory path for the logs folder ---
# os.getcwd() returns the project root. We place logs/ there.
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# --- Step 3: Create the logs/ directory if it doesn't exist ---
# exist_ok=True means: don't raise an error if the folder is already there
os.makedirs(logs_path, exist_ok=True)

# --- Step 4: Build the full path to the actual .log file ---
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# --- Step 5: Configure the root logger ---
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
```

### Understanding the Log Format

The format string `"[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"` produces entries like:

```
[ 2024-06-15 10:30:45,123 ] 20 root - INFO - Data ingestion started
```

| Placeholder | What It Shows |
|-------------|---------------|
| `%(asctime)s` | Human-readable timestamp |
| `%(lineno)d` | Line number where `logging.info()` was called |
| `%(name)s` | Logger name (defaults to `root`) |
| `%(levelname)s` | Severity level: INFO, WARNING, ERROR |
| `%(message)s` | Your custom message string |

### How to Use the Logger Anywhere in the Project

```python
from src.logger import logging

logging.info("Data ingestion component started")
logging.info(f"Train dataset shape: {train_df.shape}")
logging.warning("Missing values detected in column: Age")
logging.error("Model training failed — check hyperparameters")
```

---

## Section 4: Connecting Exception Handling and Logging

The real power comes from using both together. Every caught exception gets both **raised with context** and **written to the log file**:

```python
from src.exception import CustomException
from src.logger import logging
import sys

def divide(a, b):
    try:
        logging.info("Attempting division operation")
        result = a / b
        logging.info(f"Division successful: result = {result}")
        return result
    except Exception as e:
        logging.error("Division failed")
        raise CustomException(e, sys)
```

This pattern means:
- The log file records that the operation was attempted
- The log file records that it failed
- The raised `CustomException` carries the exact file and line number for debugging

---

## Section 5: Verifying Everything Works

### Test the Logger

```bash
# From the project root with the virtual environment active
python src/logger.py
```

Check that a `logs/` folder appeared containing a `.log` file with your message.

### Test the Custom Exception

```python
# Add temporarily to exception.py for testing
if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        raise CustomException(e, sys)
```

```bash
python src/exception.py
```

Expected output:
```
Error occurred in Python script: [src/exception.py]
at line number: [line_number]
with message: [division by zero]
```

---

## Section 6: Committing the Project Structure

Once everything is verified, commit it all:

```bash
git add .
git commit -m "Add project structure, logging, and exception handling"
git push -u origin main
```

---

## Full Mental Model — How Everything Connects

```
Any component (e.g., data_ingestion.py)
        │
        │  from src.logger import logging
        │  from src.exception import CustomException
        │
        ├──► logging.info("Step started")
        │
        ├──► try:
        │        [business logic]
        │
        └──► except Exception as e:
                 logging.error("Step failed")
                 raise CustomException(e, sys)
                         │
                         ▼
              Enriched error message:
              "Error in [file] at line [n]: [message]"
                         │
                         ▼
              Written to: logs/MM_DD_YYYY_HH_MM_SS.log
```

---

## Summary: What We Built and Why

| File | Purpose | Used By |
|------|---------|---------|
| `components/data_ingestion.py` | Read and split raw data | `train_pipeline.py` |
| `components/data_transformation.py` | Feature engineering | `train_pipeline.py` |
| `components/model_trainer.py` | Train and evaluate models | `train_pipeline.py` |
| `pipeline/train_pipeline.py` | Orchestrate training end-to-end | Entry point / scheduler |
| `pipeline/predict_pipeline.py` | Serve predictions on new data | Web app / API |
| `utils.py` | Shared helpers (DB connections, file I/O) | All components |
| `logger.py` | Persistent, timestamped log files | All components |
| `exception.py` | Contextual error messages with file + line | All components |

---

## What Comes Next

In the next session we will:

1. Define the **problem statement** and explore the dataset with EDA
2. Write the full **`data_ingestion.py`** component — reading from a flat file initially, then from **MongoDB** to simulate a real database workflow
3. Build `data_transformation.py` and `model_trainer.py` on top of the structure we have just established