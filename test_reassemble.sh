#!/bin/bash

parse_manifest() {
    local manifest_file=$1
    local manifest_dir=$(dirname "$manifest_file")
    
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
    
    echo "$original_file|$original_size|$original_md5|${chunks[*]}"
}

test_reassemble() {
    local manifest_file=$1
    
    echo "Testing reassemble for: $manifest_file"
    echo "---"
    
    # Parse manifest
    local parse_output=$(parse_manifest "$manifest_file")
    echo "Parse output: $parse_output"
    echo "---"
    
    IFS='|' read -r original_file original_size original_md5 chunks_str <<< "$parse_output"
    
    echo "After splitting by |:"
    echo "  original_file: $original_file"
    echo "  original_size: $original_size"
    echo "  original_md5: $original_md5"
    echo "  chunks_str: $chunks_str"
    echo "---"
    
    IFS=' ' read -ra chunks <<< "$chunks_str"
    
    echo "After splitting chunks_str by space:"
    echo "  Number of chunks: ${#chunks[@]}"
    for i in "${!chunks[@]}"; do
        echo "    [$i] = ${chunks[$i]}"
    done
    echo "---"
    
    # Test what happens in the loop
    echo "Testing chunk path construction:"
    local manifest_dir=$(dirname "$manifest_file")
    for chunk in "${chunks[@]}"; do
        local chunk_path="${manifest_dir}/${chunk}"
        echo "  Chunk: $chunk"
        echo "  Path: $chunk_path"
        if [ -f "$chunk_path" ]; then
            echo "  Exists: YES"
        else
            echo "  Exists: NO"
        fi
    done
}

# Test with a manifest file
test_reassemble "/Users/admin/multimodal-agent-builder/train-test-validate/chunks/ML-Testing/open_images_test_asr.jsonl.manifest"
