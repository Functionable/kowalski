func = """| %s%s%s( %s )  |
| ------------------- |
| %s |"""

constant = """| %s%s%s <span style="float: right;">Constant: %s</span> |
| ------------------- |
| %s |"""


prop = """| **%s** %s |
| --------------------- |
| %s     |"""

evnt = """| %s( %s ) |
| -------------------------- |
| %s |"""

markdown_title = """---
title: %s
summary: %s
---
"""

def document_arguments(arguments_array):
    documented_string = ""

    should_comma = False
    for argument in arguments_array:
        if should_comma:
            documented_string += ", "

        if argument["type"] and argument["name"]:
            documented_string += "**" + argument["type"] + "** " + argument["name"] 

        should_comma = True

    return documented_string

def document_return(return_type):
    if return_type:
        return "**" + return_type + "** "

    return return_type

def document_function(function, function_name):
    return func % (document_return(function["returns"]), "", function_name, document_arguments(function["arguments"]), function["description"]) + "\n\n"

def document_constant(constant_value, constant_name):
    return constant % ("", "", constant_name, constant_value["constant"], constant_value["description"]) + "\n\n"

def document_enum(constant_value, constant_name):
    return constant % ("", "", constant_name, constant_value["value"], constant_value["description"]) + "\n\n"

def document_event(event, event_name):
    return evnt % (event_name, document_arguments(event["arguments"]), event["description"]) + "\n\n"

def document_event_empty(event, event_name):
    return evnt % (event_name, document_arguments(event["arguments"]), " ") + "\n\n"


def save_library(library_name, library_path, library_data):
    class_text = (markdown_title % (library_name + " Library", library_name + " Library")) + "\n\n"
    class_text += library_data["description"] + "\n\n"
    for key, data in sorted(library_data.items()):
        if key == "description": continue
        if "constant" in data.keys():
            class_text += document_constant(data, key)
            continue

        class_text += document_function(data, key) + "\n\n"

    file_out = open(library_path, "w")
    file_out.write(class_text)
    file_out.close()

def get_enum_value(enum_data):
    return int(enum_data["value"])

def save_enum(enum_name, enum_path, enum_data):
    #pass
    #print("Enum Name: %s @ '%s'" % (enum_name, enum_path) )

    #for k, v in enum_data.items():
    #    print(str(k) + ": " + str(v))

    enum_text = (markdown_title % (enum_name, "An enum")) + "\n\n"
    enum_text += enum_data["description"] + "\n\n"

    for key, data in sorted(enum_data["values"].items()):
        enum_text += document_enum(data, key)

    file_out = open(enum_path, "w")
    file_out.write(enum_text)
    file_out.close()


def save_event(event_name, event_path, event_data):
    event_text = (markdown_title % (event_name , "A global event")) + "\n\n"
    event_text += event_data["description"] + "\n\n"

    event_text += document_event_empty(event_data, event_name)

    file_out = open(event_path, "w")
    file_out.write(event_text)
    file_out.close()
    