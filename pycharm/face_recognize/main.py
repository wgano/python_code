import cv2
import dlib

# 初始化人脸检测器
detector = dlib.get_frontal_face_detector()

# 初始化人脸特征点检测器
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")  # 需要下载模型文件

# 初始化人脸识别模型
face_recognizer = dlib.face_recognition_model_v1("./dlib_face_recognition_resnet_model_v1.dat")  # 需要下载模型文件

# 从摄像头捕获视频
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # 设置宽度为640像素
cap.set(4, 240)  # 设置高度为480像素

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

    # 显示结果
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 按下Esc键退出循环
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()