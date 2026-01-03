#!/usr/bin/env python3
"""
Simple File Splitter Tool

Splits large files into smaller chunks and merges them back together.
Handles any file type (binary-safe).
"""

import os
import sys
import argparse
from pathlib import Path


def format_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def split_file(input_file, chunk_size_mb=10, output_dir=None):
    """
    Split a file into smaller chunks.

    Args:
        input_file: Path to the file to split
        chunk_size_mb: Size of each chunk in MB (default: 10MB)
        output_dir: Directory to save chunks (default: same as input file)
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: File '{input_file}' not found")
        return False

    if not input_path.is_file():
        print(f"Error: '{input_file}' is not a file")
        return False

    # Setup output directory
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = input_path.parent

    # Calculate chunk size in bytes
    chunk_size = chunk_size_mb * 1024 * 1024
    file_size = input_path.stat().st_size

    print(f"Splitting file: {input_path.name}")
    print(f"File size: {format_size(file_size)}")
    print(f"Chunk size: {format_size(chunk_size)}")

    # Create base name for chunks
    base_name = f"{input_path.stem}_chunk"
    extension = input_path.suffix

    chunk_num = 0
    bytes_read = 0

    try:
        with open(input_path, 'rb') as infile:
            while True:
                chunk_data = infile.read(chunk_size)
                if not chunk_data:
                    break

                # Create chunk filename with zero-padded number
                chunk_filename = out_dir / f"{base_name}_{chunk_num:04d}{extension}"

                with open(chunk_filename, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)

                bytes_read += len(chunk_data)
                chunk_num += 1

                print(f"  Created: {chunk_filename.name} ({format_size(len(chunk_data))})")

        print(f"\nSplit complete!")
        print(f"  Total chunks: {chunk_num}")
        print(f"  Output directory: {out_dir}")

        # Create manifest file
        manifest_path = out_dir / f"{input_path.stem}.manifest"
        with open(manifest_path, 'w') as manifest:
            manifest.write(f"original_file={input_path.name}\n")
            manifest.write(f"original_size={file_size}\n")
            manifest.write(f"chunk_count={chunk_num}\n")
            manifest.write(f"chunk_size={chunk_size}\n")
            manifest.write(f"base_name={base_name}\n")
            manifest.write(f"extension={extension}\n")

        print(f"  Manifest: {manifest_path.name}")
        return True

    except Exception as e:
        print(f"Error splitting file: {e}")
        return False


def merge_files(manifest_file=None, chunk_pattern=None, output_file=None):
    """
    Merge split chunks back into original file.

    Args:
        manifest_file: Path to manifest file (preferred method)
        chunk_pattern: Pattern to match chunks (alternative method)
        output_file: Output filename (required if using chunk_pattern)
    """
    if manifest_file:
        return merge_from_manifest(manifest_file)
    elif chunk_pattern and output_file:
        return merge_from_pattern(chunk_pattern, output_file)
    else:
        print("Error: Either provide manifest file or both chunk_pattern and output_file")
        return False


def merge_from_manifest(manifest_file):
    """Merge chunks using manifest file."""
    manifest_path = Path(manifest_file)

    if not manifest_path.exists():
        print(f"Error: Manifest file '{manifest_file}' not found")
        return False

    # Read manifest
    manifest_data = {}
    with open(manifest_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            manifest_data[key] = value

    original_name = manifest_data['original_file']
    chunk_count = int(manifest_data['chunk_count'])
    base_name = manifest_data['base_name']
    extension = manifest_data['extension']

    output_path = manifest_path.parent / original_name
    manifest_dir = manifest_path.parent

    print(f"Merging chunks to: {original_name}")
    print(f"Expected chunks: {chunk_count}")

    try:
        with open(output_path, 'wb') as outfile:
            for i in range(chunk_count):
                chunk_filename = manifest_dir / f"{base_name}_{i:04d}{extension}"

                if not chunk_filename.exists():
                    print(f"Error: Missing chunk {chunk_filename.name}")
                    return False

                with open(chunk_filename, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    outfile.write(chunk_data)

                print(f"  Merged: {chunk_filename.name} ({format_size(len(chunk_data))})")

        final_size = output_path.stat().st_size
        print(f"\nMerge complete!")
        print(f"  Output file: {output_path}")
        print(f"  Final size: {format_size(final_size)}")

        # Verify size if available
        if 'original_size' in manifest_data:
            expected_size = int(manifest_data['original_size'])
            if final_size == expected_size:
                print(f"  ✓ Size verification passed")
            else:
                print(f"  ✗ Warning: Size mismatch (expected {format_size(expected_size)})")

        return True

    except Exception as e:
        print(f"Error merging files: {e}")
        return False


def merge_from_pattern(chunk_pattern, output_file):
    """Merge chunks using filename pattern."""
    pattern_path = Path(chunk_pattern)
    chunks = sorted(pattern_path.parent.glob(pattern_path.name))

    if not chunks:
        print(f"Error: No files found matching pattern '{chunk_pattern}'")
        return False

    output_path = Path(output_file)

    print(f"Found {len(chunks)} chunks")
    print(f"Merging to: {output_file}")

    try:
        with open(output_path, 'wb') as outfile:
            for chunk_path in chunks:
                with open(chunk_path, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    outfile.write(chunk_data)

                print(f"  Merged: {chunk_path.name} ({format_size(len(chunk_data))})")

        final_size = output_path.stat().st_size
        print(f"\nMerge complete!")
        print(f"  Output file: {output_path}")
        print(f"  Final size: {format_size(final_size)}")
        return True

    except Exception as e:
        print(f"Error merging files: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Split large files into smaller chunks or merge them back together',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split a file into 10MB chunks (default)
  %(prog)s split large_file.zip

  # Split with custom chunk size
  %(prog)s split large_file.zip --size 5

  # Split to specific directory
  %(prog)s split large_file.zip --output ./chunks

  # Merge using manifest file
  %(prog)s merge --manifest large_file.manifest

  # Merge using pattern (no manifest)
  %(prog)s merge --pattern "large_file_chunk_*.zip" --output large_file.zip
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Split command
    split_parser = subparsers.add_parser('split', help='Split a file into chunks')
    split_parser.add_argument('file', help='File to split')
    split_parser.add_argument('-s', '--size', type=int, default=10,
                            help='Chunk size in MB (default: 10)')
    split_parser.add_argument('-o', '--output', help='Output directory for chunks')

    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge chunks back together')
    merge_parser.add_argument('-m', '--manifest', help='Manifest file from split operation')
    merge_parser.add_argument('-p', '--pattern', help='Pattern to match chunk files')
    merge_parser.add_argument('-o', '--output', help='Output filename (required with --pattern)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'split':
        success = split_file(args.file, args.size, args.output)
        return 0 if success else 1

    elif args.command == 'merge':
        success = merge_files(args.manifest, args.pattern, args.output)
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
