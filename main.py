# This is a sample Python script.
import dataclasses

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
    node = create_tree()
    myFunc(node)
    print_proto_desc()


def print_proto_desc():
    # global message_type, field
    descriptor_data = read_descriptor_file('person.desc')
    file_descriptor_set = pb2.FileDescriptorSet()
    file_descriptor_set.ParseFromString(descriptor_data)
    for file_descriptor in file_descriptor_set.file:
        print(f"File: {file_descriptor.name}")
        for enum_type in file_descriptor.enum_type:
            print(f"  Enum: {enum_type.name}")
            for value in enum_type.value:
                print(f"    Value: {value.name} ({value.number})")
        for message_type in file_descriptor.message_type:
            print(f"  Message: {message_type.name}")
            for nested_type in message_type.nested_type:
                print(f"    Nested Message: {nested_type.name}")
            for enum_type in message_type.enum_type:
                print(f"    Enum: {enum_type.name}")
                for value in enum_type.value:
                    print(f"      Value: {value.name} ({value.number})")
            for oneof_decl in message_type.oneof_decl:
                print(f"    Oneof: {oneof_decl.name}")
            for field in message_type.field:
                print(f"    Field: {field.name} ({field.type_name})")


@dataclasses.dataclass
class Node:
    name: str
    type: str
    children: list

def create_tree():
    node1 = Node('node1', 'type1', [])
    node2 = Node('node2', 'type2', [])
    node3 = Node('node3', 'type3', [])
    node4 = Node('node4', 'type4', [])
    node5 = Node('node5', 'type5', [])
    node6 = Node('node6', 'type6', [])
    node7 = Node('node7', 'type7', [])
    node8 = Node('node8', 'type8', [])
    node1.children = [node2, node3]
    node2.children = [node4, node5]
    node3.children = [node6, node7]
    node4.children = [node8]
    return node1

def myFunc(node:Node):
    print(node.name)
    for child in node.children:
        myFunc(child)
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
