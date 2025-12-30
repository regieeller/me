import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'config/app_config.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(
    const ProviderScope(
      child: AtomicLoggerApp(),
    ),
  );
}

class AtomicLoggerApp extends StatelessWidget {
  const AtomicLoggerApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Configure which flavor to use
    // This will eventually be set via build flavors
    final config = AppConfig.siteStamp; // Default to SiteStamp

    return MaterialApp(
      title: config.appName,
      theme: config.theme,
      debugShowCheckedModeBanner: false,
      home: HomeScreen(config: config),
    );
  }
}
