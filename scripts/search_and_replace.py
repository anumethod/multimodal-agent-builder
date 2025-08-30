#!/usr/bin/env python
"""
search_and_replace.py

Quick script to search (and optionally replace) regex patterns in your codebase using the SearchReplaceAgent.
- Usage:
    python scripts/search_and_replace.py --pattern PATTERN [--repl REPLACEMENT] [--ext EXT] [--apply]
- Default: just prints all matches with context and file names.
"""
import argparse
from src.agents.search_replace_agent import SearchReplaceAgent

parser = argparse.ArgumentParser()
parser.add_argument('--pattern', required=True, help='Regex pattern to search for')
parser.add_argument('--repl', help='Replacement string (if provided, will run replacement logic)')
parser.add_argument('--ext', nargs="*", help='Which file extensions to process (default: .py .js .ts)', default=['.py', '.js', '.ts'])
parser.add_argument('--ignore', nargs="*", default=['.venv', 'node_modules', 'dist'], help='Dirs to skip')
parser.add_argument('--apply', action='store_true', help='If set, makes replacements (default: dry run)')

args = parser.parse_args()
agent = SearchReplaceAgent(repo_root=".")

if args.repl:
    print(f"Searching and replacing in extensions: {args.ext} (dry run: {not args.apply}) ...")
    changes = agent.replace(pattern=args.pattern, repl=args.repl, file_extensions=args.ext, ignore_dirs=args.ignore, dry_run=not args.apply)
    for c in changes:
        print(c)
    print("Done.")
else:
    print(f"Searching for pattern: '{args.pattern}' in extensions {args.ext} ...")
    results = agent.search(pattern=args.pattern, file_extensions=args.ext, ignore_dirs=args.ignore)
    for file, lines in results.items():
        print(f"{file}:")
        for line in lines:
            print("  ", line)
    if not results:
        print("No matches found.")

