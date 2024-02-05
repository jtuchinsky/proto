# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import google.protobuf.descriptor_pb2 as pb2

def read_descriptor_file(descriptor_file_path):
    with open(descriptor_file_path, 'rb') as file:
        data = file.read()
    return data

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    print_proto_desc()


def print_proto_desc():
    global message_type, field
    descriptor_data = read_descriptor_file('person.desc')
    file_descriptor_set = pb2.FileDescriptorSet()
    file_descriptor_set.ParseFromString(descriptor_data)
    for file_descriptor in file_descriptor_set.file:
        print(f"File: {file_descriptor.name}")
        for message_type in file_descriptor.message_type:
            print(f"  Message: {message_type.name}")
            for field in message_type.field:
                print(f"    Field: {field.name} ({field.type_name})")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
