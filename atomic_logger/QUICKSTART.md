# 🚀 Quick Start Guide

Get SiteStamp running in 5 minutes.

## Prerequisites

- Flutter SDK 3.2.0+ installed ([Get Flutter](https://flutter.dev/docs/get-started/install))
- iOS: Xcode 14+ (macOS only)
- Android: Android Studio with SDK 21+

## Setup

```bash
# 1. Navigate to project
cd atomic_logger

# 2. Install dependencies
flutter pub get

# 3. Generate database code
dart run build_runner build --delete-conflicting-outputs

# 4. Run on device (make sure device/emulator is connected)
flutter run
```

## First Run

1. App will request **Camera** and **Location** permissions - tap **Allow**
2. Tap the **CAPTURE** button
3. Take a photo
4. View your timestamped entry in the list

## Development

### Hot Reload
While the app is running, save any file to hot reload changes instantly.

### Viewing Database
The SQLite database is at:
- iOS: `~/Library/Developer/CoreSimulator/Devices/[ID]/data/Containers/Data/Application/[ID]/Documents/atomic_logger.db`
- Android: `/data/data/com.atomiclogger.sitestamp/app_flutter/atomic_logger.db`

Use [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect.

### Changing Flavors
Edit `lib/main.dart` line 14:
```dart
final config = AppConfig.siteStamp; // or .secretSpot or .mnemosyne
```

## Building Release

```bash
# Android APK
flutter build apk --release

# iOS (then archive in Xcode)
flutter build ios --release
```

## Troubleshooting

**Database errors?**
```bash
flutter clean
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

**Camera/GPS not working?**
- Grant permissions in device Settings
- Test on physical device (not emulator)
- For GPS, go outdoors

## Next Steps

- Read full [README.md](README.md) for architecture details
- Review handoff document for product strategy
- Set up subscription backend (RevenueCat recommended)
- Create App Store/Play Store listings

---

**Need help?** Check the [Troubleshooting](README.md#troubleshooting) section in the main README.
