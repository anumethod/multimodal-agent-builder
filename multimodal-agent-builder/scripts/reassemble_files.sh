#!/bin/bash

################################################################################
# Reassemble Chunked Dataset Files
# 
# This script reassembles chunked dataset files that were split for GitHub 
# compatibility. It reads manifest files, concatenates chunks in order,
# and verifies checksums to ensure data integrity.
#
# Usage: ./scripts/reassemble_files.sh [options]
#
# Options:
#   -h, --help     Show this help message
#   -v, --verbose  Enable verbose output
#   -d, --dry-run  Show what would be done without actually doing it
#   -f, --force    Overwrite existing files without prompting
#   -c, --cleanup  Remove chunk files after successful reassembly
#
################################################################################

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
VERBOSE=false
DRY_RUN=false
FORCE=false
CLEANUP=false

# Script configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CHUNKS_DIR="${REPO_ROOT}/train-test-validate/chunks"
OUTPUT_BASE="${REPO_ROOT}/train-test-validate"

# Statistics
TOTAL_FILES=0
PROCESSED_FILES=0
SKIPPED_FILES=0
FAILED_FILES=0

# Function to display usage
show_usage() {
    cat << EOF
Usage: $0 [options]

Reassemble chunked dataset files from manifest specifications.

Options:
    -h, --help     Show this help message
    -v, --verbose  Enable verbose output
    -d, --dry-run  Show what would be done without actually doing it
    -f, --force    Overwrite existing files without prompting
    -c, --cleanup  Remove chunk files after successful reassembly

Examples:
    $0                    # Reassemble all files
    $0 -v                 # Reassemble with verbose output
    $0 -d                 # Dry run to see what would be done
    $0 -f -c              # Force overwrite and cleanup chunks

EOF
}

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to print verbose messages
verbose_print() {
    if [ "$VERBOSE" = true ]; then
        print_message "$BLUE" "[VERBOSE] $1"
    fi
}

# Function to calculate MD5 checksum
calculate_md5() {
    local file=$1
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        md5 -q "$file"
    else
        # Linux
        md5sum "$file" | awk '{print $1}'
    fi
}

# Function to format file size
format_size() {
    local size=$1
    local units=("B" "KB" "MB" "GB")
    local unit=0
    local formatted_size=$size
    
    while (( formatted_size > 1024 && unit < 3 )); do
        formatted_size=$(( formatted_size / 1024 ))
        unit=$(( unit + 1 ))
    done
    
    echo "${formatted_size} ${units[$unit]}"
}

# Function to parse manifest file
parse_manifest() {
    local manifest_file=$1
    local manifest_dir=$(dirname "$manifest_file")
    
    verbose_print "Parsing manifest: $manifest_file"
    
    # Extract values from manifest
    local original_file=$(grep "^original_file:" "$manifest_file" | cut -d' ' -f2)
    local original_size=$(grep "^original_size:" "$manifest_file" | cut -d' ' -f2)
    local original_md5=$(grep "^original_md5:" "$manifest_file" | cut -d' ' -f2)
    
    # Extract chunk information
    local chunks=()
    while IFS= read -r line; do
        if [[ "$line" =~ name:\ (.+) ]]; then
            chunks+=("${BASH_REMATCH[1]}")
        fi
    done < "$manifest_file"
    
    echo "$original_file|$original_size|$original_md5|${chunks[*]}"
}

