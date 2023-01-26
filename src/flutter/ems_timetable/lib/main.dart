import 'dart:convert';

import 'package:ems_timetable/api_service.dart';
import 'package:ems_timetable/timetable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ems_timetable/entry.dart';
import 'package:ems_timetable/hour_label.dart';
import 'package:ems_timetable/mintY.dart';
import 'package:ems_timetable/space.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

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
    MintY.currentColor = const Color.fromARGB(255, 13, 110, 253);
    Future<Map<DateTime, Map<int, List<Entry>>>> timetableData =
        APIService.getTimetableData();
    return FutureBuilder(
      future: timetableData,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<Widget> contentElements = [];
          for (DateTime day in snapshot.data!.keys) {
            Map<int, List<Entry>> timetable = snapshot.data![day]!;
            contentElements.add(Text(
              DateFormat('EEEE, d. MMMM yyyy', Intl.getCurrentLocale())
                  .format(day),
              style: MintY.heading1,
              textAlign: TextAlign.center,
            ));
            contentElements.add(TimetableEMS(day: day, timetable: timetable));
          }
          return MaterialApp(
            theme: MintY.theme(),
            home: MintYPage(
              contentElements: contentElements,
            ),
          );
        } else if (snapshot.hasError) {
          return MaterialApp(
            theme: MintY.theme(),
            home: MintYPage(
              customContentElement: Text(snapshot.error.toString()),
            ),
          );
        } else {
          return MaterialApp(
            theme: MintY.theme(),
            home: MintYPage(
              customContentElement: MintYProgressIndicatorCircle(),
            ),
          );
        }
      },
    );
  }
}
