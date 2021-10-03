import copy
import csv


class Subject:
    """
    domain_times: array
    domain_rooms: array
    type: string, "c" or "o"
    name: name of subject, string
    """

    def __init__(self, domain_times: [], domain_rooms: [], type: str, name: str):
        self.domain_times = domain_times
        self.domain_rooms = domain_rooms
        self.temp_time = ""
        self.temp_room = ""
        self.type = type
        self.name = name

    def setRoom(self, room):

        self.temp_room = room

    def setTime(self, time):
        self.temp_time = time


class Constraints:

    @staticmethod
    def isSatisfied(variable1: Subject, assignedSubjects: []) -> bool:
        """
        accepts two subjects and checks if they satisfy the constraints
        1. If both are c, both cannot have the same time slot
        2. If both are o, can have same timeslot,  but then can't have same room, or both can be in different timeslots
        3. If one is o and the other is c, can't have same timeslot

        """
        for variable2 in assignedSubjects:

            # both compulsory subjects
            if (variable1.type == "c" and variable2.type == "c"):

                # same timeslot
                if (variable1.temp_time == variable2.temp_time):
                    return False

            # both optional subjects
            elif (variable1.type == "o" and variable2.type == "o"):

                # same timeslot
                if (variable1.temp_time == variable2.temp_time):

                    # same room
                    if (variable1.temp_room == variable2.temp_room):
                        return False

            # one optional, one compulsory
            elif (variable1.type == "c" and variable2.type == "o"):

                # same timeslot
                if (variable1.temp_time == variable2.temp_time):
                    return False

            # switch (one compulsory, other optional)
            elif (variable1.type == "o" and variable2.type == "c"):

                # same timeslot
                if (variable1.temp_time == variable2.temp_time):
                    return False

        # all other options are valid
        return True


class IOFunctions:
    @staticmethod
    def loadVariablesWithDomains(inputFileName: str):
        file = open(inputFileName)
        csvreader = csv.reader(file)
        inputList1 = []
        for row in csvreader:
            inputList1.append(row[0].strip().split(","))
        file.close()
        print(inputList1)
        inputList = []
        for l in inputList1:
            inputList.append([s.strip() for s in l])


        print(inputList)
        subjects = []
        rooms = inputList.pop()

        for i in inputList:
            subjects.append(Subject(i[2:], copy.deepcopy(rooms), i[1], i[0]))

        return subjects

    @staticmethod
    def writeOutputsToFile(outputFileName, allSubjects):
        with open(outputFileName, mode='w') as file:
            writer = csv.writer(
                file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i in allSubjects:
                writer.writerow([i.name, i.temp_time, i.temp_room])

    @staticmethod
    def loadDummyValues():
        inputList = [
            ["S1", "o", "M1"],
            ["S2", "o", "M2", "M3", "T1"],
            ["S3", "o", "M1"],
            ["S4", "c", "M2"],
            ["S5", "c", "M2", "M3", "T2"],
            ["S6", "c", "M2", "M3", "T1"],
            ["R1", "R2"],
        ]
        rooms = inputList.pop()
        subjects = []
        for i in inputList:
            subjects.append(Subject(i[2:], copy.deepcopy(rooms), i[1], i[0]))

        return subjects

    @staticmethod
    def printResult(allSubjects):
        for i in allSubjects:
            print(i.name, i.temp_time, i.temp_room)


class CSP:
    @staticmethod
    def updateDomains(subject: Subject, time_slot: str, subjects):
        """
        """
        if subject.type == "c":
            for i in subjects:
                if time_slot in i.domain_times:
                    i.domain_times.remove(time_slot)
        return subjects

    @staticmethod
    def main():

        inputFileName = input("Input file name: ")
        outputFileName = input("Output file name: ")

        # contains Subject object
        allSubjects = IOFunctions.loadVariablesWithDomains(inputFileName)
        # allSubjects = IOFunctions.loadDummyValues()

        # TODO: reduce the domains of the problem

        # list of the names of the subjects
        # variables = IOFunctions.loadVariables(domains)
        result = CSP.backtrackingSearch([], allSubjects)
        if (result == None):
            print("No possible solutions")
        else:
            IOFunctions.printResult(result)
            IOFunctions.writeOutputsToFile(outputFileName, result)

    @staticmethod
    def backtrackingSearch(assignedSubjects: [], allSubjects: []):
        """
        performs backtracking search and returns valid assignments per subject
        """
        if (len(assignedSubjects)) == len(allSubjects):
            return assignedSubjects

        assignedSubjectNames = []

        for i in assignedSubjects:
            assignedSubjectNames.append(i.name)

        # contains the subjects (as Subject objects) that havent been assigned anything yet
        unassignedSubjects = []
        for i in allSubjects:
            if i.name not in assignedSubjectNames:
                unassignedSubjects.append(i)

        # a subject that hasnt been assigned a value yet
        # TODO: optimize selecting the next subject to be assigned: select most constrained value
        subject = unassignedSubjects[0]

        # cycling through all valid values for that unassigned subject's name
        domain_times = subject.domain_times.copy()
        domain_rooms = subject.domain_rooms.copy()

        for time in domain_times:
            subject.temp_time = time
            for room in domain_rooms:
                subject.temp_room = room
                if Constraints.isSatisfied(subject, assignedSubjects):
                    CSP.updateDomains(subject, time, allSubjects)
                    tempAssignedSubjects = copy.deepcopy(assignedSubjects)
                    tempAssignedSubjects.append(subject)
                    result = CSP.backtrackingSearch(
                        tempAssignedSubjects, allSubjects)
                    if (result != None):
                        return result
        return None


if __name__ == "__main__":
    CSP.main()
