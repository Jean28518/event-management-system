import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ems_timetable/mintY.dart';

class Entry extends StatelessWidget {
  /// Minutes
  late int length;
  late String title;
  late String presentator;
  late int track;
  late DateTime start;
  Entry(
      {super.key,
      this.length = 10,
      this.title = "",
      this.presentator = "",
      this.track = 0,
      required this.start});

  @override
  Widget build(BuildContext context) {
    double height = length * 2 - 2;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 1, horizontal: 5),
      child: Container(
          height: height,
          color: MintY.currentColor,
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
                        title,
                        textAlign: TextAlign.center,
                        style: height > 20
                            ? MintY.heading4White
                            : MintY.paragraphWhite,
                        overflow: TextOverflow.clip,
                      ),
                    ),
                  ],
                ),
              ),
              Flexible(
                child: Text(
                  presentator,
                  textAlign: TextAlign.center,
                  style: MintY.paragraphWhite,
                  overflow: TextOverflow.clip,
                ),
              ),
            ],
          )),
    );
  }
}
