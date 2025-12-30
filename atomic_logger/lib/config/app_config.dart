import 'package:flutter/material.dart';

/// App flavor enumeration
enum AppFlavor {
  siteStamp,
  secretSpot,
  mnemosyne,
}

/// Configuration for each app flavor
class AppConfig {
  final AppFlavor flavor;
  final String appName;
  final String tagline;
  final ThemeData theme;
  final bool defaultLockEntries;
  final bool showEnrichmentData;
  final bool showMapView;

  const AppConfig({
    required this.flavor,
    required this.appName,
    required this.tagline,
    required this.theme,
    required this.defaultLockEntries,
    required this.showEnrichmentData,
    required this.showMapView,
  });

  /// SiteStamp: Construction & Trades
  static AppConfig get siteStamp => AppConfig(
        flavor: AppFlavor.siteStamp,
        appName: 'SiteStamp',
        tagline: 'Prove you were there. One tap.',
        defaultLockEntries: true, // Legal proof mode
        showEnrichmentData: false, // Keep it simple
        showMapView: false, // Not needed for v1.0
        theme: ThemeData(
          useMaterial3: true,
          brightness: Brightness.dark,
          colorScheme: ColorScheme.dark(
            primary: const Color(0xFFFF6B00), // Safety orange
            secondary: const Color(0xFFFFD600), // Warning yellow
            background: const Color(0xFF000000),
            surface: const Color(0xFF1A1A1A),
          ),
          scaffoldBackgroundColor: const Color(0xFF000000),
          appBarTheme: const AppBarTheme(
            backgroundColor: Color(0xFF1A1A1A),
            foregroundColor: Color(0xFFFF6B00),
            elevation: 0,
          ),
          cardTheme: CardTheme(
            color: const Color(0xFF1A1A1A),
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
              side: const BorderSide(color: Color(0xFF333333), width: 1),
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFFF6B00),
              foregroundColor: Colors.black,
              minimumSize: const Size(double.infinity, 56), // Large buttons for gloves
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
          textTheme: const TextTheme(
            headlineLarge: TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.bold,
              color: Color(0xFFFFFFFF),
            ),
            bodyLarge: TextStyle(
              fontSize: 18,
              color: Color(0xFFFFFFFF),
            ),
            bodyMedium: TextStyle(
              fontSize: 16,
              color: Color(0xFFCCCCCC),
            ),
          ),
        ),
      );

  /// Secret Spot: Fishing & Foraging (Future flavor)
  static AppConfig get secretSpot => AppConfig(
        flavor: AppFlavor.secretSpot,
        appName: 'Secret Spot',
        tagline: 'Your private black book.',
        defaultLockEntries: false,
        showEnrichmentData: true, // Weather, moon, pressure critical
        showMapView: true, // Satellite view
        theme: ThemeData(
          useMaterial3: true,
          brightness: Brightness.dark,
          colorScheme: ColorScheme.dark(
            primary: const Color(0xFF00FF00), // Night vision green
            secondary: const Color(0xFFFF0000), // Night vision red
            background: const Color(0xFF000000),
            surface: const Color(0xFF0A0A0A),
          ),
        ),
      );

  /// Mnemosyne: Life Logging (Future flavor)
  static AppConfig get mnemosyne => AppConfig(
        flavor: AppFlavor.mnemosyne,
        appName: 'Mnemosyne',
        tagline: 'Remember your life.',
        defaultLockEntries: false,
        showEnrichmentData: true,
        showMapView: true,
        theme: ThemeData(
          useMaterial3: true,
          brightness: Brightness.light,
          colorScheme: ColorScheme.light(
            primary: const Color(0xFF2C3E50),
            secondary: const Color(0xFF3498DB),
            background: const Color(0xFFFAFAFA),
            surface: Colors.white,
          ),
          textTheme: const TextTheme(
            headlineLarge: TextStyle(
              fontFamily: 'Serif',
              fontSize: 32,
              fontWeight: FontWeight.w300,
            ),
          ),
        ),
      );
}
