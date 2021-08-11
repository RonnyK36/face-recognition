import cv2 as cv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import face_recognition as fr


# remove window from the screen
Tk().withdraw()
# temporary store a picked file from explorer
get_image = askopenfilename()

# assign picked image
picked_image = fr.load_image_file(get_image)
# encode the image
# encodings are used to compare known_people
picked_encoding = fr.face_encodings(picked_image)

def encode_faces(folder):
    # create a list of encoded people or faces
    list_people_encoding = []
    # to loop over all known_people in the selected folder
    for filename in os.listdir(folder):
        # make all files in the folder known_people
        known_people = fr.load_image_file(f'{folder}{filename}')
        # encode the known_people at index 0 from the folder
        known_encoding = fr.face_encodings(known_people)[0]

        # add encoded image to the list
        list_people_encoding.append((known_encoding,filename))

    return list_people_encoding

# a function to look for faces in a selected image and ID known
def find_known_face():
    # get all faces in  image
    face_location =fr.face_locations(picked_image)
    # loop over the faces that are saved
    for person in encode_faces('known_people/'):
        # create encoded face from list of people (index[0]=>known_encoding)
        encoded_face =person[0]
        # assign index[1](filename) to filename
        # gives the filename of the person
        filename = person[1]

        # check each face if it is known by comparing
        # tolerance help change accuracy, low tolerance, high accuracy
        is_target_face =fr.compare_faces(encoded_face, picked_encoding, tolerance=0.45)
        print(f'{is_target_face} {filename}')

        # handle case where a match was found and if not
        if face_location:
            # for iteration
            face_number =0
            for location in face_location:
                #  executed if match is found
                if is_target_face[face_number]:
                    # assigning filename to the variable label
                    label = filename
                    # calling function and passing in 2 parameters
                    create_frame(location,label)

                face_number +=1






def create_frame(location, label):
    # describe rectangle sides
    top, right, bottom,left = location

    # draw rectangle around identified image
    cv.rectangle(picked_image,(left,top),(right,bottom),(255,0,0),2)
    cv.rectangle(picked_image,(left,bottom),(right,bottom),(255,0,0),cv.FILLED)
    # add name to rectangle
    cv.putText(picked_image,label,(left+3,bottom+20),cv.FONT_HERSHEY_DUPLEX,0.4,(0,255,0),1)



def show_image():
    colored_img = cv.cvtColor(picked_image, cv.COLOR_BGR2RGB)
    # resize output window for large images
    # cv.namedWindow('Image Recognition', cv.WINDOW_GUI_NORMAL)
    # show image with title  name
    cv.imshow('Image Recognition', colored_img)
    # await any key press to exit
    cv.waitKey(0)
    # pop window on processing complete
    cv.destroyAllWindows()


# calling the functions on run
find_known_face()
show_image()
