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
        # iterate through each row
        for column in range(0,height):
            # iterate through each column
            for row in range(0,width):
                # list to hold each pixels, RGB values after operation
                values = []
                # iterate and hold each images pixel colour values one by one for each colour
                for value in img[column, row]:
                    for value2 in img2[column,row]:
                        # use my binary converter to get binary values
                        value = self.decimalToBinary(value) 
                        value2 = self.decimalToBinary(value2)
                        # adjust the length of the values so that both have the same number of bits
                        if value > value2:
                            # .zfill(desiredLength) can be used on an str to fill with leading 0's
                            value2 = int(str(value2).zfill(len(str(value))))
                        elif value2 > value:
                            value = int(str(value).zfill(len(str(value2))))
                        # iterate through each bit in each value
                        for bit in value:
                            for bit in value2:
                                # perform a bitwise AND operation using if conditions
                                if value == 1 and value2 == 1:
                                    values.append(1)
                                else:
                                    values.append(0)
                        # perform AND operation on the bits and add to this pixels values
                        #values.append(value&value2)
                # ammend the pixel values in the respective pixel with the ANDed values
                img[column,row] = (values[0],values[1],values[2])
        # return the amended first image which now holds the values after being ANDed with all of image 2
        return img


    def bitOr(self, img, img2):
        # perform a bitwise OR between the two images
        height = img.shape[0]
        width = img.shape[1]
        if img.shape != img2.shape:
            sys.exit("ERROR - images are not the same size")
        # iterate through each row
        for column in range(0,height):
            # iterate through each column
            for row in range(0,width):
                # list to hold each pixels, RGB values after operation
                values = []
                # iterate and hold each images pixel colour values one by one for each colour
                for value in img[column, row]:
                    for value2 in img2[column,row]:
                        # use my binary converter to get binary values
                        value = self.decimalToBinary(value) 
                        value2 = self.decimalToBinary(value2)
                        # adjust the length of the values so that both have the same number of bits
                        if value > value2:
                            # .zfill(desiredLength) can be used on an str to fill with leading 0's
                            value2 = int(str(value2).zfill(len(str(value))))
                        elif value2 > value:
                            value = int(str(value).zfill(len(str(value2))))
                        # iterate through each bit in each value
                        for bit in value:
                            for bit in value2:
                                # perform a bitwise AND operation using if conditions
                                if value == 1 or value2 == 1:
                                    values.append(1)
                                else:
                                    values.append(0)
                        # perform OR operation on the bits and add to this pixels values
                        # values.append(value|value2)
                # ammend the pixel values in the respective pixel with the ORed values
                img[column,row] = (values[0],values[1],values[2])
        # return the amended first image which now holds the values after being ORed with all of image 2
        return img

    def bitNot(self, img):
        # perfrom a bitwise NOT on an image
        height = (img.shape[0])
        width = (img.shape[1])
        for column in range(0,height):
            for row in range(0,width):
                # iterate through every pixel value
                # create list to store new values for this pixel
                values = []
                for value in img[column,row]:
                    # iterate through every pixel's RGB values, using a loop here as sometimes images have more than 3 values (CMYK)
                    # convert to binary using my converter method
                    value = self.decimalToBinary(value)
                    # use a bitwise NOT on the value
                    # values.append(~value)
                    for bit in str(value):
                        if int(bit) == 0:
                            values.append(1)
                        else:
                            values.append(0)
                img[column,row] = (values[0],values[1],values[2])