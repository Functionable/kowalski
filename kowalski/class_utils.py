from .doc_utils import *

def save_class(class_name, path, blur_class):
    class_text = ""
    class_text += (markdown_title % (class_name, "A BlurLua class")) + "\n\n"
    class_text += blur_class["description"] + "\n\n"
    if( len(blur_class["properties"]) > 0 ):
        class_text += "## Properties\n"
        for key, data in blur_class["properties"].items():
            class_text += prop % (data["type"], key, data["description"]) + "\n\n"

    if( len(blur_class["functions"]) > 0 ):
        class_text += "## Functions\n"
        for key, data in blur_class["functions"].items():
            class_text += document_function(data, class_name + ":" + key) + "\n\n"

    if( len(blur_class["events"]) > 0 ):
        class_text += "## Events\n"
        for key, data in blur_class["events"].items():
            class_text += document_event(data, key) + "\n\n"


    file_out = open(path, "w")
    file_out.write(class_text)
    file_out.close()