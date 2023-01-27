import 'package:ems_timetable/entry.dart';
import 'package:ems_timetable/hour_label.dart';
import 'package:ems_timetable/space.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class TimetableEMS extends StatelessWidget {
  late DateTime day;
  late Map<int, List<Entry>> timetable;
  TimetableEMS({super.key, required this.day, required this.timetable});

  @override
  Widget build(BuildContext context) {
    DateTime earliestStart = timetable[timetable.keys.first]![0].start;
    DateTime latestTime = timetable[timetable.keys.first]![0].start;
    for (int i in timetable.keys) {
      List<Entry> entries = timetable[i]!;
      for (Entry e in entries) {
        if (e.start.compareTo(earliestStart) < 0) {
          earliestStart = e.start;
        }
        DateTime eEnd = e.start.add(Duration(minutes: e.length));
        if (eEnd.compareTo(latestTime) > 0) {
          latestTime = eEnd;
        }
      }
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
      // We start always at XX:00
      DateTime time =
          earliestStart.subtract(Duration(minutes: earliestStart.minute));
      bool error = false;
      for (Entry e in timetable[track]!) {
        int gapMinutes = e.start.difference(time).inMinutes;
        if (gapMinutes > 0) {
          columnChildren.add(Space(length: gapMinutes));
        } else if (gapMinutes.isNegative) {
          error = true;
        }
        e.displayError = error;
        columnChildren.add(e);
        time = e.start.add(Duration(minutes: e.length));
        // print("Added ${e.title}");
      }
      // print(columnChildren.length);
      rowChildren.add(
        Expanded(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: columnChildren,
          ),
        ),
      );
    }
    // print(rowChildren.length);
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: rowChildren,
    );
  }
}
