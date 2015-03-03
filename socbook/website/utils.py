from json import dumps


def form_fields_to_json(form):
    fields = []
    for field in form.visible_fields():
        if field.help_text:
            field_selector = "input[id=\"{0}\"]".format(field.id_for_label)
            field = {'selector': field_selector, 'help_text': field.help_text}
            fields.append(field)
    return dumps(fields)
