from event_management_system.meta import meta

def string_disabled_entries2field_activation_entries(string):
    disabled_entries = string.split(";")
    field_activation_entries = []

    for lecture_field in _get_fields_lecture():
        field_activation_entry = {"id": lecture_field}
        if lecture_field in disabled_entries:
            field_activation_entry["checked"] = False
        else:
            field_activation_entry["checked"] = True
        field_activation_entries.append(field_activation_entry)

    return field_activation_entries

def post_answer2string_disabled_entries(request):
    string = ""
    for lecture_field in _get_fields_lecture():
        if not f"field_{lecture_field}" in request.POST.keys():
            string += f"{lecture_field};"
    return string

def _get_fields_lecture():
    fields = meta.get_fields_lecture()
    fields_2 = []
    for field in fields:
        field = field.replace("$lecture.", "")
        fields_2 .append(field)
    fields = fields_2
    fields.remove("id")
    fields.remove("event_id")
    fields.remove("presentator_id")
    fields.remove("custom_question_answers")
    fields.remove("available_timeslots")
    return fields