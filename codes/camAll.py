import cv2 as cv
import glob
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from can_detection import *
from ikin_final import *

def triangulate(mtx1, mtx2, R, T):
 
##    uvs1 = [[360, 162]]
## 
##    uvs2 = [[197, 155]]
## 
##    uvs1 = np.array(uvs1)
##    uvs2 = np.array(uvs2)
 
    u1x1, u1y1, frame1 = center_location(0)
    u2x1, u2y1, frame2 = center_location(1)

    uvs1 = [[u1x1, u1y1]]
    uvs2 = [[u2x1, u2y1]]

    uvs1 = np.array(uvs1)
    uvs2 = np.array(uvs2)

##    frame1 = cv.imread('testing/_C1.png')
##    frame2 = cv.imread('testing/_C2.png')
 
    plt.imshow(frame1[:,:,[2,1,0]])
    plt.scatter(uvs1[:,0], uvs1[:,1])
    plt.show()
    
    plt.imshow(frame2[:,:,[2,1,0]])
    plt.scatter(uvs2[:,0], uvs2[:,1])
    plt.show()
 
    RT1 = np.concatenate([np.eye(3), [[0],[0],[0]]], axis = -1)
    P1 = mtx1 @ RT1
 
    RT2 = np.concatenate([R, T], axis = -1)
    P2 = mtx2 @ RT2
 
    def DLT(P1, P2, point1, point2):
 
        A = [point1[1]*P1[2,:] - P1[1,:],
             P1[0,:] - point1[0]*P1[2,:],
             point2[1]*P2[2,:] - P2[1,:],
             P2[0,:] - point2[0]*P2[2,:]
            ]
        A = np.array(A).reshape((4,4))
 
        B = A.transpose() @ A
        from scipy import linalg
        U, s, Vh = linalg.svd(B, full_matrices = False)
 
        print('Triangulated point: ')
        print(Vh[3,0:3]*2.2/Vh[3,3])
        return Vh[3,0:3]*2.2/Vh[3,3]
 
    p3ds = []
    for uv1, uv2 in zip(uvs1, uvs2):
        _p3d = DLT(P1, P2, uv1, uv2)
        p3ds.append(_p3d)
    p3ds = np.array(p3ds)
 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-15, 100)
    ax.set_ylim3d(-10, 100)
    ax.set_zlim3d(-10, 300)
    
    ax.scatter(p3ds[0][0], p3ds[0][1], p3ds[0][2], 'gray')
    ax.scatter(0, 0, 0, 'gray')
    
    ax.set_title('This figure can be rotated.')
    plt.show()
 
def calibrate_camera(images_folder):
    images_names = sorted(glob.glob(images_folder))
    images = []
    for imname in images_names:
        im = cv.imread(imname, 1)
        images.append(im)
    
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
    rows = 6
    columns = 8
    world_scaling = 1.
 
    objp = np.zeros((rows*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = world_scaling* objp
 
    width = images[0].shape[1]
    height = images[0].shape[0]
 
    imgpoints = []  
    objpoints = [] 
 
 
    for frame in images:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 
        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)
 
        if ret == True:
            conv_size = (11, 11)
 
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
            cv.drawChessboardCorners(frame, (rows,columns), corners, ret)
            cv.imshow('img', frame)
            k = cv.waitKey(500)
 
            objpoints.append(objp)
            imgpoints.append(corners)
 
 
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    print('rmse:', ret)
    print('camera matrix:\n', mtx)
    print('distortion coeffs:', dist)
    print('Rs:\n', rvecs)
    print('Ts:\n', tvecs)
 
    return mtx, dist
 
mtx1, dist1 = calibrate_camera(images_folder = 'camera_1_2/*')
mtx2, dist2 = calibrate_camera(images_folder = 'camera_2_3/*')

def stereo_calibrate(mtx1, dist1, mtx2, dist2, frames_folder):
    
    images_names = glob.glob(frames_folder)
    images_names = sorted(images_names)
    c1_images_names = images_names[:len(images_names)//2]
    c2_images_names = images_names[len(images_names)//2:]
    print(c1_images_names, c2_images_names)
    c1_images = []
    c2_images = []
    for im1, im2 in zip(c1_images_names, c2_images_names):
        _im = cv.imread(im1, 1)
        c1_images.append(_im)
 
        _im = cv.imread(im2, 1)
        c2_images.append(_im)
    

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
 
    rows = 6 
    columns = 8 
    world_scaling = 1.
 
    objp = np.zeros((rows*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = world_scaling* objp
 
    width = c1_images[0].shape[1]
    height = c1_images[0].shape[0]
 
    imgpoints_left = [] 
    imgpoints_right = []
 
    objpoints = [] 
 
    for frame1, frame2 in zip(c1_images, c2_images):
        gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        c_ret1, corners1 = cv.findChessboardCorners(gray1, (6, 8), None)
        c_ret2, corners2 = cv.findChessboardCorners(gray2, (6, 8), None)
 
        if c_ret1 == True and c_ret2 == True:
            corners1 = cv.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)
 
            cv.drawChessboardCorners(frame1, (6,8), corners1, c_ret1)
            cv.imshow('img', frame1)
 
            cv.drawChessboardCorners(frame2, (6,8), corners2, c_ret2)
            cv.imshow('img2', frame2)
            k = cv.waitKey(500)
 
            objpoints.append(objp)
            imgpoints_left.append(corners1)
            imgpoints_right.append(corners2)
    
    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, mtx1, dist1, mtx2, dist2, (width, height), criteria = criteria, flags = stereocalibration_flags)
 
    print(ret)
    return R, T
 
R, T = stereo_calibrate(mtx1, dist1, mtx2, dist2, 'synch_3/*')

print(R)
print("\n")
print(T)

goal = triangulate(mtx1, mtx2, R, T)
# angles = ikin(goal)
# arduino_operate(angles, false)




