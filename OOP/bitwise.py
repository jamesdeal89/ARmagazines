"""This class is for the bitwise operations which have to be performed on the webcam and source video to create a projection effect."""
class Bitwise():
    def __init__(self):
        pass

    def DecimalToBinary(self,num,out=""): 
        if num >= 1:
            out += self.DecimalToBinary(num // 2, out)
        else:
            out += "0"
        return out

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

bitwise = Bitwise()
print(bitwise.DecimalToBinary(10))
