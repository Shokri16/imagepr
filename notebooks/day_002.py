import cv2

image = cv2.imread(r"C:\Users\PC-LAB1\Desktop\shok\day 2 shapes (1).jpeg")

half_image = cv2.resize(image, (288, 288))

cv2.imshow("50% Image", half_image)
cv2.waitKey
cv2.destroyAllWindows