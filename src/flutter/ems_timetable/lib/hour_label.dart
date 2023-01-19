import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class HourLabel extends StatelessWidget {
  late DateTime hour;
  HourLabel({super.key, required this.hour});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 60 * 2,
      child: Column(
        children: [
          Container(
            height: 1,
            width: 100,
            color: Colors.black,
          ),
          const SizedBox(
            height: 2,
          ),
          Text("${hour.hour.toString()}:00 Uhr"),
        ],
      ),
    );
  }
}
