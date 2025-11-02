import 'dart:convert';

import 'package:ems_timetable/entry.dart';
import 'package:http/http.dart' as http;
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';

/// If you paste new data, make sure to double the backslashes in the string.
String testData =
    '{"lectures": [{"id": 1, "event_id": 1, "presentator_id": 1, "attendant_id": null, "title": "Test", "description": " Test\\r\\n\\r\\nDas ist ein cooler Test", "target_group": "BE", "available_timeslots": "Samstag (11.11.);", "minimal_lecture_length": 10, "maximal_lecture_length": 10, "preferred_presentation_style": "RE", "qualification_for_lecture": "ich cool bin", "questions_during_lecture": false, "questions_after_lecture": false, "additional_information_by_presentator": "", "scheduled_in_room_id": 1, "scheduled_presentation_time": "2023-04-01T12:00:00", "scheduled_presentation_length": 20, "scheduled_presentation_style": "RE", "further_information": "", "related_website": "", "link_to_material": "", "link_to_recording": "", "custom_question_answers": "", "thumbnail": "Screenshot_20191021-102348_6jhOA4C.png", "presentator_name": "Jean Vogelbacher", "presentator_link": "https://www.linuxguides.de/", "presentator_organisation": "Linux Guides", "presentator_image": "/media/Screenshot_20190929-003143.png", "presentator_vita": "Ausbildung\\r\\n\\r\\n2015 - 2019: Master of Science in Informatik, Technische Universit\\u00e4t M\\u00fcnchen\\r\\n2012 - 2015: Bachelor of Science in Informatik, Technische Universit\\u00e4t M\\u00fcnchen\\r\\nBerufserfahrung\\r\\n\\r\\nSoftware Manager, [Unternehmen], M\\u00fcnchen, Deutschland\\r\\n2022 - heute\\r\\nF\\u00fchre ein Team von 10 Softwareentwicklern und -ingenieuren\\r\\nVerantworte die Entwicklung und den Betrieb einer Software-Plattform f\\u00fcr Kundenbeziehungsmanagement\\r\\nErziele eine j\\u00e4hrliche Wachstumsrate von 20\\r\\nSoftwareentwickler, [Unternehmen], M\\u00fcnchen, Deutschland\\r\\n2019 - 2022\\r\\nEntwickelte und implementierte neue Funktionen f\\u00fcr eine Software-Plattform f\\u00fcr E-Commerce\\r\\nArbeitete mit einem Team von 20 Softwareentwicklern zusammen\\r\\nErzielte eine Verbesserung der Performance um 15"}, {"id": 2, "event_id": 1, "presentator_id": 1, "attendant_id": null, "title": "Test 2", "description": " ", "target_group": "BE", "available_timeslots": "", "minimal_lecture_length": 10, "maximal_lecture_length": 10, "preferred_presentation_style": "RE", "qualification_for_lecture": " ", "questions_during_lecture": false, "questions_after_lecture": false, "additional_information_by_presentator": "", "scheduled_in_room_id": 1, "scheduled_presentation_time": "2023-04-01T12:30:00", "scheduled_presentation_length": 50, "scheduled_presentation_style": "RE", "further_information": "", "related_website": "", "link_to_material": "", "link_to_recording": "", "custom_question_answers": "", "thumbnail": "Screenshot_20200108-081724.png", "presentator_name": "Jean Vogelbacher", "presentator_link": "https://www.linuxguides.de/", "presentator_organisation": "Linux Guides", "presentator_image": "/media/Screenshot_20190929-003143.png", "presentator_vita": "Ausbildung\\r\\n\\r\\n2015 - 2019: Master of Science in Informatik, Technische Universit\\u00e4t M\\u00fcnchen\\r\\n2012 - 2015: Bachelor of Science in Informatik, Technische Universit\\u00e4t M\\u00fcnchen\\r\\nBerufserfahrung\\r\\n\\r\\nSoftware Manager, [Unternehmen], M\\u00fcnchen, Deutschland\\r\\n2022 - heute\\r\\nF\\u00fchre ein Team von 10 Softwareentwicklern und -ingenieuren\\r\\nVerantworte die Entwicklung und den Betrieb einer Software-Plattform f\\u00fcr Kundenbeziehungsmanagement\\r\\nErziele eine j\\u00e4hrliche Wachstumsrate von 20\\r\\nSoftwareentwickler, [Unternehmen], M\\u00fcnchen, Deutschland\\r\\n2019 - 2022\\r\\nEntwickelte und implementierte neue Funktionen f\\u00fcr eine Software-Plattform f\\u00fcr E-Commerce\\r\\nArbeitete mit einem Team von 20 Softwareentwicklern zusammen\\r\\nErzielte eine Verbesserung der Performance um 15"}]}';

class APIService {
  /// Returns a Map of timetables per day.
  /// A timetable is divided in tracks.
  static Future<Map<DateTime, Map<int, List<Entry>>>> getTimetableData() async {
    // For production:
    // String id = Uri.base.queryParameters["id"]!;
    // http.Response response = await http
    //     .get(Uri.parse('/events/api/$id/'))
    //     .timeout(const Duration(seconds: 5));
    // Map<String, dynamic> dataJson = jsonDecode(response.body);

    // For testing and running without backend:
    Map<String, dynamic> dataJson = jsonDecode(testData);

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
        vita: entryJson["presentator_vita"],
        thumbnailUrl: entryJson["thumbnail"],
        profilePictureUrl: entryJson["presentator_image"],
      );

      // Skip entries which aren't scheduled in any room.
      if (entry.track <= 0) {
        continue;
      }

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
