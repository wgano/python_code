import cv2
import numpy as np
from tensorflow import keras

# 加载训练好的手势数字识别模型
model = keras.models.load_model('gesture_model.h5')  # 请替换为你的模型文件路径

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 在此处添加手势识别的代码
    # 首先，处理摄像头捕获的图像，进行预处理（例如，缩放、归一化）

    # 示例：在捕获的图像上绘制一个矩形区域，然后提取该区域作为手势图像
    roi = frame[100:300, 100:300]

    # 对手势图像进行预处理，以与模型输入匹配

    # 示例：将图像缩放为 64x64 像素
    resized_roi = cv2.resize(roi, (64, 64))

    # 使用模型进行手势数字识别
    prediction = model.predict(np.array([resized_roi]))
    predicted_digit = np.argmax(prediction)

    # 在图像上显示识别结果
    cv2.putText(frame, f"Predicted Digit: {predicted_digit}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 显示图像
    cv2.imshow('Gesture Recognition', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
