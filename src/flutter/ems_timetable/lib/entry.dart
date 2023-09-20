import 'dart:math';
import 'package:flutter/material.dart';
import 'package:ems_timetable/mintY.dart';
import 'package:flutter_widget_from_html/flutter_widget_from_html.dart';
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
  });

  @override
  Widget build(BuildContext context) {
    if (organisation.isNotEmpty) {
      presentator = "$presentator ($organisation)";
    }
    double height = length * 2 - 2;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 1, horizontal: 5),
      child: InkWell(
        onTap: () {
          // Entry Info
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
                          Expanded(
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
                                            style: MintY.heading1,
                                          ),
                                          SelectableText(
                                              "Beginn: ${DateFormat('kk:mm').format(start)} Uhr\t\tLänge: $length Minuten"),
                                          const SizedBox(height: 20),
                                        ],
                                      ),
                                    )
                                  ],
                                ),
                                HtmlWidget(
                                  description,
                                  onTapUrl: (url) =>
                                      js.context.callMethod('open', [url]),
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
                                                style: MintY.heading3,
                                              ),
                                              onPressed: () {
                                                js.context.callMethod('open',
                                                    [websiteOfPresentation]);
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
                                                style: MintY.heading3,
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
                                                style: MintY.heading3,
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
                                  padding: const EdgeInsets.symmetric(
                                      vertical: 32.0),
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
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          SelectableText(
                                            presentator,
                                            style: MintY.heading2,
                                          ),
                                          websiteOfAuthor == ""
                                              ? Container()
                                              : InkWell(
                                                  child: Text(
                                                    websiteOfAuthor,
                                                    style: MintY.heading4,
                                                  ),
                                                  onTap: () {
                                                    js.context.callMethod(
                                                        'open',
                                                        [websiteOfAuthor]);
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
                                  style: MintY.paragraph,
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
                                text: Text(
                                  "Schließen",
                                  style: MintY.heading3,
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
        },
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
}
