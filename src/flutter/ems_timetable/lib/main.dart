import 'package:ems_timetable/timetable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:ems_timetable/mintY.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    // MintY.currentColor = const Color.fromARGB(255, 47, 61, 126);
    MintY.currentColor = const Color.fromARGB(255, 255, 177, 51);
    return MaterialApp(
      theme: MintY.theme(),
      home: Timetable(),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('de', 'DE'), // German
      ],
    );
  }
}
