import dataclasses
import itertools
from enum import Enum
import google.protobuf.descriptor_pb2 as pb2

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

class NodeType(Enum):
    FILE = 'File'
    PACKAGE = 'Package'
    ENUM = 'Enum'
    ENUM_VALUE = 'EnumValue'
    MESSAGE = 'Message'
    FIELD = 'Field'
    ONEOF = 'Oneof'
    ROOT = 'Root'


@dataclasses.dataclass
class Node:
    name: str
    type: str
    # package: str
    # filename: str
    children: list  # List['Node']
    parent: 'Node' = None

    def add_node(self, node: 'Node'):
        self.children.append(node)
        node.parent = self
        return node

    def __str__(self):
        if self.parent:
            return f"Name: {self.name} Type: {self.type} Children: {len(self.children)} Parent: {self.parent.name}"
        else:
            return f"Name: {self.name} Type: {self.type} Children: {len(self.children)} Parent: None"


    def print_tree(self, root, markerStr="+- ", levelMarkers=[]):
        emptyStr = " " * len(markerStr)

        connectionStr = "|" + emptyStr[:-1]
        level = len(levelMarkers)  # recursion level
        mapper = lambda draw: connectionStr if draw else emptyStr
        markers = "".join(map(mapper, levelMarkers[:-1]))
        markers += markerStr if level > 0 else ""
        print(f"{markers}{root.name} ({root.type})")
        # After root has been printed, recurse down (depth-first) the child nodes.
        for i, child in enumerate(root.children):
            # The last child will not need connection markers on the current level
            # (see example above)
            isLast = i == len(root.children) - 1
            self.print_tree(child, markerStr, [*levelMarkers, not isLast])

def traverse(parent: Node, descriptor):
    print(f"Parent: {parent.name} Node: {descriptor.name}")

    if isinstance(descriptor, pb2.FileDescriptorProto):
        file_node = Node(descriptor.name, NodeType.FILE, [], parent)
        yield parent.add_node(file_node)
        yield file_node.add_node(Node(descriptor.package, NodeType.PACKAGE, [], file_node))

        for item in itertools.chain(descriptor.enum_type, descriptor.message_type):
            yield from traverse(file_node, item)

    elif isinstance(descriptor, pb2.EnumDescriptorProto):
        enum_node = parent.add_node(Node(descriptor.name, NodeType.ENUM, [], parent))
        yield enum_node
        for item in descriptor.value:
            yield from traverse(enum_node, item)

    elif isinstance(descriptor, pb2.EnumValueDescriptorProto):
        yield parent.add_node(Node(descriptor.name, NodeType.ENUM_VALUE, [], parent))

    elif isinstance(descriptor, pb2.DescriptorProto):
        message_node = parent.add_node(Node(descriptor.name, NodeType.MESSAGE, [], parent))
        yield message_node
        for item in itertools.chain(descriptor.enum_type, descriptor.nested_type, descriptor.field, descriptor.oneof_decl):
            yield from traverse(message_node, item)

    elif isinstance(descriptor, pb2.FieldDescriptorProto):
        yield parent.add_node(Node(descriptor.name, NodeType.FIELD, [], parent))

    elif isinstance(descriptor, pb2.OneofDescriptorProto):
        yield parent.add_node(Node(descriptor.name, NodeType.ONEOF, [], parent))

    else:
        return