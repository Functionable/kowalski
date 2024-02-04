from kowalski.doc_utils import *
from kowalski.class_utils import *
import colorama
import json
import os
import re

enums = {
    "BLF": "BLF_.*",
    "Log": "LOG_.*",
    "Texture Mode": "TEXTUREMODE_.*",
    "Alignment": "ALIGN_.*",
    "Key": "KEY_.*"
}

test = """---
title: %s
summary: %s
---

%s

"""

global_desc = """This page documents all functions present directly in _G.
It does not document any libraries which are available in another section.
"""

total_warns = 0

collected_enums = {}

for key in enums.keys():
    enums[key] = re.compile(enums[key])
    collected_enums[key] = {}

def warn(text):
    global total_warns
    print(colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL)
    total_warns += 1

def read_all(path):
    with open(path, "r") as handle:
        return handle.read()

def write_all(path, data):
    with open(path, "w") as handle:
        return handle.write(data)

def readJSON(file):
    file_handle = open(file, "r")
    file_content = file_handle.read()
    file_handle.close()
    return json.loads(file_content)
    
def writeJSON(file, data):
    file_handle = open(file, "w")
    file_handle.write(json.dumps(data))
    file_handle.close()

sample_function = {
    "description": "This is a sample description.",
    "arguments": [{
        "name": "",
        "type": ""
    }],
    "returns": ""
}

sample_event = {
    "description": "This is a sample event description.",
    "arguments": [{
        "name": "",
        "type": ""
    }]
}

sample_property = {
    "type": "",
    "description": "This is a sample property description",
}

sample_enum_value = {
    "name": "",
    "value": "",
    "description": "This is a sample enum description",
}

sample_enum = {
    "name": "",
    "description": "This is a sample enum description",

    "values": []
}

sample_class_description = "This is a sample class description"
sample_library_description = "This is a sample library description"
sample_event_description = "This is a sample event description."
sample_enum_description = "This is a sample enum description"

documented_globals = readJSON("global-functions.json")
documented_classes = {}
documented_libraries = {}
documented_events = {}
documented_enums = {}

test_str = ""

test_str += (test % ("Global Functions", "All Globals", global_desc))

report_data = readJSON("report.json")
#documented_events = report_data["_events"]
#documented_enums = report_data["_enums"]
for (key, data) in sorted(report_data["globals"].items()):
    if data == "function":
        if key not in documented_globals:
            documented_globals[key] = {
                "description": "This is a sample description.",
                "arguments": [{
                    "name": "",
                    "type": ""
                }],
                "returns": ""
            }

        test_str += document_function(documented_globals[key], key)

    #elif type(data) == int:
    #    for (enum_key, enum_regex) in enums.items():
    #        if( enum_regex.match(key) ):
    #            collected_enums[enum_key][key] = data
    elif key == "_events":
        for event_name in data:
            if( os.path.exists("docs/event_%s.json" % event_name)):
                documented_events[event_name] = readJSON("docs/event_%s.json" % event_name)
                #if "description" in documented_events[key]:
            else:
                documented_events[event_name] = {
                    "description": "This is a sample event description.",
                    "arguments": [{
                        "name": "",
                        "type": ""
                    }]
                }
                print("Creating '%sdocs/event_%s.json%s'..." % (colorama.Fore.BLUE, event_name, colorama.Style.RESET_ALL))

            writeJSON("docs/event_%s.json" % event_name, documented_events[event_name] )
    elif key == "_enums":
        for enum_name, enum_data in data.items():
            if os.path.exists("docs/enum_%s.json" % enum_name):
                documented_enums[enum_name] = readJSON("docs/enum_%s.json" % enum_name)

                for enum_val_name, enum_val_value in sorted(enum_data.items()):
                    if enum_val_name not in documented_enums[enum_name]["values"]:
                        val_data = {
                            "value": "",
                            "description": "This is a sample enum description",
                        }
                        val_data["value"] = enum_val_value
                        documented_enums[enum_name]["values"][enum_val_name] = val_data

            else:
                documented_enums[enum_name] = {
                    "description": "This is a sample enum description",

                    "values": {}
                }

                for enum_val_name, enum_val_value in sorted(enum_data.items()):
                    val_data = {
                        "value": "",
                        "description": "This is a sample enum description",
                    }
                    #val_data["name"] = enum_val_name
                    val_data["value"] = enum_val_value

                    documented_enums[enum_name]["values"][enum_val_name] = (val_data)
                    print("Creating '%sdocs/enum_%s.json%s'..." % (colorama.Fore.BLUE, enum_name, colorama.Style.RESET_ALL))

            writeJSON("docs/enum_%s.json" % enum_name, documented_enums[enum_name] )
           # print(json.dumps(documented_enums[enum_name]))

    elif type(data) == dict and key[0] != '_':
        if( os.path.exists("docs/lib_%s.json" % key) ):
            documented_libraries[key] = readJSON("docs/lib_%s.json" % key)
        else:
            documented_libraries[key] = {}
            print("Creating '%sdocs/lib_%s.json%s'..." % (colorama.Fore.BLUE, key, colorama.Style.RESET_ALL))

        function_list = [key for key, value in data.items() if value == "function"]
        constant_list = [key for key, value in data.items() if type(value) == str and value != "function" and key != "TypeName" ]
        library_description = sample_library_description
        if "description" in documented_libraries[key]:
            library_description = documented_libraries[key]["description"]

        documented_libraries[key] = {function_key: (sample_function if function_key not in documented_libraries[key] else documented_libraries[key][function_key]) for function_key in (function_list + constant_list)}
        documented_libraries[key]["description"] = library_description

        for constant in constant_list:
            if constant in documented_libraries[key].keys():
                documented_libraries[key][constant]["constant"] = data[constant]
            else:
                documented_libraries[key][constant] = dict(sample_function)
                documented_libraries[key][constant]["description"] = sample_function["description"]
                documented_libraries[key][constant]["constant"] = data[constant]

        writeJSON("docs/lib_%s.json" % key, documented_libraries[key])

