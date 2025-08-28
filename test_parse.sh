#!/bin/bash

parse_manifest() {
    local manifest_file=$1
    
    echo "Parsing manifest: $manifest_file"
    
    # Extract values from manifest
    local original_file=$(grep "^original_file:" "$manifest_file" | cut -d' ' -f2-)
    local original_size=$(grep "^original_size:" "$manifest_file" | cut -d' ' -f2)
    local original_md5=$(grep "^original_md5:" "$manifest_file" | cut -d' ' -f2)
    
    # Extract chunk information - handle YAML indented format
    local chunks=()
    while IFS= read -r line; do
        # Look for lines with "- name:" pattern (YAML list format)
        if [[ "$line" =~ -\ *name:\ *(.+) ]]; then
            # Trim leading/trailing whitespace from chunk name
            local chunk_name="${BASH_REMATCH[1]}"
            chunk_name="${chunk_name#"${chunk_name%%[![:space:]]*}"}"
            chunk_name="${chunk_name%"${chunk_name##*[![:space:]]}"}"
            chunks+=("$chunk_name")
        fi
    done < "$manifest_file"
    
    echo "Original file: $original_file"
    echo "Original size: $original_size"
    echo "Original MD5: $original_md5"
    echo "Number of chunks: ${#chunks[@]}"
    echo "Chunks array contents:"
    for i in "${!chunks[@]}"; do
        echo "  [$i] = ${chunks[$i]}"
    done
    
    # This is what the original function returns
    echo ""
    echo "Output that would be returned: $original_file|$original_size|$original_md5|${chunks[*]}"
}

# Test with a manifest file
parse_manifest "/Users/admin/multimodal-agent-builder/train-test-validate/chunks/ML-Testing/open_images_test_asr.jsonl.manifest"
