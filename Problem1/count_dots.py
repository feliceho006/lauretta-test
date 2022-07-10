import cv2
import os
import numpy as np
from tqdm import tqdm

def get_count(img, colour):
    mask = cv2.inRange(img,colour[0],colour[1])
    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,10,param1=100, param2=3,
                                minRadius=1,maxRadius=5)
    if circles is not None:                            
        return len(circles[0])
    else:
        return 0

# cv2.imshow(filename,mask)
# cv2.waitKey(0)

def count_circles(root,filename):

    red = [(0,0,185),(20,20,255)] # lower and upper 
    blue = [(200,0,0),(255,20,20)]

    img = cv2.imread(root+"/"+filename)
    blur= cv2.medianBlur(img, 5)

    col = get_count(blur, red)
    row = get_count(blur, blue)

    return col, row

def assemble_puzzle(rootdir,filenames):
    coords = {}
    missing = []
    for i in tqdm(range(len(filenames))):
        col, row = count_circles(rootdir,filenames[i])
        if (row,col) in coords:
            missing.append(filenames[i])
        coords[(row,col)] = filenames[i]

    num_rows = max(coords.keys(), key=lambda x:x[0])[0]
    num_cols = max(coords.keys(), key=lambda x:x[1])[1]

    
    index=0
    for i in tqdm(range(1,num_rows+1)):
        for j in range(1,num_cols):

            if(i,j+1) in coords:
                if j == 1:
                    img1 = cv2.imread(rootdir+"/"+coords[(i,j)])
                img2 = cv2.imread(rootdir+"/"+coords[(i,j+1)])
                
            else:
                img2 = cv2.imread(rootdir+"/"+missing[index])
                index+=1
            img_strip = np.concatenate((img1,img2), axis=1)
            img1 = img_strip

        if i == 1:
            img_col = img1
            continue
        img_v = cv2.vconcat([img_col, img1])
        img_col = img_v

    imS = cv2.resize(img_col, (960, 540))
    cv2.imshow("window",imS)
    cv2.waitKey(0)

def main():
    rootdir = "./galaxy"
    filenames = os.listdir(rootdir)

    assemble_puzzle(rootdir,filenames)

if __name__ == '__main__':
    main()