for key, data in report_data["classes"].items():
    if( os.path.exists("docs/class_%s.json" % key)):
        documented_classes[key] = readJSON("docs/class_%s.json" % key)
    else:
        print("Creating '%sdocs/class_%s.json%s'..." % (colorama.Fore.BLUE, key, colorama.Style.RESET_ALL))
        documented_classes[key] = {}
        documented_classes[key]["properties"] = {}
        documented_classes[key]["functions"] = {}

    if "events" not in documented_classes[key]:
        documented_classes[key]["events"] = {}

    function_list = [function_key for function_key, function_value in data.items() if function_key[:2] != "__" and function_value == "function"]
    property_list = []
    events_list   = []
    if "__getters" in data:
        property_list = [property_key for property_key in data["__getters"].keys()]
    if "__getters" in data and "__setters" in data:
        events_list = [event_key for event_key in data["__setters"].keys() if event_key not in data["__getters"]]

    documented_classes[key]["properties"] = {property_key: (sample_property if property_key not in documented_classes[key]["properties"]  else documented_classes[key]["properties"][property_key]) for property_key in property_list}
    documented_classes[key]["functions"] = {function_key: (sample_function if function_key not in documented_classes[key]["functions"]  else documented_classes[key]["functions"][function_key]) for function_key in function_list}
    documented_classes[key]["events"] = {event_key: (sample_event if event_key not in documented_classes[key]["events"]  else documented_classes[key]["events"][event_key]) for event_key in events_list}
    if "description" not in documented_classes[key]:
        documented_classes[key]["description"] = sample_class_description
    
    writeJSON("docs/class_%s.json" % key, documented_classes[key])
    
for (key, data) in documented_globals.items():
    if key not in report_data["globals"]:
        warn("[W]: Global Function '%s' not present in report. Function no longer exists?" % (key))

file_handle = open("out/globals.md", "w")
file_handle.write(test_str)
file_handle.close()

file_handle = open("global-functions.json", "w")
file_handle.write(json.dumps(documented_globals))
file_handle.close()

documentable_units = 0 
documented_units = 0
undocumented_global_count = 0
documented_global_max   = 0
for (key, data) in documented_globals.items():
    documented_global_max += 1
    documentable_units += 1
    if( data["description"] == sample_function["description"] ):
        undocumented_global_count += 1

if( undocumented_global_count > 0):
    warn("[W]: %d global functions left undocumented." % undocumented_global_count)   
    warn("  - " + "[" + ", ".join([key for key, data in documented_globals.items() if data["description"] == sample_function["description"]]) + "]")

documented_units = documented_global_max - undocumented_global_count

for (key, data) in (documented_libraries.items()):
    library_undocumented = 0
    library_undocumented_list = []
    library_documentable = 0
    for function_key, function_value in data.items():
        ##if function_key == "constant": continue

        if function_key == "description":
            library_documentable += 1
            if function_value == sample_library_description:
                library_undocumented += 1
            continue

        library_documentable += 1
        if( function_value["description"] == sample_function["description"]):
            library_undocumented += 1
            library_undocumented_list.append(function_key)

    documentable_units += library_documentable
    documented_units   += (library_documentable - library_undocumented)

    if( library_undocumented > 0 ):
        warn("[W]: %d doc-units undocumented in library '%s'\n  - [%s]" % (library_undocumented, key, ", ".join(library_undocumented_list)))
        if data["description"] == sample_library_description:
            warn("  - description")

