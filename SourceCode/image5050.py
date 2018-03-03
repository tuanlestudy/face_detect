import cv2
import sys




if __name__ == "__main__":
    # Get user supplied values
    imagePath = sys.argv[1]
    try:
        img = cv2.imread(imagePath,1)
        resized_image = cv2.resize(img,(50,50))
        newgrayimage = "image5050.jpg"
        cv2.imwrite(newgrayimage, resized_image)
        print("Complete!!!")
    except Exception as e:
        print(str(e))