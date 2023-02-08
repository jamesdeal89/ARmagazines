"""This class is for the bitwise operations which have to be performed on the webcam and source video to create a projection effect."""
class Bitwise():
    def __init__(self):
        pass


    def decimalToBinary(self,num,output=[]): 
        """takes a decimal number and uses recursion to return the binary value """
        # if the number is greater than 1
        if num > 1:
            # recur and half the number by 2 using integer division and also pass in the current output
            self.decimalToBinary(num//2,output)
        # then if the output is 1 or less we can append this to our output and return the output
        # when the output is not complete, the return closes the stack frame, 
        # but when the final stack is complete, it will return the final output out of the original call
        output.append(num%2)
        # make output a single string
        return int("".join(map(str,output)))


    def bitAnd(self,img, img2):
        # perform a bitwise AND between the two images
        height = img.shape[0]
        width = img.shape[1]
        if img.shape != img2.shape:
            sys.exit("ERROR - images are not the same size")
        for row in range(0,height):
            for column in range(0,width):
                values = []
                for value in img[column, row]:
                    for value2 in img2[column,row]:
                        values.append()
                img[column,row] = (values[0],values[1],values[2])


    def bitOr(self):
        # perform a bitwise OR between the two images
        pass


    def bitNot(self):
        # perfrom a bitwise NOT between the two images
        pass

