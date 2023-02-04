""" This is a class for searching a filesystem for a filename. It allows more forgiving user input than default python"
"""
class Search():
    def __init__(self, filename):
        self._filename = filename
        self._sortedDir = None

    def sort(self,unordList):
        """
        this method uses insetion sort to sort the files in the directory currently searching
        necesary to allow for searching later with binary search
        in insertion sort we take values in an unsorted list and continously insert them into their appropriate position in a sorted list
        """
        # for each item in the unordered list
        for i in range(1, len(unordList)):
            position = i 
            # while we arent at the start index and the current element is less than the previous element,
            while position > 0 and unordList[position-1] > unordList[position]:
                # swap the two elements if they are not in the correct order
                unordList[position], unordList[position-1] = unordList[position-1], unordList[position]
                # change the position value to be the previous element
                position -= 1
        # once all loops are broken, return the ordered list
        return unordList

    def search(self,unordList):
        """
        this uses binary search on an ordered list to check the filename is in the directory.
        returns a boolean value and takes an unordered list as a parameter (uses insertion sort first).
        """
        self._sortedDir = self.sort(unordList)