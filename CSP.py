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
        self.original_rooms = domain_rooms
        self.original_times = domain_rooms
        self.temp_time = ""
        self.temp_room = ""
        self.type = type
        self.name = name

    def setRoom(self, room):
        self.temp_room = room

    def setTime(self, time):
        self.temp_time = time


class IOFunctions:
    @staticmethod
    def loadVariablesWithDomains(inputFileName: str):
        file = open(inputFileName)
        csvreader = csv.reader(file)
        inputList1 = []
        for row in csvreader:
            inputList1.append(row[0].strip().split(","))
        file.close()
        inputList = []
        for l in inputList1:
            inputList.append([s.strip() for s in l])

        subjects = []
        rooms = inputList.pop()
        csp = {}
        for i in inputList:
            newSubject = (Subject(i[2:], copy.deepcopy(rooms), i[1], i[0]))
            subjects.append(newSubject)
            csp[newSubject] = i[2:]
        return [subjects, csp]

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
        csp = {}
        for i in inputList:
            subjects.append(Subject(i[2:], copy.deepcopy(rooms), i[1], i[0]))
            csp[i[0]] = " "
        return [subjects, csp]

    @staticmethod
    def printResult(allSubjects):
        for i in allSubjects:
            print(i.name, i.temp_time, i.temp_room)


class CSP:

    @staticmethod
    def assignmentComplete(assignment) -> bool:
        for i in assignment.keys():
            if assignment[i] == " ":
                return False
        return True

    @staticmethod
    def isConsistent(timeSlot: str, assignment: {}, type: str) -> bool:
        if timeSlot in assignment.values():
            for subject in assignment.keys():
                if assignment[subject] == timeSlot and type == "c":
                    return False
        return True

    @staticmethod
    def getMRVSubject(assignment: dict, csp: dict) -> []:
        unassignedSubjects = []
        for subject in csp.keys():
            if assignment[subject.name] == ' ':
                unassignedSubjects.append(subject)
        print("===================")
        print("UNASSIGNED")
        for s in unassignedSubjects:
            print(s.name)
        print("===================")
        leastSlotSubjects = []
        minSlots = float('inf')

        for subject in unassignedSubjects:
            numberOfSlots = len(csp[subject])
            minSlots = min(minSlots, numberOfSlots)

        for subject in unassignedSubjects:
            if len(csp[subject]) == minSlots:
                leastSlotSubjects.append(subject)
        # the subjects with the least possible values
        return leastSlotSubjects

    @staticmethod
    def calculateNumberOfConstraints(subject: Subject, csp) -> int:
        """
        gets the number of constraints for each of the leastSlotSubjects
        + 1 if there is a common timeslot between the two subjects
        """
        type = subject.type
        constraints = 0
        for cspSubject in csp.keys():
            if cspSubject != subject:
                for time in csp[subject]:
                    for time2 in csp[cspSubject]:
                        # TODO: check condition
                        if time == time2 and type == "c" or cspSubject.type == "c":
                            constraints += 1
        return constraints

    @staticmethod
    def selectUnassignedVariable(subjects, assignment, csp) -> Subject:
        leastSlotSubjects = CSP.getMRVSubject(assignment, csp)
        if len(leastSlotSubjects) == 1:
            return leastSlotSubjects[0]
        else:
            maximumValue = -float('inf')
            constraints = 0
            mostConstrainedSubject = " "
            for subject in leastSlotSubjects:
                constraints = CSP.calculateNumberOfConstraints(
                    subject, csp)  # tiebreaker: subject with highest number of constraints
                if constraints > maximumValue:
                    maximumValue = constraints
                    mostConstrainedSubject = subject
            return mostConstrainedSubject

    # TODO: implement
    @staticmethod
    def orderedTimeSlotOrder(subject, assignment, csp) -> []:
        timeSlotsForSubject = csp[subject]
        constraintSlots = {}
        for temp in timeSlotsForSubject:
            constraints = 0
            for s in csp.keys():
                if temp in csp[s] and (subject.type == "c" or s.type == "c"):
                    constraints += 1
            constraintSlots[temp] = constraints

        sortedTimeSlots = dict(
            sorted(constraintSlots.items(), key=lambda x: x[1]))
        print(sortedTimeSlots)
        return sortedTimeSlots

    @staticmethod
    def updateDomains(csp: {}, subject: Subject, timeSlot: str) -> {}:
        """
        """
        for cspSubject in csp.keys():
            if timeSlot in csp[cspSubject] and (subject.type == "c" or cspSubject.type == "c"):
                csp[cspSubject].remove(timeSlot)
        return csp

    @staticmethod
    def backtrackingSearch(subjects, csp, assignment) -> bool:
        """
        """
        return CSP.recursiveBacktracking(subjects,  csp, assignment)

    @staticmethod
    def recursiveBacktracking(subjects: [], csp: {}, assignment: {}) -> bool:
        """
        """
        print(assignment)
        if (CSP.assignmentComplete(assignment)):
            return True
        else:
            subject = CSP.selectUnassignedVariable(subjects, assignment, csp)
            orderedSlots = CSP.orderedTimeSlotOrder(
                subject, assignment, csp)
            for slot in orderedSlots.keys():
                if (CSP.isConsistent(slot, assignment, subject.type)):
                    assignment[subject.name] = slot
                    csp = CSP.updateDomains(csp, subject, slot)
                    result = CSP.recursiveBacktracking(
                        subjects, csp, assignment)
                    if (result == True):
                        return True
                    else:
                        assignment[subject.name] = " "
        return False

    @staticmethod
    def main():
        inputFileName = input("Input file name: ")
        outputFileName = input("Output file name: ")
        data = IOFunctions.loadVariablesWithDomains(inputFileName)
        allSubjects = data[0]
        csp = data[1]
        assignment = {}
        for i in allSubjects:
            assignment[i.name] = " "
        print(assignment)
        print(CSP.backtrackingSearch(allSubjects, csp, assignment))

        # csp has key value pairs: key is subject name, value is the list of timeslots


if __name__ == "__main__":
    CSP.main()
