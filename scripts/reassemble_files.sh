#!/bin/bash

# Script to reassemble chunked data files back to their original form

echo "Reassembling chunked data files..."

# Function to reassemble a file from chunks
reassemble_file() {
    local manifest_file="$1"
    local chunk_dir=$(dirname "$manifest_file")
    local file_name=$(basename "$manifest_file" .manifest)
    
    # Read original file path from manifest
    local original_path=$(grep "^original_file:" "$manifest_file" | cut -d' ' -f2)
    local original_md5=$(grep "^original_md5:" "$manifest_file" | cut -d' ' -f2)
    
    echo "Reassembling $file_name..."
    
    # Create output directory if it doesn't exist
    mkdir -p "$(dirname "$original_path")"
    
    # Concatenate all chunks in order
    cat "$chunk_dir/${file_name}.part_"* > "$original_path"
    
    # Verify checksum
    local new_md5=$(md5sum "$original_path" | cut -d' ' -f1)
    
    if [ "$new_md5" = "$original_md5" ]; then
        echo "✅ Successfully reassembled $file_name (checksum verified)"
    else
        echo "❌ Error: Checksum mismatch for $file_name"
        echo "   Expected: $original_md5"
        echo "   Got: $new_md5"
        return 1
    fi
}

# Find all manifest files and reassemble
echo "Finding manifest files..."

for manifest in train-test-validate/chunks/*/*.manifest; do
    if [ -f "$manifest" ]; then
        reassemble_file "$manifest"
    fi
done

echo ""
echo "✅ Reassembly complete!"
echo ""
echo "Original data files have been restored from chunks."
echo "You can now use the full data files for training and testing."
