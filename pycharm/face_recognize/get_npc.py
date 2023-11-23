import cv2
import dlib
import numpy as np

# 输入人名信息
name = input("please input your name:")

# 初始化人脸检测器
detector = dlib.get_frontal_face_detector()

# 初始化人脸特征点检测器
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # 需要下载模型文件

# 初始化人脸识别模型
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # 需要下载模型文件

# 打开摄像头或图像文件
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 用人脸检测器检测人脸
    faces = detector(gray)

    if len(faces) == 1:
        # 获取人脸特征点
        landmarks = predictor(gray, faces[0])

        # 获取人脸特征向量
        face_descriptor = face_recognizer.compute_face_descriptor(frame, landmarks)

        # 保存特定人脸的特征向量到文件
        np.save("./specific_npc/"+name+".npy", face_descriptor)
        print("Specific face descriptor saved.")
        break

# 释放摄像头
cap.release()
