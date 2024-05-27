import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt

def calibrate(showPics: bool = True):
    # Check Current Working Directory
    print("Current working directory:", os.getcwd())

    # Read Image
    root = os.getcwd()
    calibrationDir = os.path.join(root, 'camera_calibration/checkers/')
    print("Calibration directory:", calibrationDir)
    imgPathList = glob.glob(os.path.join(calibrationDir, '*.jpeg'))
    print("imgPathList directory:", imgPathList)

    # Initialize
    nRows = 7
    nCols = 7
    termCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    worldPtsCur = np.zeros((nRows * nCols, 3), np.float32)
    worldPtsCur[:, :2] = np.mgrid[0:nRows, 0:nCols].T.reshape(-1, 2)
    worldPtsList = []
    imgPtsList = []

    # Find Corners
    for curImgPath in imgPathList:
        imgBGR = cv.imread(curImgPath)
        imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)
        cornersFound, cornersOrg = cv.findChessboardCorners(imgGray, (nRows, nCols), None)

        if cornersFound == True:
            worldPtsList.append(worldPtsCur)
            cornersRefined = cv.cornerSubPix(imgGray, cornersOrg, (11, 11), (-1, -1), termCriteria)
            imgPtsList.append(cornersRefined)

            if showPics:
                cv.drawChessboardCorners(imgBGR, (nRows, nCols), cornersRefined, cornersFound)
                cv.imshow('Chessboard', imgBGR)
                cv.waitKey(500)
    cv.destroyAllWindows()

    # Ensure at least one image was processed successfully
    if not worldPtsList or not imgPtsList:
        print("No corners found in any images.")
        return None

    # Calibrate
    imgGrayShape = imgGray.shape[::-1]
    repError, camMatrix, distCoeff, rvecs, tvecs = cv.calibrateCamera(worldPtsList, imgPtsList, imgGrayShape, None,
                                                                      None)
    print('Camera Matrix:\n', camMatrix)
    print("Reproj Error (pixels): {:.4f}".format(repError))

    # Save Calibration Parameters (later video)
    curFolder = os.path.dirname(os.path.abspath(__file__))
    paramPath = os.path.join(curFolder, 'calibration.npz')
    np.savez(paramPath,
             repError=repError,
             camMatrix=camMatrix,
             distCoeff=distCoeff,
             rvecs=rvecs,
             tvecs=tvecs)

    return camMatrix, distCoeff

# make image path a function argument
def removeDistortion(camMatrix, distCoeff, imgPath):
    # root = os.getcwd()
    # imgPath = os.path.join(root, 'camera_calibration\images\IMG_20240408_153443_963.jpg')
    img = cv.imread(imgPath)

    height, width = img.shape[:2]
    camMatrixNew, roi = cv.getOptimalNewCameraMatrix(camMatrix, distCoeff, (width, height), 1, (width, height))
    imgUndist = cv.undistort(img, camMatrix, distCoeff)
    # undistorted_image = cv.imwrite()
    # cv.imshow("undistorted image", imgUndist)

    # Draw Line to See Distortion Change
    cv.line(img, (1769, 103), (1780, 922), (255, 255, 255), 2)
    cv.line(imgUndist, (1769, 103), (1780, 922), (255, 255, 255), 2)

    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    # plt.imshow(imgUndist)
    # plt.show()

    cv.waitKey(0)
    cv.destroyAllWindows()

    return (imgUndist, camMatrix, distCoeff)


def calculate_XYZ(fx, fy, cx, cy, d_pix, x, y) -> dict:
    '''
    Z = (fx * 0.08) / (d_pix)

    X = ((x-cx)*Z)/fx

    Y= ((y-cy)*Z)/fy

    d_pix -diameter in pixel count
    x,y -the center of the ball in the image
    X,Y,Z -3D position of the object in camera coordinate system
    cx,cy -principal point.
    '''
    Z = (fx * 0.05) / (d_pix)

    X = ((cx-x)*Z)/fx

    Y= ((cy-y)*Z)/fy

    print({"X": X,"Y": Y,"Z": Z})
    return({"X": X,"Y": Y,"Z": Z})

    pass

def runCalibration():
    calibrate(showPics=True)


def runRemoveDistortion(imgPath):
    '''
    '''
    # camMatrix, distCoeff = calibrate(showPics=False)
    camMatrix = np.array([[1431.4442223274898, 0, 567.1183795056423],
                      [0, 1437.8244576241643, 359.903331163494],
                      [0, 0, 1]])
    distCoeff = np.array([[-0.48469890653839187, 10.765847101805587, 0.024410415674970664, 0.025233081566231098, -41.528018135482775]])
    print("fx:", camMatrix[0, 0])  # focal length in x direction
    print("fy:", camMatrix[1, 1])  # focal length in y direction
    print("px:", camMatrix[0, 2])  # principal point x coordinate
    print("py:", camMatrix[1, 2])  # principal point y coordinate
    un_distorted = removeDistortion(camMatrix, distCoeff, imgPath)
    return un_distorted


if __name__ == '__main__':
    # runCalibration()

    # =========================
    root = os.getcwd()
    imgPath = os.path.join(root, 'camera_calibration\images\IMG_20240408_153443_963.jpg')
    runRemoveDistortion(imgPath)
    # runRemoveDistortion()
