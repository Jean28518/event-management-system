import 'dart:convert';

import 'package:ems_timetable/entry.dart';
import 'package:http/http.dart' as http;
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';

class APIService {
  /// Returns a Map of timetables per day.
  /// A timetable is divided in tracks.
  static Future<Map<DateTime, Map<int, List<Entry>>>> getTimetableData() async {
    // await initializeDateFormatting('de_DE', null);

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
        description: entryJson["description"],
        websiteOfAuthor: entryJson["presentator_link"],
        organisation: entryJson["presentator_organisation"],
        websiteOfPresentation: entryJson["related_website"],
        linkToMaterial: entryJson["link_to_material"],
        linkToRecording: entryJson["link_to_recording"],
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
      // Sort rooms
      timetableForDay = Map.fromEntries(timetableForDay.entries.toList()
        ..sort((e1, e2) => e1.key.compareTo(e2.key)));
      returnValue[currentDay] = timetableForDay;
    }

    // Sort days
    returnValue = Map.fromEntries(returnValue.entries.toList()
      ..sort((e1, e2) => e1.key.compareTo(e2.key)));

    return returnValue;
  }
}
