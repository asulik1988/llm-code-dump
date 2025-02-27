# LLM Code Collector

A simple Python utility that collects and combines code files from a directory into a single text file, optimized for sharing with Large Language Models (LLMs).

## Overview

Code Collector scans a specified directory, gathers all code files while respecting `.gitignore` patterns, and creates a single output file. This is particularly useful when you need to share multiple files with an LLM for code reviews, refactoring suggestions, or other tasks that require contextual understanding of your codebase.

## Features

- Respects `.gitignore` patterns to skip irrelevant files
- Formats output with clear file headers for easy navigation
- Includes a directory tree structure at the end of the file
- Handles encoding issues gracefully
- Creates output in your current working directory, not in the scanned directory

## Requirements

- Python 3.6+
- `pathspec` package for parsing gitignore patterns
- `tree` command (optional, for directory structure visualization)

## Installation

1. Install required Python package:
   ```
   pip install pathspec
   ```

2. (Optional) Install the `tree` command:
   - On Ubuntu/Debian: `apt-get install tree`
   - On macOS with Homebrew: `brew install tree`
   - On Windows: Available through various package managers like Chocolatey

## Usage

```
python3 ./get-code.py <directory_path>
```

Example:
```
python3 ./get-code.py ~/projects/my-app
```

This will create a `combined_output.txt` file in your current directory containing all code from `~/projects/my-app`.

## Output Format

The output file contains:

1. Each file's content with a header:
   ```
   <FILENAME: path/to/file.js>

   [file content here]

   ################################################################################
   ```

2. A directory tree structure at the end (if `tree` command is available)

## Tips for Using with LLMs

1. For large codebases, consider running the script on specific subdirectories to keep outputs within token limits
2. When sharing with an LLM, explain what you're looking for (e.g., code review, bug identification, refactoring suggestions)
3. Reference specific filenames when asking questions about the code
4. For very large outputs, you may need to chunk the file into smaller pieces

## Limitations
- Very large codebases may exceed LLM token limits
