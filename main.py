import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import keyboard  # 用于模拟键盘按键
import time

# 初始化MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# 打开摄像头
cap = cv2.VideoCapture(0)

# 创建主窗口
root = tk.Tk()
root.title("手势追踪控制")

# 创建画布用于显示摄像头画面
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# 创建标签用于显示识别结果
result_label = tk.Label(root, text="手势方向: 无", font=("Arial", 16))
result_label.pack()

# 定义九宫格方向到按键的映射
gesture_directions = ["上", "下", "左", "右", "左上", "右上", "左下", "右下"]
gesture_to_keys = {direction: [] for direction in gesture_directions}  # 支持多个键位

# 镜面反转状态
mirror_mode = tk.BooleanVar(value=False)

# 长按时间阈值（秒）
LONG_PRESS_THRESHOLD = 1.0

# 当前按下的方向和时间
current_pressed_direction = None
press_start_time = None

# 用于存储当前按下的按键
pressed_keys = set()

# 握拳状态
fist_closed = False

# 用于存储当前录入的按键
current_keys = []

# 用于存储当前录入的方向
current_gesture = None

# 创建三个输入框
entry1 = tk.Entry(root, width=20)
entry1.pack()
entry2 = tk.Entry(root, width=20)
entry2.pack()
entry3 = tk.Entry(root, width=20)
entry3.pack()

# 创建确认按钮
confirm_button = tk.Button(root, text="确认", command=lambda: confirm_keys())
confirm_button.pack()

# 创建标签用于显示当前录入的按键
current_keys_label = tk.Label(root, text="当前录入的按键: 无", font=("Arial", 12))
current_keys_label.pack()

# 函数：确认按键录入
def confirm_keys():
    global current_keys, current_gesture
    if current_gesture and current_keys:
        gesture_to_keys[current_gesture] = current_keys.copy()
        result_label.config(text=f"'{current_gesture}'手势已映射到'{', '.join(current_keys)}'")
        current_keys.clear()
        current_gesture = None
        current_keys_label.config(text="当前录入的按键: 无")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)

# 函数：设置手势对应的按键
def set_gesture_keys(gesture):
    global current_gesture, current_keys
    current_gesture = gesture
    current_keys = []
    current_keys_label.config(text="当前录入的按键: 无")
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    result_label.config(text=f"请按下键盘按键来设置'{gesture}'手势")

# 创建按钮用于设置手势按键
for direction in gesture_directions:
    button = tk.Button(root, text=f"设置{direction}按键", command=lambda d=direction: set_gesture_keys(d))
    button.pack()

# 创建镜面反转切换按钮
mirror_button = tk.Button(root, text="切换镜像模式", command=lambda: mirror_mode.set(not mirror_mode.get()))
mirror_button.pack()

# 键盘事件处理函数
def on_key_press(event):
    global current_keys
    if current_gesture and len(current_keys) < 3:
        key = event.keysym
        if key not in current_keys:
            current_keys.append(key)
            current_keys_label.config(text=f"当前录入的按键: {', '.join(current_keys)}")
            if len(current_keys) == 1:
                entry1.insert(0, key)
            elif len(current_keys) == 2:
                entry2.insert(0, key)
            elif len(current_keys) == 3:
                entry3.insert(0, key)

# 绑定键盘事件
root.bind("<KeyPress>", on_key_press)