for key, data in documented_events.items():
    documentable_units += 1
    undocumented = 0
    if data["description"] != sample_event_description:
        documented_units += 1
    else:
        undocumented += 1

    if len(data["arguments"]) == 1:
        documentable_units += 1
        if not data["arguments"][0]["name"]:
            undocumented += 1
        else:
            documented_units += 1

    if undocumented > 0:
        warn("[W]: %d doc-units undocumented in event '%s'" % (undocumented, key))

for key, data in documented_enums.items():
    undocumented = 0
    documentable_units += 1
    if data["description"] != sample_enum_description:
        documented_units += 1
    else:
        undocumented += 1

    for enum_key, enum_value in data["values"].items():
        documentable_units += 1
        if enum_value["description"] != sample_enum_description:
            documented_units += 1
        else:
            undocumented += 1

    if undocumented > 0:
        warn("[W]: %d doc-units undocumented in enum '%s'" % (undocumented, key))
        warn("  - [" + ", ".join([key for key, value in data["values"].items() if value["description"] == sample_enum_description]) + "]")
        if data["description"] == sample_enum_description:
            warn("  - description")

for key, data in documented_classes.items():
    class_undocumented = 0
    class_undocumented_dict = {"properties": [], "functions": [], "events": []}
    class_documentable = 1
    if data["description"] == sample_class_description:
        class_undocumented += 1

    for function_key, function_value in data["functions"].items():
        class_documentable += 1
        if( function_value["description"] == sample_function["description"]):
            class_undocumented += 1
            class_undocumented_dict["functions"].append(function_key)

    for property_key, property_value in data["properties"].items():
        class_documentable += 1
        if property_value["description"] == sample_property["description"]:
            class_undocumented += 1
            class_undocumented_dict["properties"].append(property_key)

    for event_key, event_value in data["events"].items():
        class_documentable += 1
        if event_value["description"] == sample_event["description"]:
            class_undocumented += 1
            class_undocumented_dict["events"].append(event_key)

    documentable_units += class_documentable
    documented_units += (class_documentable - class_undocumented)

    if class_undocumented > 0:
        warn("[W] %d doc-units undocumented in class '%s'" % (class_undocumented, key))
        if len(class_undocumented_dict["functions"]) > 0:
            warn("  - Functions: [%s]" % ", ".join(class_undocumented_dict["functions"]))
        if len(class_undocumented_dict["properties"]) > 0:
            warn("  - Properties: [%s]" % ", ".join(class_undocumented_dict["properties"]))
        if len(class_undocumented_dict["events"]) > 0:
            warn("  - Events: [%s]" % ", ".join(class_undocumented_dict["events"]))

warn("[W]: %d/%d (%f%%) doc-units documented" % (documented_units, documentable_units, (100*documented_units/documentable_units)))

print("Producing new mkdocs.yml...")

mkdocs_content = read_all("mkdocs.yml")
replace_index = mkdocs_content.index("%%MKDOCS_SUB%%")  -1
char = mkdocs_content[replace_index]
prefix = ""
while char != '\n':
    prefix += char
    replace_index -= 1
    char = mkdocs_content[replace_index]

replace_content = "- \"Classes\": "
for key, data in sorted(documented_classes.items()):
    replace_content += "\n%s    - \"%s\": api-reference/classes/class_%s.md" % (prefix, key, key)
replace_content += "\n%s- \"Libraries\": " % prefix
for key, data in sorted(documented_libraries.items()):
    replace_content += "\n%s    - \"%s\": api-reference/libraries/library_%s.md" % (prefix, key, key)
replace_content += "\n%s- \"Enums\": " % prefix
for key, data in sorted(documented_enums.items()):
    replace_content += "\n%s    - \"%s\": api-reference/enums/enum_%s.md" % (prefix, key, key)
replace_content += "\n%s- \"Global Events\": " % prefix
for key, data in sorted(documented_events.items()):
    replace_content += "\n%s    - \"%s\": api-reference/events/event_%s.md" % (prefix, key, key)


mkdocs_content = mkdocs_content.replace("%%MKDOCS_SUB%%", replace_content)
write_all("out/mkdocs.yml", mkdocs_content)

print("Finished successfully with %d warnings" % total_warns)

for key, data in documented_classes.items():
    save_class(key, "out/classes/class_%s.md" % key, data)

for key, data in documented_libraries.items():
    save_library(key, "out/libraries/library_%s.md" % key, data)

for key, data in documented_enums.items():
    save_enum(key, "out/enums/enum_%s.md" % key, data)

for key, data in documented_events.items():
    save_event(key, "out/events/event_%s.md" % key, data)

write_all("testtttt.json", json.dumps(documented_enums))