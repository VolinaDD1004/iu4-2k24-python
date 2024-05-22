from typing import TextIO
from .smd_structs import *

class SMDContext:

    def __init__(self):
        self.in_nodes = False
        self.in_skeleton = False

    def setNodes(self):
        self.in_nodes = True
        self.in_skeleton = False
    
    def setSkeleton(self):
        self.in_nodes = False
        self.in_skeleton = True

def findBone(id: int, bones: list[Bone]):
    for bone in bones:
        if bone.id == id:
            return bone
    return None

def parseSMD(stream: TextIO):

    context = SMDContext()
    time_oracle = 0

    smd_version : int
    bones : list[Bone] = []
    movements : list[Movement] = []
    frames : list[Frame] = []

    for line in stream:

        if line.startswith('//'):
            continue

        tokens = line.split()

        if tokens[0] == 'end':
            if context.in_nodes:
                context.setSkeleton()
                continue
            if context.in_skeleton:
                frames.append(Frame(time_oracle, movements))
                break

        if context.in_nodes and tokens[0] != 'nodes':
            bones.append(Bone.load(tokens))
            continue

        if context.in_skeleton and tokens[0] != 'skeleton':

            if tokens[0] == 'time':
                if not movements:
                    pass
                else: 
                    frames.append(Frame(int(tokens[1])-1, movements))
                    movements.clear()
                    time_oracle = int(tokens[1])
                continue

            movements.append(Movement.load(findBone(int(tokens[0]), bones), tokens[1:]))
            continue

        if tokens[0] == 'version':
            smd_version = int(tokens[1])
            context.setNodes()
            continue

    return SMD(smd_version, bones, frames)