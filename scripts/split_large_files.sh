#!/bin/bash

# Script to split large data files into smaller chunks for GitHub compatibility
# Each chunk will be max 90MB to stay safely under GitHub's 100MB limit

echo "Creating data chunks directory..."
mkdir -p train-test-validate/chunks

# Function to split a file
split_file() {
    local file_path="$1"
    local file_name=$(basename "$file_path")
    local dir_name=$(dirname "$file_path")
    local chunk_dir="train-test-validate/chunks/${dir_name#train-test-validate/}"
    
    mkdir -p "$chunk_dir"
    
    echo "Splitting $file_path..."
    
    # Split into 90MB chunks
    split -b 90m "$file_path" "$chunk_dir/${file_name}.part_"
    
    # Create a manifest file with checksums
    echo "Creating manifest for $file_name..."
    echo "# Manifest for $file_name" > "$chunk_dir/${file_name}.manifest"
    echo "original_file: $file_path" >> "$chunk_dir/${file_name}.manifest"
    echo "original_size: $(stat -f%z "$file_path" 2>/dev/null || stat -c%s "$file_path" 2>/dev/null)" >> "$chunk_dir/${file_name}.manifest"
    echo "original_md5: $(md5sum "$file_path" | cut -d' ' -f1)" >> "$chunk_dir/${file_name}.manifest"
    echo "chunks:" >> "$chunk_dir/${file_name}.manifest"
    
    for chunk in "$chunk_dir/${file_name}.part_"*; do
        if [ -f "$chunk" ]; then
            chunk_name=$(basename "$chunk")
            chunk_md5=$(md5sum "$chunk" | cut -d' ' -f1)
            echo "  - name: $chunk_name" >> "$chunk_dir/${file_name}.manifest"
            echo "    md5: $chunk_md5" >> "$chunk_dir/${file_name}.manifest"
        fi
    done
    
    echo "Split $file_name into $(ls -1 "$chunk_dir/${file_name}.part_"* 2>/dev/null | wc -l) chunks"
}

# Split large files (over 90MB)
echo "Finding and splitting large files..."

# Testing data
if [ -f "train-test-validate/ML-Testing/open_images_test_asr.jsonl" ]; then
    split_file "train-test-validate/ML-Testing/open_images_test_asr.jsonl"
fi

if [ -f "train-test-validate/ML-Testing/open_images_test_localized_narratives.jsonl" ]; then
    split_file "train-test-validate/ML-Testing/open_images_test_localized_narratives.jsonl"
fi

# Training data
if [ -f "train-test-validate/ML-Training/open_images_train_v6_asr.jsonl" ]; then
    split_file "train-test-validate/ML-Training/open_images_train_v6_asr.jsonl"
fi

if [ -f "train-test-validate/ML-Training/open_images_train_v6_localized_narratives-00009-of-00010.jsonl" ]; then
    split_file "train-test-validate/ML-Training/open_images_train_v6_localized_narratives-00009-of-00010.jsonl"
fi

# Validation data
if [ -f "train-test-validate/ML-Validation/open_images_validation_localized_narratives.jsonl" ]; then
    split_file "train-test-validate/ML-Validation/open_images_validation_localized_narratives.jsonl"
fi

echo ""
echo "✅ Splitting complete!"
echo ""
echo "Large files have been split into chunks in train-test-validate/chunks/"
echo "You can now remove the original large files from git and add the chunks instead."
echo ""
echo "To reassemble files later, use: ./scripts/reassemble_files.sh"
