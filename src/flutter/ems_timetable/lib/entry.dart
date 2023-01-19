import 'package:flutter/cupertino.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ems_timetable/mintY.dart';

class Entry extends StatelessWidget {
  /// Minutes
  late int length;
  late String title;
  late int track;
  late DateTime start;
  Entry(
      {super.key,
      this.length = 10,
      this.title = "",
      this.track = 0,
      required this.start});

  @override
  Widget build(BuildContext context) {
    double height = length * 2 - 2;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 1, horizontal: 5),
      child: Container(

          /// -2: - Padding
          height: height,
          color: MintY.currentColor,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Flexible(
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 0),
                  child: Text(
                    title,
                    textAlign: TextAlign.center,
                    style: height > 20 ? MintY.heading4 : MintY.paragraph,
                    overflow: TextOverflow.clip,
                  ),
                ),
              ),
            ],
          )),
    );
  }
}
