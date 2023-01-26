import 'dart:convert';

import 'package:ems_timetable/entry.dart';
import 'package:http/http.dart' as http;

class APIService {
  /// Returns a Map of timetables per day.
  /// A timetable is divided in tracks.
  static Future<Map<DateTime, Map<int, List<Entry>>>> getTimetableData() async {
    String id = Uri.base.queryParameters["id"]!;
    http.Response response = await http
        .get(Uri.parse('/events/api/$id/'))
        .timeout(Duration(seconds: 5));
    Map<String, dynamic> dataJson = jsonDecode(response.body);
    Map<DateTime, Map<int, List<Entry>>> returnValue = {};
    for (Map<String, dynamic> entryJson in dataJson["lectures"]) {
      Entry entry = Entry(
        start: DateTime.parse(entryJson["scheduled_presentation_time"]),
        track: entryJson["scheduled_in_room_id"],
        title: entryJson["title"],
        presentator: entryJson["presentator_name"],
        length: entryJson["scheduled_presentation_length"],
      );

      // Add day to map if not existent
      DateTime day =
          DateTime(entry.start.year, entry.start.month, entry.start.day);
      if (!returnValue.containsKey(day)) {
        returnValue[day] = {};
        returnValue[day]![-1] = [];
      }
      // Add entry to timetable map
      returnValue[day]![-1]!.add(entry);

      // entries.add(entry);
    }

    for (DateTime currentDay in returnValue.keys) {
      List<Entry> entries = returnValue[currentDay]![-1]!;
      Map<int, List<Entry>> timetableForDay = {};

      for (Entry e in entries) {
        if (!timetableForDay.keys.contains(e.track)) {
          timetableForDay[e.track] = [];
        }

        timetableForDay[e.track]!.add(e);
      }
      for (int track in timetableForDay.keys) {
        timetableForDay[track]!.sort(((a, b) => a.start.compareTo(b.start)));
      }
      returnValue[currentDay] = timetableForDay;
    }

    return returnValue;
  }
}
