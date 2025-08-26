# Chunked Data Files

This directory contains large dataset files that have been split into smaller chunks for GitHub compatibility.

## Why Chunks?

GitHub has a 100MB file size limit. Our training and test datasets exceed this limit, so they've been split into 90MB chunks that can be safely stored in the repository.

## Data Structure

```
chunks/
├── ML-Testing/
│   ├── open_images_test_asr.jsonl.part_* (3 chunks)
│   ├── open_images_test_localized_narratives.jsonl.part_* (38 chunks)
│   └── *.manifest (checksums and metadata)
├── ML-Training/
│   ├── open_images_train_v6_asr.jsonl.part_* (11 chunks)
│   ├── open_images_train_v6_localized_narratives-00009-of-00010.jsonl.part_* (18 chunks)
│   └── *.manifest (checksums and metadata)
└── ML-Validation/
    ├── open_images_validation_localized_narratives.jsonl.part_* (13 chunks)
    └── *.manifest (checksums and metadata)
```

## How to Reassemble Files

To reassemble the chunked files into their original form:

```bash
# From the repository root
./scripts/reassemble_files.sh
```

This will:
1. Read the manifest files to understand the chunk structure
2. Concatenate chunks in the correct order
3. Verify checksums to ensure data integrity
4. Restore files to their original locations

## Original File Sizes

- **ML-Testing/open_images_test_asr.jsonl**: 217MB
- **ML-Testing/open_images_test_localized_narratives.jsonl**: 3.3GB
- **ML-Training/open_images_train_v6_asr.jsonl**: 929MB
- **ML-Training/open_images_train_v6_localized_narratives-00009-of-00010.jsonl**: 1.5GB
- **ML-Validation/open_images_validation_localized_narratives.jsonl**: 1.1GB

## Manifest Files

Each dataset has a `.manifest` file that contains:
- Original file path
- Original file size
- MD5 checksum of the original file
- List of chunks with their individual checksums

This ensures data integrity when reassembling files.

## Working with Chunked Data

For development and testing, you'll need to reassemble the files first:

```bash
# Reassemble all files
./scripts/reassemble_files.sh

# The original files will be restored to:
# - train-test-validate/ML-Testing/*.jsonl
# - train-test-validate/ML-Training/*.jsonl
# - train-test-validate/ML-Validation/*.jsonl
```

## Notes

- The 71MB validation ASR file is kept as-is (under GitHub's limit)
- Chunks are named with suffixes like `.part_aa`, `.part_ab`, etc.
- The reassembly script verifies checksums to ensure data integrity
- Original large files are gitignored to prevent accidental commits
