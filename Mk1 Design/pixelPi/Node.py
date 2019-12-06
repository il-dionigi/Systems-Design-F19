class Node:
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None

    def __repr__(self):
        return(f"{self.id}~ x:{self.x} y:{self.y}\n")