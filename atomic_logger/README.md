# Atomic Logger

**A local-first, offline-ready mobile utility that captures [GPS + Time + Media + Context] instantly.**

This repository contains the **Core Engine** that powers multiple distinct applications ("Skins"):
- 🏗️ **SiteStamp** - Construction & Trades (Priority 1)
- 🎣 **Secret Spot** - Fishing & Foraging (Priority 2)
- 📔 **Mnemosyne** - Life Logging (Priority 3)

---

## Current Status: SiteStamp v1.0 MVP

**Target Market**: Construction, Trades, Facility Management
**Pricing Model**: $9.99/month subscription
**Core Promise**: "Prove you were there. One tap."

### MVP Features (v1.0)
- ✅ Single-tap photo capture with camera
- ✅ Automatic GPS + timestamp stamping
- ✅ Offline-first SQLite storage
- ✅ List view of all entries with thumbnails
- ✅ Full-screen photo viewer
- ✅ Native share (photo + GPS + timestamp)
- ✅ Immutable "Proof Mode" (locked entries)
- ✅ High-contrast UI optimized for gloves

### Planned Features (v1.1+)
- Background enrichment (reverse geocoding, weather)
- PDF export with photo grid + map
- Voice-to-text notes
- Project tagging

---

## Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Framework | Flutter | Single codebase for iOS/Android |
| Database | Drift (SQLite) | Local-first, future-proof, portable |
| State Management | Riverpod | Scalable, type-safe |
| Location | Geolocator | Cross-platform GPS |
| Camera | Camera plugin | Native camera access |

---

## Project Structure

```
atomic_logger/
├── lib/
│   ├── config/
│   │   └── app_config.dart         # Flavor configurations
│   ├── models/
│   │   └── database.dart           # Drift schema & queries
│   ├── screens/
│   │   ├── home_screen.dart        # Main list view
│   │   ├── capture_screen.dart     # Camera + GPS capture
│   │   └── entry_detail_screen.dart # Full-screen photo view
│   ├── services/
│   │   ├── camera_service.dart     # Camera abstraction
│   │   └── location_service.dart   # GPS abstraction
│   ├── widgets/
│   │   └── entry_card.dart         # List item widget
│   └── main.dart                   # App entry point
├── android/                        # Android config
├── ios/                           # iOS config
└── pubspec.yaml                   # Dependencies
```

---

## Setup Instructions

### Prerequisites
1. Install Flutter SDK (3.2.0 or higher)
   ```bash
   # Check installation
   flutter doctor
   ```

2. Install platform tools:
   - **iOS**: Xcode 14+ (macOS only)
   - **Android**: Android Studio with SDK 21+

### Initial Setup

1. **Clone and navigate to project**
   ```bash
   cd atomic_logger
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Generate Drift database code**
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```

4. **Run on device/emulator**
   ```bash
   # iOS
   flutter run -d ios

   # Android
   flutter run -d android
   ```

---

## Development Workflow

### Running the App
```bash
# List available devices
flutter devices

# Run with hot reload
flutter run

# Run in release mode
flutter run --release
```

### Database Changes
When you modify `lib/models/database.dart`:
```bash
# Regenerate database code
dart run build_runner build --delete-conflicting-outputs
```

### Testing
```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

### Building Release Versions

#### Android APK
```bash
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

#### Android App Bundle (for Google Play)
```bash
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
```

#### iOS
```bash
flutter build ios --release
# Then open Xcode to archive and submit
```

---

## Data Schema

Each log entry is stored with this structure:

```dart
{
  "uuid": "unique-id-12345",
  "timestamp_utc": "2025-12-30T07:00:00Z",
  "local_timezone": "America/New_York",
  "location": {
    "lat": 34.61,
    "long": -82.48,
    "altitude": 245.0,
    "accuracy_meters": 3.5,
    "reverse_geo": "123 Main St, Williamston, SC" // v1.1+
  },
  "media": {
    "photo_path": "local/storage/img_123.jpg",
    "text_note": "Found a crack in foundation" // v1.1+
  },
  "is_locked": true // Immutable if true
}
```

The SQLite database file is stored at:
- **iOS**: `Application Documents Directory/atomic_logger.db`
- **Android**: `Application Documents Directory/atomic_logger.db`

---

## Flavors (Multi-App Strategy)

The core engine supports multiple app "flavors" configured via `lib/config/app_config.dart`:

| Flavor | Target Market | Theme | Features |
|--------|--------------|-------|----------|
| **SiteStamp** | Construction | Safety Orange/Black | Locked entries, simple export |
| **Secret Spot** | Anglers/Foragers | Night Vision (Red/Green) | Weather/moon/pressure data |
| **Mnemosyne** | Life Logging | Serif/Minimalist | Timeline view, "On This Day" |

### Switching Flavors (Dev Mode)
Edit `lib/main.dart`:
```dart
// Change this line:
final config = AppConfig.siteStamp;

// To:
final config = AppConfig.secretSpot;
// or
final config = AppConfig.mnemosyne;
```

---

## Permissions

### iOS (`ios/Runner/Info.plist`)
- `NSCameraUsageDescription` - Camera access for photo capture
- `NSLocationWhenInUseUsageDescription` - GPS for timestamping
- `NSPhotoLibraryUsageDescription` - Save/share photos

### Android (`android/app/src/main/AndroidManifest.xml`)
- `CAMERA` - Camera access
- `ACCESS_FINE_LOCATION` - GPS access
- `ACCESS_COARSE_LOCATION` - Fallback location
- `INTERNET` - For future enrichment features

All permissions are requested at runtime, not installation.

---

## Troubleshooting

### Camera not working
1. Check permissions in device settings
2. Ensure device has a camera (emulators may not)
3. Try on physical device

### GPS not working
1. Enable location services in device settings
2. Grant app location permission
3. Test outdoors (GPS doesn't work well indoors)

### Build errors with Drift
```bash
# Clean and regenerate
flutter clean
flutter pub get
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

### iOS build fails
1. Update CocoaPods: `cd ios && pod install`
2. Clean build folder in Xcode
3. Ensure Xcode 14+ is installed

---

## Deployment Checklist

### Before Launch
- [ ] Test on physical iOS device
- [ ] Test on physical Android device
- [ ] Test offline behavior (airplane mode)
- [ ] Test with gloves (button sizes)
- [ ] Verify GPS accuracy in various conditions
- [ ] Test battery drain during extended use
- [ ] Test with 100+ photos
- [ ] Configure app store assets (icons, screenshots)
- [ ] Set up subscription backend (RevenueCat/Stripe)
- [ ] Write privacy policy
- [ ] Write terms of service

### App Store Setup
1. **iOS**: Create app in App Store Connect
2. **Android**: Create app in Google Play Console
3. Configure in-app purchases ($9.99/month)
4. Upload screenshots and metadata
5. Submit for review

---

## Future Roadmap

### v1.1 (2-4 weeks post-launch)
- Background enrichment (geocoding, weather)
- Immutability toggle UI
- PDF export
- Voice notes

### v1.2 (Long-term)
- Project/client organization
- Calendar view
- Search functionality
- Team collaboration

### v2.0+ (Other Flavors)
- Launch Secret Spot
- Launch Mnemosyne
- Cross-flavor data migration

---

## License

Proprietary - All rights reserved

---

## Contact

For development questions or support, contact the development team.

---

**Built with Flutter 🚀**