# Function to reassemble a single file
reassemble_file() {
    local manifest_file=$1
    local manifest_dir=$(dirname "$manifest_file")
    local manifest_basename=$(basename "$manifest_file" .manifest)
    
    print_message "$BLUE" "\n📦 Processing: $manifest_basename"
    
    # Parse manifest
    IFS='|' read -r original_file original_size original_md5 chunks_str <<< "$(parse_manifest "$manifest_file")"
    IFS=' ' read -ra chunks <<< "$chunks_str"
    
    # Determine output path
    local output_file="${REPO_ROOT}/${original_file}"
    local output_dir=$(dirname "$output_file")
    
    verbose_print "Output file: $output_file"
    verbose_print "Original size: $(format_size $original_size)"
    verbose_print "Original MD5: $original_md5"
    verbose_print "Number of chunks: ${#chunks[@]}"
    
    # Check if output file already exists
    if [ -f "$output_file" ] && [ "$FORCE" = false ] && [ "$DRY_RUN" = false ]; then
        print_message "$YELLOW" "  ⚠️  File already exists: $output_file"
        
        # Calculate MD5 of existing file
        local existing_md5=$(calculate_md5 "$output_file")
        if [ "$existing_md5" = "$original_md5" ]; then
            print_message "$GREEN" "  ✅ Existing file has correct checksum. Skipping."
            ((SKIPPED_FILES++))
            return 0
        else
            print_message "$YELLOW" "  ⚠️  Existing file has different checksum!"
            read -p "  Overwrite? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_message "$YELLOW" "  ⏭️  Skipping file"
                ((SKIPPED_FILES++))
                return 0
            fi
        fi
    fi
    
    # Dry run check
    if [ "$DRY_RUN" = true ]; then
        print_message "$YELLOW" "  [DRY RUN] Would reassemble ${#chunks[@]} chunks into: $output_file"
        if [ "$VERBOSE" = true ]; then
            for chunk in "${chunks[@]}"; do
                echo "           - $chunk"
            done
        fi
        return 0
    fi
    
    # Create output directory if it doesn't exist
    mkdir -p "$output_dir"
    
    # Reassemble chunks
    print_message "$BLUE" "  📂 Reassembling ${#chunks[@]} chunks..."
    
    # Remove existing file if forcing
    if [ -f "$output_file" ]; then
        rm -f "$output_file"
    fi
    
    # Concatenate chunks
    local chunk_count=0
    for chunk in "${chunks[@]}"; do
        local chunk_path="${manifest_dir}/${chunk}"
        
        if [ ! -f "$chunk_path" ]; then
            print_message "$RED" "  ❌ ERROR: Chunk not found: $chunk_path"
            ((FAILED_FILES++))
            return 1
        fi
        
        verbose_print "  Appending chunk: $chunk"
        cat "$chunk_path" >> "$output_file"
        
        ((chunk_count++))
        if [ "$VERBOSE" = false ]; then
            printf "\r  📂 Progress: %d/%d chunks" "$chunk_count" "${#chunks[@]}"
        fi
    done
    
    if [ "$VERBOSE" = false ]; then
        echo  # New line after progress indicator
    fi
    
    # Verify file size
    local actual_size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null)
    if [ "$actual_size" != "$original_size" ]; then
        print_message "$RED" "  ❌ ERROR: Size mismatch! Expected: $original_size, Got: $actual_size"
        ((FAILED_FILES++))
        return 1
    fi
    
    verbose_print "  Size verification passed"
    
    # Verify checksum
    print_message "$BLUE" "  🔍 Verifying checksum..."
    local actual_md5=$(calculate_md5 "$output_file")
    
    if [ "$actual_md5" != "$original_md5" ]; then
        print_message "$RED" "  ❌ ERROR: Checksum mismatch!"
        print_message "$RED" "     Expected: $original_md5"
        print_message "$RED" "     Got:      $actual_md5"
        ((FAILED_FILES++))
        return 1
    fi
    
    print_message "$GREEN" "  ✅ Successfully reassembled: $(format_size $actual_size)"
    ((PROCESSED_FILES++))
    
    # Cleanup chunks if requested
    if [ "$CLEANUP" = true ]; then
        print_message "$YELLOW" "  🧹 Removing chunk files..."
        for chunk in "${chunks[@]}"; do
            local chunk_path="${manifest_dir}/${chunk}"
            rm -f "$chunk_path"
            verbose_print "     Removed: $chunk"
        done
        print_message "$GREEN" "  ✅ Chunks removed"
    fi
    
    return 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -c|--cleanup)
            CLEANUP=true
            shift
            ;;
        *)
            print_message "$RED" "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
print_message "$GREEN" "════════════════════════════════════════════════════════════════"
print_message "$GREEN" "                Dataset File Reassembly Script                  "
print_message "$GREEN" "════════════════════════════════════════════════════════════════"

if [ "$DRY_RUN" = true ]; then
    print_message "$YELLOW" "🔍 DRY RUN MODE - No files will be modified"
fi

# Check if chunks directory exists
if [ ! -d "$CHUNKS_DIR" ]; then
    print_message "$RED" "❌ ERROR: Chunks directory not found: $CHUNKS_DIR"
    exit 1
fi

# Find all manifest files
print_message "$BLUE" "\n📋 Searching for manifest files..."
# Use array assignment for better compatibility (mapfile not available on older bash)
manifest_files=()
while IFS= read -r line; do
    manifest_files+=("$line")
done < <(find "$CHUNKS_DIR" -name "*.manifest" -type f | sort)

if [ ${#manifest_files[@]} -eq 0 ]; then
    print_message "$YELLOW" "⚠️  No manifest files found in $CHUNKS_DIR"
    exit 0
fi

TOTAL_FILES=${#manifest_files[@]}
print_message "$GREEN" "📊 Found $TOTAL_FILES manifest file(s) to process"

# Process each manifest file
for manifest_file in "${manifest_files[@]}"; do
    reassemble_file "$manifest_file" || true
done

# Print summary
print_message "$GREEN" "\n════════════════════════════════════════════════════════════════"
print_message "$GREEN" "                         Summary                                "
print_message "$GREEN" "════════════════════════════════════════════════════════════════"
print_message "$BLUE" "📊 Total manifests:    $TOTAL_FILES"
print_message "$GREEN" "✅ Successfully reassembled: $PROCESSED_FILES"

if [ $SKIPPED_FILES -gt 0 ]; then
    print_message "$YELLOW" "⏭️  Skipped (already exist): $SKIPPED_FILES"
fi

if [ $FAILED_FILES -gt 0 ]; then
    print_message "$RED" "❌ Failed:             $FAILED_FILES"
fi

# Exit with appropriate code
if [ $FAILED_FILES -gt 0 ]; then
    print_message "$RED" "\n⚠️  Some files failed to reassemble. Check the errors above."
    exit 1
else
    print_message "$GREEN" "\n🎉 All operations completed successfully!"
    
    if [ "$CLEANUP" = false ] && [ "$DRY_RUN" = false ]; then
        print_message "$BLUE" "\n💡 Tip: Run with -c flag to remove chunk files after reassembly"
    fi
fi

# Show location of reassembled files
if [ $PROCESSED_FILES -gt 0 ] && [ "$DRY_RUN" = false ]; then
    print_message "$BLUE" "\n📁 Reassembled files are located in:"
    print_message "$BLUE" "   • ${OUTPUT_BASE}/ML-Testing/"
    print_message "$BLUE" "   • ${OUTPUT_BASE}/ML-Training/"
    print_message "$BLUE" "   • ${OUTPUT_BASE}/ML-Validation/"
fi
