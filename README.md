‘‘
# 手势控制虚拟键盘 ✋⌨️

![Python版本](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV版本](https://img.shields.io/badge/OpenCV-4.5%2B-green)

基于MediaPipe的手势识别系统，通过摄像头捕捉手部动作实现虚拟键盘控制

## 🚀 核心功能

- **九宫格方向识别**：精确定位手掌在屏幕九宫格区域的位置
- **手势-按键映射**：自定义8个方向对应的键盘组合键
- **长按触发**：持续1秒以上触发特殊操作
- **握拳急停**：闭合手掌立即释放所有按键
- **镜面模式**：支持左右手切换使用

## 🛠️ 技术实现

### 关键算法
```python
# 手部区域判定逻辑
if wrist_x < third_width:
    if wrist_y < third_height: direction = "左上"
    elif wrist_y < 2*third_height: direction = "左"
    else: direction = "左下"
```

### 技术栈
- **手部追踪**：MediaPipe Hands
- **图像处理**：OpenCV
- **GUI界面**：Tkinter
- **键盘模拟**：keyboard库
- **性能优化**：60FPS实时处理

## 📦 安装使用

### 依赖安装
```bash
pip install opencv-python mediapipe keyboard pillow
```

### 启动程序
```bash
python main.py
```

## 🎮 操作指南

1. **手势设置**：
   - 点击界面按钮选择方向（如"左上"）
   - 按下物理键盘按键完成绑定（最多3键组合）

2. **控制模式**：
   - 手掌移动至九宫格区域触发对应按键
   - 保持手势1秒触发长按状态
   - 握拳立即停止所有按键输入

3. **镜像模式**：
   - 点击"切换镜像模式"按钮适配左右手


## 📂 项目结构
```
Gesture_Keyboard/
├── main.py    # 主程序
└── README.md
```

## 💡 应用场景

- **无障碍辅助**：为行动不便者提供输入方案
- **体感游戏**：替代手柄方向键控制
- **演示控制**：远程操控PPT翻页
- **智能家居**：手势控制智能设备

## 🚨 已知限制

- 需要良好光照条件
- 复杂背景可能影响识别
- 仅支持单只手势输入

## 运行界面
![image](https://github.com/user-attachments/assets/bdefd1ce-e28e-4632-89d7-390d76db0501)
![image](https://github.com/user-attachments/assets/2316690d-e681-45ab-bfb5-6b19fd33b48a)
![ae7609f6b46fac18873184be4747b5f](https://github.com/user-attachments/assets/fbeace66-4f03-41b8-899e-932dcf8babde)





## 🤝 如何贡献

欢迎提交：
- 更精准的手势识别算法
- 多语言界面支持
- 预置快捷键方案

贡献流程：
1. Fork项目仓库
2. 创建特性分支
3. 提交Pull Request

## 📄 开源协议
[MIT License](LICENSE)

---

⭐ **如果喜欢这个项目，欢迎Star支持！**  
🐛 **问题反馈**：附上环境配置和错误日志
```
