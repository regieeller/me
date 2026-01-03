#!/usr/bin/env python3
"""
Web interface for File Splitter Tool
Simple Flask app for splitting/merging files from any device
"""

from flask import Flask, request, render_template_string, send_file, jsonify, send_from_directory
import os
import tempfile
import zipfile
from pathlib import Path
import shutil
from file_splitter import split_file, merge_from_manifest

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Splitter</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
            background: #f5f5f5;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { font-size: 24px; margin-bottom: 10px; }
        h2 { font-size: 18px; margin-bottom: 15px; color: #333; }
        .subtitle { color: #666; margin-bottom: 20px; }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input[type="file"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
        }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .result {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
            display: none;
        }
        .result.show { display: block; }
        .result.success { background: #d4edda; color: #155724; }
        .result.error { background: #f8d7da; color: #721c24; }
        .download-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .loading {
            display: none;
            margin-top: 10px;
            color: #666;
        }
        .loading.show { display: block; }
    </style>
</head>
<body>
    <div class="card">
        <h1>File Splitter</h1>
        <p class="subtitle">Split large files or merge chunks</p>
    </div>

    <div class="card">
        <h2>Split File</h2>
        <form id="splitForm" enctype="multipart/form-data">
            <label>Choose file to split:</label>
            <input type="file" name="file" id="splitFile" required>

            <label>Chunk size (MB):</label>
            <input type="number" name="chunk_size" value="10" min="1" max="50">

            <button type="submit">Split File</button>
        </form>
        <div class="loading" id="splitLoading">Processing...</div>
        <div class="result" id="splitResult"></div>
    </div>

    <div class="card">
        <h2>Merge Chunks</h2>
        <form id="mergeForm" enctype="multipart/form-data">
            <label>Upload chunks and manifest (.zip all files together):</label>
            <input type="file" name="files" id="mergeFiles" multiple required>
            <p style="font-size: 14px; color: #666; margin-bottom: 15px;">
                Select all chunk files AND the .manifest file
            </p>

            <button type="submit">Merge Files</button>
        </form>
        <div class="loading" id="mergeLoading">Processing...</div>
        <div class="result" id="mergeResult"></div>
    </div>

    <script>
        document.getElementById('splitForm').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const result = document.getElementById('splitResult');
            const loading = document.getElementById('splitLoading');

            result.className = 'result';
            loading.className = 'loading show';

            try {
                const response = await fetch('/split', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                loading.className = 'loading';

                if (response.ok) {
                    result.className = 'result show success';
                    result.innerHTML = `
                        <strong>Success!</strong><br>
                        Created ${data.chunk_count} chunks<br>
                        <a href="/download/${data.filename}" class="download-link">Download ZIP</a>
                    `;
                } else {
                    result.className = 'result show error';
                    result.innerHTML = `<strong>Error:</strong> ${data.error}`;
                }
            } catch (error) {
                loading.className = 'loading';
                result.className = 'result show error';
                result.innerHTML = `<strong>Error:</strong> ${error.message}`;
            }
        };

        document.getElementById('mergeForm').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const result = document.getElementById('mergeResult');
            const loading = document.getElementById('mergeLoading');

            result.className = 'result';
            loading.className = 'loading show';

            try {
                const response = await fetch('/merge', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                loading.className = 'loading';

                if (response.ok) {
                    result.className = 'result show success';
                    result.innerHTML = `
                        <strong>Success!</strong><br>
                        File merged: ${data.original_name}<br>
                        Size: ${data.size}<br>
                        <a href="/download/${data.filename}" class="download-link">Download File</a>
                    `;
                } else {
                    result.className = 'result show error';
                    result.innerHTML = `<strong>Error:</strong> ${data.error}`;
                }
            } catch (error) {
                loading.className = 'loading';
                result.className = 'result show error';
                result.innerHTML = `<strong>Error:</strong> ${error.message}`;
            }
        };
    </script>
</body>
</html>
"""


def format_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/split', methods=['POST'])
def split():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        chunk_size = int(request.form.get('chunk_size', 10))

        # Create temp directory for this operation
        temp_dir = Path(tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER']))
        input_path = temp_dir / file.filename

        # Save uploaded file
        file.save(input_path)

        # Split the file
        split_file(str(input_path), chunk_size, str(temp_dir))

        # Create ZIP of all chunks and manifest
        zip_name = f"{input_path.stem}_chunks.zip"
        zip_path = temp_dir / zip_name

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for item in temp_dir.iterdir():
                if item != zip_path and item != input_path:
                    zipf.write(item, item.name)

        return jsonify({
            'success': True,
            'filename': zip_path.name,
            'chunk_count': len(list(temp_dir.glob('*_chunk_*.bin'))) + len(list(temp_dir.glob('*_chunk_*.*'))),
            'download_path': f'/download/{temp_dir.name}/{zip_path.name}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/merge', methods=['POST'])
def merge():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400

        # Create temp directory for this operation
        temp_dir = Path(tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER']))

        # Save all uploaded files
        manifest_file = None
        for file in files:
            if file.filename:
                file_path = temp_dir / file.filename
                file.save(file_path)
                if file.filename.endswith('.manifest'):
                    manifest_file = file_path

        if not manifest_file:
            return jsonify({'error': 'No manifest file found'}), 400

        # Merge the files
        merge_from_manifest(str(manifest_file))

        # Find the merged file (should be the newest file that's not a chunk or manifest)
        merged_files = [f for f in temp_dir.iterdir()
                       if not f.name.endswith('.manifest')
                       and '_chunk_' not in f.name]

        if not merged_files:
            return jsonify({'error': 'Merge failed - no output file found'}), 500

        merged_file = merged_files[0]

        return jsonify({
            'success': True,
            'filename': merged_file.name,
            'original_name': merged_file.name,
            'size': format_size(merged_file.stat().st_size),
            'download_path': f'/download/{temp_dir.name}/{merged_file.name}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<path:filename>')
def download(filename):
    """Download a file from the temp directory."""
    # Handle both formats: "tempdir/file.zip" and "file.zip"
    if '/' in filename:
        parts = filename.split('/', 1)
        directory = os.path.join(app.config['UPLOAD_FOLDER'], parts[0])
        file = parts[1]
    else:
        # Look for the file in all temp directories
        for temp_dir in Path(app.config['UPLOAD_FOLDER']).iterdir():
            if temp_dir.is_dir():
                file_path = temp_dir / filename
                if file_path.exists():
                    directory = str(temp_dir)
                    file = filename
                    break
        else:
            return "File not found", 404

    return send_from_directory(directory, file, as_attachment=True)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("File Splitter Web Interface")
    print("="*50)
    print("\nStarting server...")
    print("\nAccess from your phone:")
    print("  1. Make sure your phone is on the same WiFi network")
    print("  2. Find your computer's IP address:")
    print("     - On Linux/Mac: ifconfig or ip addr")
    print("     - On Windows: ipconfig")
    print("  3. Open browser on your phone and go to:")
    print("     http://YOUR_IP_ADDRESS:5000")
    print("\n" + "="*50 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False)
