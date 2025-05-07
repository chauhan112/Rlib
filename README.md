# Rlib - Personal Python Utility Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Placeholder - Add actual license -->

## Overview

Rlib is a comprehensive personal Python library developed by chauhan112. It serves as a collection of tools, utilities, abstractions, and experiments built over time to assist with various development tasks, data management, code analysis, and creating interactive user interfaces, primarily within the Jupyter Notebook environment.

Due to its nature as a personal toolkit evolved over years (as reflected in the `timeline` directory structure), it contains a diverse and eclectic mix of functionalities.

## Key Features & Modules

Rlib provides a wide range of capabilities, broadly categorized as:

*   **Core Utilities:**
    *   **File & Path Management (`Path.py`, `FileDatabase.py`):** Robust tools for filesystem navigation, file I/O, extension filtering, path manipulation, and watching file changes (`modules/DataServer/FileObserve.py`).
    *   **Data Serialization & Storage (`SerializationDB.py`, `PickleCRUDDB.py`, `StorageSystem.py`):** Utilities for saving and loading data using Pickle, YAML, and potentially custom binary/compressed formats (`CompressDB.py`). Includes CRUD abstractions.
    *   **String & Regex (`WordDB.py`, `RegexDB.py`):** Helpers for string manipulation, tokenization, regex searching, and replacement.
    *   **Data Structures (`DataStructure.py`, `ListDB.py`, `TreeDB.py`):** Functions for handling lists, dictionaries, trees, CSVs, and custom data structures.
    *   **Time & Date (`TimeDB.py`):** Utilities for timestamping, date calculations, scheduling, and timers.
    *   **Logging (`Logger.py`, `modules/Logger`):** Various logging implementations (Pickle, Text) and specialized loggers (e.g., `FoodLogger`, `StatusLogger`).
*   **Data Management & Exploration:**
    *   **Database Abstractions (`Database.py`):** Wrappers and utilities for interacting with different data sources (files, dictionaries, potentially SQL via `sql_crud.py`).
    *   **Data Exploration Tools (`ExplorerDB.py`, `modules/Explorer`):** Interactive explorers for dictionaries, filesystems, and Zip archives, often using `ipywidgets`.
    *   **Search Systems (`SearchSystem.py`, `modules/SearchSystem`):** Multiple search engine implementations (Dictionary, File Content, PDF, URL, etc.).
*   **Jupyter Integration & GUIs:**
    *   **Widgets (`WidgetsDB.py`, `modules/GUIs`, timeline modules):** Extensive use and creation of custom interactive widgets using `ipywidgets`.
    *   **Jupyter Utilities (`jupyterDB.py`, `NotebookDB.py`):** Helpers for interacting with the Jupyter environment, managing notebooks, and displaying content.
*   **Code Analysis & Parsing:**
    *   **AST Parsing (`modules/code_parser/ast_parser.py`):** Tools for parsing Python code using Abstract Syntax Trees.
    *   **Dependency Extraction (`modules/code_parser/dependency.py`):** Utilities to analyze and visualize code dependencies.
    *   **Code Analysis (`CodeDB.py`, `ProjectAnalysis.py`):** Functions for analyzing code complexity (LOC, cyclomatic complexity) and structure.
*   **Specialized Tools:**
    *   **Math & Numerics (`MathObjectDB.py`, `NumericalAnalysis.py`):** Classes and functions for mathematical operations, ranges, and numerical methods. Integration with SymPy (`projects/sympy`).
    *   **Image Processing (`ImageProcessing.py`):** Basic image loading, manipulation, text extraction (OCR), and display utilities.
    *   **AI/ML Helpers (`AIAlgoDB.py`, archived ML code):** Implementations or helpers for algorithms like Genetic Algorithms, Perceptron, Dijkstra, etc.
    *   **Project/Task Management (`ProjectSerialization.py`, `archives/TaskManger.py`):** Utilities for archiving projects and managing tasks.
    *   **Version Control (`VersionSystem.py`, `GitDB.py`):** Simple wrappers around Git commands.
*   **Multi-language Utilities (`cpp/`, `java/`, `javascript/`, `kotlin/`):** Basic utilities or wrappers related to other programming languages.

## Module Highlights

*   **Root `.py` Files:** Contain many of the core, frequently used utilities (e.g., `Path.py`, `Database.py`, `TimeDB.py`, `ListDB.py`, `SerializationDB.py`).
*   **`modules/`:** Houses more complex, structured sub-libraries like `DataServer`, `Explorer`, `Logger`, `SearchSystem`, `code_parser`.
*   **`timeline/`:** Contains code developed chronologically (t2022, t2023, t2024), often featuring experiments, specific solutions, and advanced `ipywidgets`-based GUIs.
*   **`archives/`:** Stores older code, specific project analyses (e.g., `micpad_analysis`), and various specialized data storage modules.
*   **`nice_design/`:** Appears to be an area for exploring potentially cleaner or more structured designs for certain functionalities (e.g., `dicrud.py`).
*   **`projects/`:** Contains standalone projects or examples built using the Rlib library itself.

## Installation

As a personal library, Rlib is likely used directly by cloning the repository and ensuring the root directory is in the Python path.

```bash
git clone <repository_url> Rlib
# Add the path to Rlib to your PYTHONPATH or manage via sys.path in scripts/notebooks
```

*Potentially, a `setup.py` might exist or could be added for standard installation using pip:*

```bash
# cd Rlib
# pip install .
```
