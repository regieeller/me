import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:camera/camera.dart';
import 'package:uuid/uuid.dart';
import 'package:drift/drift.dart' as drift;
import '../config/app_config.dart';
import '../services/camera_service.dart';
import '../services/location_service.dart';
import '../models/database.dart';
import '../screens/home_screen.dart';

class CaptureScreen extends ConsumerStatefulWidget {
  final AppConfig config;

  const CaptureScreen({
    super.key,
    required this.config,
  });

  @override
  ConsumerState<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends ConsumerState<CaptureScreen> {
  final CameraService _cameraService = CameraService();
  final LocationService _locationService = LocationService();
  bool _isInitializing = true;
  bool _isSaving = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final success = await _cameraService.initialize();
    if (!success) {
      setState(() {
        _error = 'Failed to initialize camera. Please check permissions.';
        _isInitializing = false;
      });
      return;
    }

    // Check location permission
    final hasLocation = await _locationService.hasPermission();
    if (!hasLocation) {
      await _locationService.requestPermission();
    }

    setState(() {
      _isInitializing = false;
    });
  }

  Future<void> _captureAndSave() async {
    if (_isSaving) return;

    setState(() {
      _isSaving = true;
      _error = null;
    });

    try {
      // Take photo
      final photoPath = await _cameraService.takePicture();
      if (photoPath == null) {
        throw Exception('Failed to capture photo');
      }

      // Get GPS location
      final location = await _locationService.getCurrentLocation();
      if (location == null) {
        throw Exception('Failed to get GPS location');
      }

      // Create database entry
      final database = ref.read(databaseProvider);
      final uuid = const Uuid().v4();

      final entry = LogEntriesCompanion(
        uuid: drift.Value(uuid),
        timestampUtc: drift.Value(DateTime.now().toUtc()),
        localTimezone: drift.Value(DateTime.now().timeZoneName),
        lat: drift.Value(location.latitude),
        long: drift.Value(location.longitude),
        altitude: drift.Value(location.altitude),
        accuracyMeters: drift.Value(location.accuracy),
        photoPath: drift.Value(photoPath),
        isLocked: drift.Value(widget.config.defaultLockEntries),
      );

      await database.insertEntry(entry);

      // Success! Return to home screen
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Entry saved successfully'),
            duration: Duration(seconds: 2),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isSaving = false;
      });
    }
  }

  @override
  void dispose() {
    _cameraService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isInitializing) {
      return Scaffold(
        appBar: AppBar(title: const Text('Loading...')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_error != null && !_cameraService.isInitialized) {
      return Scaffold(
        appBar: AppBar(title: const Text('Error')),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 64, color: Colors.red),
                const SizedBox(height: 16),
                Text(
                  _error!,
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Go Back'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Camera preview
          if (_cameraService.controller != null)
            SizedBox.expand(
              child: CameraPreview(_cameraService.controller!),
            ),

          // Top bar with back button
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white, size: 32),
                    onPressed: () => Navigator.pop(context),
                  ),
                  if (widget.config.defaultLockEntries)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.black54,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        children: const [
                          Icon(Icons.lock, color: Colors.white, size: 16),
                          SizedBox(width: 4),
                          Text(
                            'PROOF MODE',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ),

          // Bottom capture button
          Align(
            alignment: Alignment.bottomCenter,
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.only(bottom: 32.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (_error != null && _isSaving == false)
                      Container(
                        margin: const EdgeInsets.only(bottom: 16),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.red,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          _error!,
                          style: const TextStyle(color: Colors.white),
                        ),
                      ),
                    GestureDetector(
                      onTap: _isSaving ? null : _captureAndSave,
                      child: Container(
                        width: 80,
                        height: 80,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.white, width: 4),
                          color: _isSaving
                              ? Colors.grey
                              : Theme.of(context).colorScheme.primary,
                        ),
                        child: _isSaving
                            ? const Padding(
                                padding: EdgeInsets.all(20.0),
                                child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 3,
                                ),
                              )
                            : const Icon(
                                Icons.camera_alt,
                                color: Colors.white,
                                size: 40,
                              ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
