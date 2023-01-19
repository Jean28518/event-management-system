git clone https://github.com/flutter/flutter.git -b stable
PATH="$PATH:`pwd`/flutter/bin"
flutter doctor
cd src/flutter/ems_timetable/
flutter build web --base-href "/static/ems_timetable/"
cp -r build/web ../../event_management_system/static/ems_timetable