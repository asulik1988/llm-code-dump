#!/usr/bin/env python3

import sys
import os
import subprocess
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

def load_gitignore_patterns(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8', errors='replace') as f:
            patterns = f.read().splitlines()

    # Add forced ignores regardless of .gitignore
    patterns.append('.git/')

    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    return spec

def is_ignored(spec, base_dir, rel_path):
    if spec is None:
        return False
    # Convert path to Unix style for matching
    rel_path_unix = rel_path.replace('\\', '/')
    return spec.match_file(rel_path_unix)

def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_files.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory or does not exist.")
        sys.exit(1)

    spec = load_gitignore_patterns(directory)
    output_file = 'combined_output.txt'

    with open(output_file, 'w', encoding='utf-8', errors='replace') as out:
        for root, dirs, files in os.walk(directory):
            # Compute relative path
            relative_root = os.path.relpath(root, directory)
            if relative_root == '.':
                relative_root = ''

            # Filter directories based on ignore rules
            dirs[:] = [d for d in dirs if not is_ignored(spec, directory, os.path.join(relative_root, d))]

            for filename in files:
                rel_path = os.path.join(relative_root, filename) if relative_root else filename
                if is_ignored(spec, directory, rel_path):
                    continue

                full_path = os.path.join(root, filename)

                # Write file content with filename header
                out.write(f"<FILENAME: {rel_path}>\n\n")
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    out.write(content)
                except Exception as e:
                    out.write(f"[Error reading file: {e}]\n")

                out.write("\n################################################################################\n")

        # Append the tree output, ignoring venv, output, and .git
        try:
            tree_proc = subprocess.run(
                ["tree", directory, "--prune", "-I", "venv|output|.git"],
                capture_output=True, 
                text=True
            )
            out.write(tree_proc.stdout)
        except FileNotFoundError:
            out.write("[tree command not found]\n")

if __name__ == "__main__":
    main()
