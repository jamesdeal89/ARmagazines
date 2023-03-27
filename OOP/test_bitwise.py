# testing for bitwise.py using pytest
from bitwise import Bitwise
import cv2

bitwise = Bitwise()

img = cv2.imread("../target.jpg")
img1 = cv2.imread("../target2.jpg")
img2 = cv2.imread("../target3.jpg")
img3 = cv2.imread("../targetREAL.jpg")

h,w,c = img.shape
img1 = cv2.resize(img1,(w,h))
img2 = cv2.resize(img2,(w,h))
img3 = cv2.resize(img3,(w,h))

testANDresult1 = cv2.bitwise_and(img,img1)
testANDresult2 = cv2.bitwise_and(img2,img3)
testORresult1 = cv2.bitwise_or(img,img1)
testORresult2 = cv2.bitwise_or(img,img1)
testNOTresult1 = cv2.bitwise_not(img)
testNOTresult2 = cv2.bitwise_not(img1)

def test_binary():
    assert bitwise.decimalToBinary(10,[]) == 1010
    assert bitwise.decimalToBinary(1,[]) == 1
    assert bitwise.decimalToBinary(15,[]) == 1111
    assert bitwise.decimalToBinary(255,[]) == 11111111


def test_and():
    assert bitwise.bitAnd(img,img1).all() == testANDresult1.all()
    assert bitwise.bitAnd(img2,img3).all() == testANDresult2.all()


def test_or():
    assert bitwise.bitOr(img,img1).all() == testORresult1.all()
    assert bitwise.bitOr(img2,img3).all() == testORresult2.all()


def test_not():
    assert bitwise.bitNot(img).all() == testNOTresult1.all()
    assert bitwise.bitNot(img1).all() == testNOTresult2.all()

