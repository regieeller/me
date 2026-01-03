# File Splitter Tool

A simple, no-frills utility to split large files into smaller chunks and merge them back together. Handles any file type (binary-safe).

## Features

- Split files of any type into configurable chunk sizes
- Merge chunks back into the original file
- Automatic manifest generation for easy merging
- Size verification to ensure data integrity
- Handles files up to 100MB easily (and beyond if needed)

## Usage

### Split a file

```bash
# Split into default 10MB chunks
python3 file_splitter.py split large_file.zip

# Split with custom chunk size (in MB)
python3 file_splitter.py split large_file.zip --size 5

# Split to specific directory
python3 file_splitter.py split large_file.zip --output ./chunks
```

### Merge chunks back together

```bash
# Merge using manifest file (recommended)
python3 file_splitter.py merge --manifest large_file.manifest

# Merge using pattern (without manifest)
python3 file_splitter.py merge --pattern "large_file_chunk_*.zip" --output large_file.zip
```

## How it works

1. **Splitting**: The tool reads your file in chunks and creates numbered piece files. It also creates a `.manifest` file that tracks metadata about the split operation.

2. **Merging**: Using the manifest file, the tool reassembles the chunks in the correct order and verifies the final file size matches the original.

## Output

When you split a file named `example.zip`, you get:

```
example_chunk_0000.zip
example_chunk_0001.zip
example_chunk_0002.zip
...
example.manifest
```

The manifest file contains information needed to merge the files back together.

## Example

```bash
# Split a 25MB file into 10MB chunks
$ python3 file_splitter.py split video.mp4 --size 10

Splitting file: video.mp4
File size: 25.00 MB
Chunk size: 10.00 MB
  Created: video_chunk_0000.mp4 (10.00 MB)
  Created: video_chunk_0001.mp4 (10.00 MB)
  Created: video_chunk_0002.mp4 (5.00 MB)

Split complete!
  Total chunks: 3
  Output directory: .
  Manifest: video.manifest

# Merge them back together
$ python3 file_splitter.py merge --manifest video.manifest

Merging chunks to: video.mp4
Expected chunks: 3
  Merged: video_chunk_0000.mp4 (10.00 MB)
  Merged: video_chunk_0001.mp4 (10.00 MB)
  Merged: video_chunk_0002.mp4 (5.00 MB)

Merge complete!
  Output file: video.mp4
  Final size: 25.00 MB
  ✓ Size verification passed
```

## Why use this?

- **Email attachments**: Split large files to send via email with size limits
- **Cloud storage**: Upload large files in smaller pieces for better reliability
- **Version control**: Break up binary files for easier management
- **Transfer limits**: Work around upload/download size restrictions
- **Workflow management**: Better organize large datasets into manageable pieces

## Requirements

- Python 3.6 or higher
- No external dependencies required
