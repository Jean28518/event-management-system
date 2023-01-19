import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class Space extends StatelessWidget {
  /// Minutes
  late int length;
  Space({super.key, required this.length});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: length * 2,
    );
  }
}
