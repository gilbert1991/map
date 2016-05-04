import http_handler as hh
import my_util as mt
import setting as st
import objects as obj
import file_handler as fh
import feature
import register

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pyopengv as gv

def plot():
	marker_style = dict(color='cornflowerblue', linestyle=':', marker='o', 
				markersize=8, markerfacecoloralt='gray')
	fig, ax = plt.subplots()
	x = []
	y = []
	for r in road:
		x.append(r[1])
		y.append(r[0])		
		ax.plot(x, y, fillstyle='full', **marker_style)
	plt.show()

def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0
    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.
    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.
    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.
    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for m in matches:

        # Get the matching keypoints for each of the images
        img1_idx = m[0].queryIdx
        img2_idx = m[0].trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out

def snapRoadTest():
	fh.cleanDir(st.path + "image/sfm/", ".jpeg")
	interval = 0.0001
	path = [(40.694051, -73.983359), (40.690187, -73.981525)]

	road = hh.parseJsonRoad(hh.snapToRoad(path))

	road = mt.interpolate(road, interval)
	mt.filterPath(road, interval)

	hh.buildDataset(st.path + "image/sfm/images/", road, obj.CameraPara(size=(800, 800), fov=120, heading=[0], pitch=10))

	print road

def fivePointMatchTest():
	src = np.array( ([0, 0],[0, 1],[0, 2],[0, 3],[0, 4],[0, 5],[0, 6],[0, 7]), dtype='float64' )

	dst = np.array( ([1, 0],[1, 1],[1, 2],[1, 3],[1, 4],[1, 5],[1, 6],[1, 7]), dtype='float64' )
	dst = np.array( ([0, 0],[0, 1],[0, 2],[0, 3],[0, 4],[0, 5],[0, 6],[0, 7]), dtype='float64' )

	result = gv.relative_pose_ransac(src, dst, "NISTER", 0.01, 1000)
	print result

	return src, dst, result

def triangulationTest(src, dst, position, rotation):
	points1 = gv.triangulation_triangulate(src, dst, position, rotation)
	print points1

	points2 = gv.triangulation_triangulate2(src, dst, position, rotation)
	print points2

def imageMatchTest(src, dst):
	img1 = cv2.imread(src, 0)
	img2 = cv2.imread(dst, 0)

	kp1, des1 = feature.siftExtraction(img1)
	kp2, des2 = feature.siftExtraction(img2)

	matches = register.bruteForceMatch(des1, des2, 0.3)

	drawMatches(img1, kp1, img2, kp2, matches)

if __name__ == '__main__':
	# snapRoadTest()
	
	# src, dst, result = fivePointMatchTest()
	# triangulationTest(src, dst, result[:, :3], result[:, 3])

	imageMatchTest(st.path + "test_1.jpeg", st.path + "test_2.jpeg")
