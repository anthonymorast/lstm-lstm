class popualation:
    organisms = []
    def __init__(self):
        self.organisms = []
    
    def getOrganismList(self):
        return self.organisms
    
    def getOrganismAt(self, index):
        if index >= len(organisms):
            print("population#getOrganismAt(): Index out of range; Index: " + str(index) + " Range: " + len(self.organisms))
        else:
            return self.organisms[index]

    def addOrganism(self, organism):
        self.organisms.append(organism)