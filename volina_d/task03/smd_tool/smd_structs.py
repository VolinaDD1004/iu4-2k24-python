PREFIX = '// Created by Crowbar 0.74'

class Vector3:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'{format(self.x, '.6f')} {format(self.y, '.6f')} {format(self.z, '.6f')}'

    @classmethod
    def load(cls, tokens: list[str]):
        return cls(float(tokens[0]),
                   float(tokens[1]),
                   float(tokens[2]))

class Position(Vector3):
    pass

class Rotation(Vector3):
    pass

class Bone:

    def __init__(self, id: int, name: str, parent_id: int):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def __str__(self):
        return f'  {self.id} "{self.name}" {self.parent_id}\n'

    @classmethod
    def load(cls, tokens: list[str]):
        return cls(int(tokens[0]), tokens[1].replace('"', ''), int(tokens[2]))

class Movement:

    def __init__(self, bone: Bone, position: Position, rotation: Rotation):
        self.bone = bone
        self.position = position
        self.rotation = rotation

    def __str__(self):
        return f'    {self.bone.id} {self.position} {self.rotation}\n'

    @classmethod
    def load(cls, bone: Bone, tokens: list[str]):
        return cls(bone, Position.load(tokens[0:3]), Rotation.load(tokens[3:]))

class Frame:

    def __init__(self, time: int, movements: list[Movement]):
        self.time = time
        self.movements = movements

    def __str__(self):
        return (
                f'  time {self.time}\n'
                f'{''.join(f'{movement}' for movement in self.movements)}'
                )

class SMD:

    def __init__(self, version: int, nodes: list[Bone], skeleton: list[Frame]):
        self.version = version
        self.nodes = nodes
        self.skeleton = skeleton

    def __str__(self):
        return (
                f'{PREFIX}\n'
                f'version {self.version}\n'
                'nodes\n'
                f'{''.join(f'{bone}' for bone in self.nodes)}'
                'end\n'
                'skeleton\n'
                f'{''.join(f'{frame}' for frame in self.skeleton)}'
                'end\n'
                )