def update_frame():
    global current_pressed_direction, press_start_time, pressed_keys, fist_closed

    success, image = cap.read()
    if not success:
        return

    # 镜面反转
    if mirror_mode.get():
        image = cv2.flip(image, 1)

    # 将图像从BGR颜色空间转换为RGB颜色空间
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 处理图像以检测手部
    results = hands.process(image_rgb)

    # 绘制九宫格划分线条
    height, width, _ = image.shape
    third_width = width // 3
    third_height = height // 3

    # 绘制垂直线条
    cv2.line(image, (third_width, 0), (third_width, height), (0, 255, 0), 2)
    cv2.line(image, (2 * third_width, 0), (2 * third_width, height), (0, 255, 0), 2)

    # 绘制水平线条
    cv2.line(image, (0, third_height), (width, third_height), (0, 255, 0), 2)
    cv2.line(image, (0, 2 * third_height), (width, 2 * third_height), (0, 255, 0), 2)

    # 如果检测到手部
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 获取手腕关键点的坐标（点0）
            wrist_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            wrist_x = int(wrist_landmark.x * width)
            wrist_y = int(wrist_landmark.y * height)

            # 在图像上绘制手部关键点和连接线
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 判断手掌所在九宫格区域
            if wrist_x < third_width:
                if wrist_y < third_height:
                    direction = "左上"
                elif wrist_y < 2 * third_height:
                    direction = "左"
                else:
                    direction = "左下"
            elif wrist_x < 2 * third_width:
                if wrist_y < third_height:
                    direction = "上"
                elif wrist_y < 2 * third_height:
                    direction = "中心"  # 中间区域不触发
                else:
                    direction = "下"
            else:
                if wrist_y < third_height:
                    direction = "右上"
                elif wrist_y < 2 * third_height:
                    direction = "右"
                else:
                    direction = "右下"

            # 检测握拳状态
            # 获取指尖和指根的关键点
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

            # 计算指尖与指根的距离
            thumb_distance = ((thumb_tip.x - thumb_mcp.x) ** 2 + (thumb_tip.y - thumb_mcp.y) ** 2) ** 0.5
            index_distance = ((index_tip.x - index_mcp.x) ** 2 + (index_tip.y - index_mcp.y) ** 2) ** 0.5
            middle_distance = ((middle_tip.x - middle_mcp.x) ** 2 + (middle_tip.y - middle_mcp.y) ** 2) ** 0.5
            ring_distance = ((ring_tip.x - ring_mcp.x) ** 2 + (ring_tip.y - ring_mcp.y) ** 2) ** 0.5
            pinky_distance = ((pinky_tip.x - pinky_mcp.x) ** 2 + (pinky_tip.y - pinky_mcp.y) ** 2) ** 0.5

            # 如果所有指尖与指根的距离都小于某个阈值，则认为手是握拳状态
            if (thumb_distance < 0.05 and index_distance < 0.05 and
                    middle_distance < 0.05 and ring_distance < 0.05 and pinky_distance < 0.05):
                fist_closed = True
                result_label.config(text="手势: 握拳")
                for key in pressed_keys:
                    keyboard.release(key)  # 释放所有按键
                pressed_keys.clear()
                current_pressed_direction = None
                press_start_time = None
            else:
                fist_closed = False

            # 如果方向不是中间区域且手不是握拳状态
            if direction != "中心" and not fist_closed:
                # 如果当前没有按下的方向，或者方向改变
                if current_pressed_direction != direction:
                    current_pressed_direction = direction
                    press_start_time = time.time()
                else:
                    # 如果当前方向与之前相同且达到长按时间
                    if time.time() - press_start_time >= LONG_PRESS_THRESHOLD:
                        if gesture_to_keys[direction]:
                            result_label.config(text=f"手势方向: 长按 {direction}")
                            for key in gesture_to_keys[direction]:
                                if key not in pressed_keys:
                                    keyboard.press(key)  # 模拟按下按键
                                    pressed_keys.add(key)
            else:
                # 如果手掌在中间区域或握拳状态，重置按压状态
                for key in pressed_keys:
                    keyboard.release(key)  # 释放所有按键
                pressed_keys.clear()
                current_pressed_direction = None
                press_start_time = None
    else:
        # 如果没有检测到手部，重置按压状态
        for key in pressed_keys:
            keyboard.release(key)  # 释放所有按键
        pressed_keys.clear()
        current_pressed_direction = None
        press_start_time = None

    # 将图像转换为PhotoImage格式以在Tkinter中显示
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    # 更新画布上的图像
    canvas.create_image(0, 0, anchor=tk.NW, image=image)
    canvas.image = image

    # 每隔10毫秒更新一次画面
    root.after(10, update_frame)


# 开始更新画面
update_frame()

# 运行主循环
root.mainloop()

# 释放资源
cap.release()
cv2.destroyAllWindows()