import 'dart:math';
import 'package:flutter/material.dart';
import 'package:ems_timetable/mintY.dart';
import 'dart:js' as js;
import 'package:intl/intl.dart';

class Entry extends StatelessWidget {
  /// Minutes
  late int length;
  late String title;
  late String presentator;
  late int track;
  late DateTime start;
  late String description;
  late String websiteOfAuthor;
  late String organisation;
  late String websiteOfPresentation;
  late String linkToMaterial;
  late String linkToRecording;
  late String vita;
  late String thumbnailUrl;
  late String profilePictureUrl;
  bool displayError = false;
  Entry({
    super.key,
    this.length = 10,
    this.title = "",
    this.presentator = "",
    this.track = 0,
    required this.start,
    this.websiteOfAuthor = "",
    this.organisation = "",
    this.description = "",
    this.websiteOfPresentation = "",
    this.linkToMaterial = "",
    this.linkToRecording = "",
    this.vita = "",
    this.thumbnailUrl = "",
    this.profilePictureUrl = "",
  }) {
    if (organisation.isNotEmpty) {
      presentator = "$presentator ($organisation)";
    }
  }

  @override
  Widget build(BuildContext context) {
    double height = length * 2 - 2;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 1, horizontal: 5),
      child: InkWell(
        // onDoubleTap: () => show_info_dialog(context),
        onTap: () => show_info_dialog(context),
        // onLongPress: () => show_info_dialog(context),
        // onSecondaryTap: () => show_info_dialog(context),
        // Entry Card
        child: Container(
            // rouded corners
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: displayError ? Colors.red : MintY.currentColor,
            ),
            height: height,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Flexible(
                        child: Text(
                          height > 40 ? title : "$title - $presentator",
                          textAlign: TextAlign.center,
                          style: height > 40 ? MintY.heading4 : MintY.paragraph,
                          overflow: TextOverflow.clip,
                        ),
                      ),
                    ],
                  ),
                ),
                height > 40
                    ? Flexible(
                        child: Text(
                          presentator,
                          textAlign: TextAlign.center,
                          style: MintY.paragraph,
                          overflow: TextOverflow.clip,
                        ),
                      )
                    : Container(),
              ],
            )),
      ),
    );
  }

  void show_info_dialog(context) {
    showDialog(
        context: context,
        builder: (context) {
          double width = MediaQuery.of(context).size.width;
          double horizontalPadding = max((width - 1000) / 2, 0) + 16;
          return Padding(
            padding: EdgeInsets.symmetric(
                horizontal: horizontalPadding, vertical: 32),
            child: Dialog(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SizedBox(
                      height: min(
                          500 + description.length / 10 + vita.length / 10,
                          MediaQuery.of(context).size.height - 200),
                      child: ListView(
                        children: [
                          Row(
                            children: [
                              thumbnailUrl == ""
                                  ? Container()
                                  : Padding(
                                      padding: const EdgeInsets.all(8.0),
                                      child: Image.network(
                                        "/media/$thumbnailUrl",
                                        height: 200,
                                      ),
                                    ),
                              Expanded(
                                child: Column(
                                  children: [
                                    SelectableText(
                                      title,
                                      style: MintY.heading1White,
                                    ),
                                    SelectableText(
                                        "Beginn: ${DateFormat('kk:mm').format(start)} Uhr\t\tLänge: $length Minuten"),
                                    const SizedBox(height: 20),
                                  ],
                                ),
                              )
                            ],
                          ),
                          SelectableText(
                            description,
                            style: MintY.paragraphWhite,
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              websiteOfPresentation == ""
                                  ? Container()
                                  : Padding(
                                      padding: const EdgeInsets.all(8.0),
                                      child: MintYButton(
                                        text: const Text(
                                          "Webseite",
                                          style: MintY.heading3White,
                                        ),
                                        onPressed: () {
                                          js.context.callMethod(
                                              'open', [websiteOfPresentation]);
                                        },
                                      ),
                                    ),
                              linkToMaterial == ""
                                  ? Container()
                                  : Padding(
                                      padding: const EdgeInsets.all(8.0),
                                      child: MintYButton(
                                        text: const Text(
                                          "Material",
                                          style: MintY.heading3White,
                                        ),
                                        onPressed: () {
                                          js.context.callMethod(
                                              'open', [linkToMaterial]);
                                        },
                                      ),
                                    ),
                              linkToRecording == ""
                                  ? Container()
                                  : Padding(
                                      padding: const EdgeInsets.all(8.0),
                                      child: MintYButton(
                                        text: const Text(
                                          "Aufzeichnung",
                                          style: MintY.heading3White,
                                        ),
                                        onPressed: () {
                                          js.context.callMethod(
                                              'open', [linkToRecording]);
                                        },
                                      ),
                                    ),
                            ],
                          ),
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 32.0),
                            child: Container(
                              height: 1,
                              color: Colors.grey[300],
                            ),
                          ),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              profilePictureUrl == ""
                                  ? Container()
                                  : Image.network(
                                      profilePictureUrl,
                                      height: 200,
                                    ),
                              Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    SelectableText(
                                      presentator,
                                      style: MintY.heading2White,
                                    ),
                                    websiteOfAuthor == ""
                                        ? Container()
                                        : InkWell(
                                            child: Text(
                                              websiteOfAuthor,
                                              style: MintY.heading4White,
                                            ),
                                            onTap: () {
                                              js.context.callMethod(
                                                  'open', [websiteOfAuthor]);
                                            },
                                          ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 20),
                          SelectableText(
                            vita,
                            style: MintY.paragraphWhite,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        MintYButton(
                          color: MintY.currentColor,
                          text: const Text(
                            "Schließen",
                            style: MintY.heading3White,
                          ),
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                        ),
                      ],
                    )
                  ],
                ),
              ),
            ),
          );
        });
  }
}
