import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ems_timetable/entry.dart';
import 'package:ems_timetable/hour_label.dart';
import 'package:ems_timetable/mintY.dart';
import 'package:ems_timetable/space.dart';
import 'package:http/http.dart' as http;

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
    String id = Uri.base.queryParameters["id"]!;

    print("ID: $id");

    Future<http.Response> reponse = http.get(Uri.parse('/events/2/timetable/'));

    List<Entry> entries = [
      Entry(
        length: 10,
        title: "Begrüßung",
        start: DateTime.utc(2022, 11, 12, 10, 00),
        track: 0,
      ),
      Entry(
        length: 50,
        title:
            "Podiumsdiskussion: Raus aus der Bubble! - Open Source in das Bewusstsein der Gesellschaft bringen",
        start: DateTime.utc(2022, 11, 12, 10, 10),
        track: 0,
      ),
      Entry(
        length: 40,
        title: "Zehn Zutaten für eine zufriedene Community",
        start: DateTime.utc(2022, 11, 12, 11, 05),
        track: 0,
      ),
      Entry(
        length: 25,
        title: "Übersicht über die Linux Desktops",
        start: DateTime.utc(2022, 11, 12, 12, 00),
        track: 0,
      ),
      Entry(
        length: 60,
        title: "ProxMox der Linux Vertualisierer",
        start: DateTime.utc(2022, 11, 12, 11, 05),
        track: 1,
      ),
      Entry(
        length: 60,
        title: "Softwareverteilung mit m23",
        start: DateTime.utc(2022, 11, 12, 12, 10),
        track: 1,
      ),
      Entry(
        length: 45,
        title: "OpenCelium - Verbindet Ihre API-fähigen Applikationen ",
        start: DateTime.utc(2022, 11, 12, 13, 15),
        track: 1,
      ),
    ];
    Map<int, List<Entry>> timetable = {};
    DateTime earliestStart = entries.first.start;
    DateTime latestTime = entries.first.start;
    for (Entry e in entries) {
      if (!timetable.keys.contains(e.track)) {
        timetable[e.track] = [];
      }
      if (e.start.compareTo(earliestStart) < 0) {
        earliestStart = e.start;
      }
      DateTime eEnd = e.start.add(Duration(minutes: e.length));
      if (eEnd.compareTo(latestTime) > 0) {
        latestTime = eEnd;
      }
      timetable[e.track]!.add(e);
    }
    for (int track in timetable.keys) {
      timetable[track]!.sort(((a, b) => a.start.compareTo(b.start)));
    }

    // Prepare Row
    List<Widget> rowChildren = [];
    // First for time annotations:
    int lengthInHours = latestTime.difference(earliestStart).inHours;
    DateTime hour =
        earliestStart.subtract(Duration(minutes: earliestStart.minute));
    List<Widget> firstColumnChildren = [];
    for (int i = 0; i < lengthInHours + 1; i++) {
      firstColumnChildren.add(HourLabel(hour: hour));
      hour = hour.add(Duration(minutes: 60));
    }
    rowChildren.add(Column(
      children: firstColumnChildren,
    ));
    for (int track in timetable.keys) {
      // Add single Column
      List<Widget> columnChildren = [];
      DateTime time = earliestStart;
      for (Entry e in timetable[track]!) {
        int gapMinutes = e.start.difference(time).inMinutes;
        if (gapMinutes > 0) {
          columnChildren.add(Space(length: gapMinutes));
        }
        columnChildren.add(e);
        time = e.start.add(Duration(minutes: e.length));
      }

      rowChildren.add(
        Expanded(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: columnChildren,
          ),
        ),
      );
    }
    MintY.currentColor = const Color.fromARGB(255, 255, 177, 51);
    return MaterialApp(
      title: "Programm - Tux-Tage 2023",
      home: MintYPage(
        title: "Tux-Tage 2023 - Programm",
        contentElements: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: rowChildren,
          ),
          FutureBuilder(
            future: reponse,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return Text(snapshot.data!.body);
              } else {
                return const MintYProgressIndicatorCircle();
              }
            },
          )
        ],
      ),
    );
  }
}
