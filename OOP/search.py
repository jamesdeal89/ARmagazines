""" This is a class for searching a filesystem for a filename. It allows more forgiving user input than default python"
"""
class Search():
    def __init__(self, filename, unordList):
        self._filename = filename
        self._unordList = unordList
        self._sortedDir = None


    def sort(self):
        """
        this method uses insetion sort to sort the files in the directory currently searching
        necesary to allow for searching later with binary search
        in insertion sort we take values in an unsorted list and continously insert them into their appropriate position in a sorted list
        """
        # insertion sort --> O(n^2) time complexity 
        # for each item in the unordered list
        for i in range(1, len(self._unordList)):
            position = i 
            # while we arent at the start index and the current element is less than the previous element,
            while position > 0 and self._unordList[position-1] > self._unordList[position]:
                # swap the two elements if they are not in the correct order
                self._unordList[position], self._unordList[position-1] = self._unordList[position-1], self._unordList[position]
                # change the position value to be the previous element
                position -= 1
        # once all loops are broken, set the sortedDir attribute to the sorted list
        self._sortedDir = self._unordList

        # line below only used if testing the function with pytest
        return self._sortedDir


    def binarySearch(self,sortedDir,target,start,end):
        if start > end:
            # file not found, return False
            return False
        else:
            # calculate mid-point
            mid = (start + end) //2
            # check if mid-point is the file 
            if target == sortedDir[mid]:
                # file exists, return True
                return True
            # otherwise check if file would be above or below the mid-poiny
            elif target > sortedDir[mid]:
                # recur and exclude the first half of the list
                return self.binarySearch(sortedDir,target,mid+1,end)
            elif target < sortedDir[mid]:
                # recur and exclude the second half of the list
                return self.binarySearch(sortedDir,target,start,mid-1)


    def search(self):
        """
        this uses binary search on an ordered list to check if the filename is in the directory.
        returns a boolean value and takes no parameters. MUST call sort() method first.
        """
        if self._sortedDir != None:
            # completes a binary search algorithm --> O(log n) complexity 
            return self.binarySearch(self._sortedDir,self._filename,0,len(self._sortedDir)-1)
        else:
            sys.exit("ERROR - call sort() method before search() method")
