import 'dart:io';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'package:permission_handler/permission_handler.dart';

class CameraService {
  CameraController? _controller;
  List<CameraDescription>? _cameras;

  /// Initialize camera
  Future<bool> initialize() async {
    try {
      // Request camera permission
      final status = await Permission.camera.request();
      if (!status.isGranted) return false;

      // Get available cameras
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) return false;

      // Initialize with back camera
      final backCamera = _cameras!.firstWhere(
        (camera) => camera.lensDirection == CameraLensDirection.back,
        orElse: () => _cameras!.first,
      );

      _controller = CameraController(
        backCamera,
        ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );

      await _controller!.initialize();
      return true;
    } catch (e) {
      return false;
    }
  }

  /// Get the camera controller
  CameraController? get controller => _controller;

  /// Check if camera is initialized
  bool get isInitialized => _controller?.value.isInitialized ?? false;

  /// Take a picture and save to app storage
  /// Returns the file path or null on failure
  Future<String?> takePicture() async {
    if (!isInitialized) return null;

    try {
      // Take the picture
      final image = await _controller!.takePicture();

      // Create permanent storage directory
      final directory = await getApplicationDocumentsDirectory();
      final imagesDir = Directory(p.join(directory.path, 'images'));
      if (!await imagesDir.exists()) {
        await imagesDir.create(recursive: true);
      }

      // Generate unique filename with timestamp
      final timestamp = DateTime.now().millisecondsSinceEpoch;
      final fileName = 'IMG_$timestamp.jpg';
      final filePath = p.join(imagesDir.path, fileName);

      // Move the temporary file to permanent storage
      final file = File(image.path);
      await file.copy(filePath);
      await file.delete(); // Clean up temp file

      return filePath;
    } catch (e) {
      return null;
    }
  }

  /// Dispose of camera resources
  void dispose() {
    _controller?.dispose();
    _controller = null;
  }
}
