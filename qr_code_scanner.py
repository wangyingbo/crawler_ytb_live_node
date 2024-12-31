import cv2
import numpy as np
import pafy
from pyzbar.pyzbar import decode

def process_frame(frame):
    # 将帧转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用 pyzbar 解码二维码
    barcodes = decode(gray)
    for barcode in barcodes:
        # 提取二维码数据
        barcode_data = barcode.data.decode('utf-8')
        print(f"QR Code detected: {barcode_data}")

        # 绘制矩形框在二维码周围
        points = barcode.polygon
        if len(points) > 4:  # 如果二维码是多边形
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull
        n = len(points)
        for j in range(0, n):
            cv2.line(frame, tuple(points[j]), tuple(points[(j+1) % n]), (0, 255, 0), 3)

    return frame

def main():
    # 获取视频流
    url = 'https://www.youtube.com/watch?v=cS6zS5hi1w0'
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    # 使用 OpenCV 打开视频流
    cap = cv2.VideoCapture(best.url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 处理帧
        frame = process_frame(frame)

        # 显示结果
        cv2.imshow('QR Code Scanner', frame)

        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
