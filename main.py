import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import serial
import time

# Khởi động kết nối Serial đến Arduino (chọn cổng phù hợp)
arduino = serial.Serial('COM3', 9600)  # Thay 'COM3' bằng cổng Arduino của bạn
time.sleep(2)  # Đợi Arduino khởi động

# Cài đặt Mediapipe cho nhận diện tay
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Biến trạng thái LED
led_states = {"LED 1": False, "LED 2": False, "LED 3": False}

# Hàm xử lý khi phát hiện ngón tay chạm vào nút
def check_finger_touch(x, y):
    touched = False
    if btn_led1.winfo_x() < x < btn_led1.winfo_x() + btn_led1.winfo_width() and btn_led1.winfo_y() < y < btn_led1.winfo_y() + btn_led1.winfo_height():
        if not led_states["LED 1"]:
            arduino.write(b"LED1_ON\n")
            led_states["LED 1"] = True
        touched = True
    else:
        if led_states["LED 1"]:
            arduino.write(b"LED1_OFF\n")
            led_states["LED 1"] = False

    if btn_led2.winfo_x() < x < btn_led2.winfo_x() + btn_led2.winfo_width() and btn_led2.winfo_y() < y < btn_led2.winfo_y() + btn_led2.winfo_height():
        if not led_states["LED 2"]:
            arduino.write(b"LED2_ON\n")
            led_states["LED 2"] = True
        touched = True
    else:
        if led_states["LED 2"]:
            arduino.write(b"LED2_OFF\n")
            led_states["LED 2"] = False

    if btn_led3.winfo_x() < x < btn_led3.winfo_x() + btn_led3.winfo_width() and btn_led3.winfo_y() < y < btn_led3.winfo_y() + btn_led3.winfo_height():
        if not led_states["LED 3"]:
            arduino.write(b"LED3_ON\n")
            led_states["LED 3"] = True
        touched = True
    else:
        if led_states["LED 3"]:
            arduino.write(b"LED3_OFF\n")
            led_states["LED 3"] = False

# Hàm mở camera và hiển thị trong giao diện tkinter
def open_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)  # Lật hình ảnh để giống gương

        # Xử lý hình ảnh với Mediapipe để phát hiện tay
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Lấy vị trí ngón trỏ (landmark 8 là đầu ngón trỏ)
                index_finger_tip = hand_landmarks.landmark[8]
                h, w, _ = frame.shape
                finger_x, finger_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                # Kiểm tra nếu ngón tay chạm vào các nút LED
                check_finger_touch(finger_x, finger_y)

        # Chuyển đổi khung hình thành định dạng phù hợp với tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Hiển thị hình ảnh trong nhãn (label)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, open_camera)

# Khởi tạo cửa sổ tkinter
window = tk.Tk()
window.title("Camera với Nhận diện ngón tay và Nút LED")
window.geometry("800x600")

# Tạo khung để chứa video
frame_video = tk.Frame(window)
frame_video.pack()

# Tạo label để hiển thị video
lbl_video = tk.Label(frame_video)
lbl_video.pack()

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Tạo các nút LED với nền xanh, chữ đỏ, và đặt gần góc trái trên
btn_led1 = tk.Button(frame_video, text="LED 1", bg="blue", fg="red", width=10, height=2)
btn_led2 = tk.Button(frame_video, text="LED 2", bg="blue", fg="red", width=10, height=2)
btn_led3 = tk.Button(frame_video, text="LED 3", bg="blue", fg="red", width=10, height=2)

# Đặt các nút nằm ngang sát góc trái trên của khung video
btn_led1.place(x=10, y=10)
btn_led2.place(x=110, y=10)
btn_led3.place(x=210, y=10)

# Bắt đầu mở camera
open_camera()

# Thực hiện vòng lặp giao diện tkinter
window.mainloop()

# Giải phóng tài nguyên khi kết thúc
cap.release()
cv2.destroyAllWindows()
