import 'package:ems_timetable/api_service.dart';
import 'package:ems_timetable/entry.dart';
import 'package:ems_timetable/mintY.dart';
import 'package:ems_timetable/timetable_one_day.dart';
import 'package:flutter/cupertino.dart';
import 'package:intl/intl.dart';

class Timetable extends StatelessWidget {
  final Future<Map<DateTime, Map<int, List<Entry>>>> timetableDataFuture =
      APIService.getTimetableData();
  Timetable({super.key});

  @override
  Widget build(BuildContext context) {
    // return MintYPage(title: "Test");
    return FutureBuilder(
      future: timetableDataFuture,
      builder: (context, snapshot) {
        if (snapshot.hasData && !snapshot.hasError) {
          List<Widget> contentElements = [];
          for (DateTime day in snapshot.data!.keys) {
            Map<int, List<Entry>> timetable = snapshot.data![day]!;
            contentElements.add(Text(
              DateFormat('EEEE, d. MMMM yyyy', 'de_DE').format(day),
              style: MintY.heading1,
              textAlign: TextAlign.center,
            ));
            contentElements
                .add(TimetableOneDay(day: day, timetable: timetable));
          }
          return MintYPage(
            contentElements: contentElements,
          );
        } else if (snapshot.hasError) {
          return MintYPage(
            customContentElement: Text(snapshot.error.toString()),
          );
        } else {
          return MintYPage(
            customContentElement: const MintYProgressIndicatorCircle(),
          );
        }
      },
    );
  }
}
