import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract


def ocr(img2):
    # img2 = cv2.imread('33.jpg')
    #This is only for numberplate image , If you are giving input only numberplate image
    #then it will give output of detected number and text form of number

    # cv2.imshow('Original',img2)
    #Noise Removel
    nr_img = cv2.bilateralFilter(img2,11,17,17)

    #Convert in gray image
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('GrayImg',gray)

    soblex = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
    # cv2.imshow('Solbex',soblex)

    ret, thresh = cv2.threshold(gray,130,255, cv2.THRESH_TOZERO)
    # cv2.imshow('Thresh',thresh)

    ret, threshs = cv2.threshold(gray,0,255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #cv2.imshow('threshs',threshs)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5,11) )

    morph_img= thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)
    # cv2.imshow('morphimg',morph_img)

    print(nr_img.shape)
    i = 0
    a=np.zeros((50,50,3),dtype=np.uint8)
    contours, hierarchy= cv2.findContours(morph_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:

        r = cv2.boundingRect(c)
        # print(r)
        
        if abs(r[1]-r[3])<25 and r[1]>10 and r[3]>10:
            cv2.rectangle(morph_img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,255,0))
            cv2.rectangle(nr_img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 255, 0))
            print(r)
            crop=nr_img[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0] + r[2])]
            
            # create a large image
            add_on = 80
            add_on2 = int(add_on/2)
            crop2=np.zeros((crop.shape[0]+add_on,crop.shape[1]+add_on,3),dtype=np.uint8)
            
            # removing bounding from crop image and move in
            cut = 3
            crop2[add_on2+cut:-add_on2-cut,add_on2+cut:-add_on2-cut,:] = crop[cut:-cut,cut:-cut,:]
            
            # Binarizing with index 145
            crop2 = cv2.cvtColor(crop2, cv2.COLOR_BGR2GRAY)
            for h in range(crop2.shape[0]):
                for w in range(crop2.shape[1]):
                    crop2[h][w] = 255 if crop2[h][w]>145 else 0

            crop2 = cv2.resize(crop2,(50,50))
            
            if i == 0:
                a = crop2
            else:            
                a = cv2.hconcat([a, crop2])
                
                # cv2.imshow("cropped",a)
            i+=1
    pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

    text =pytesseract.image_to_string(a, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    text=text[::-1]
    print (text)

    cv2.waitKey(0)
    f=open("LP.txt", "w")
    f.writelines(text)
    f.close()

    file=open("LP.txt","r")
    lines = file.readlines()
    file.close()

    del lines[0]

    new_file = open("LP.txt","w+")
    for line in lines:
        new_file.write(line)
    new_file.close()
    
    cv2.destroyAllWindows()