import cv2
import dlib
import numpy as np
import os
# 初始化人脸检测器
detector = dlib.get_frontal_face_detector()

# 初始化人脸特征点检测器
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # 需要下载模型文件

# 初始化人脸识别模型
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # 需要下载模型文件

known_faces = {}
# 创建一个空字典来存储不同人脸的特征向量
filenames = os.listdir(r'.\specific_npc')
print(filenames)
for i in filenames:
    known_faces[i.split(".")[0]] = np.load('./specific_npc/'+i)


# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 用人脸检测器检测人脸
    faces = detector(gray)

    for face in faces:
        # 获取人脸特征点
        landmarks = predictor(gray, face)

        # 获取人脸特征向量
        face_descriptor = face_recognizer.compute_face_descriptor(frame, landmarks)

        # 在图像上绘制人脸框
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 在图像上标记人脸
        for name, known_face_descriptor in known_faces.items():
            match = np.linalg.norm(face_descriptor - known_face_descriptor)
            if match < 0.4:  # 调整阈值以控制匹配的松紧度
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 如果要为新的人脸添加特征向量，可以按以下方式：
        # known_faces["Person1"] = face_descriptor

    # 显示结果
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 按下Esc键退出循环
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()
