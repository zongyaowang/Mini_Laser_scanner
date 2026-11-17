# Project File List | 项目文件列表
> Electro-Dragon Drill 1D Rotating LiDAR Scanner

| 文件名 | 简要说明 | Description |
|--------|--------|-------------|
| `README.md` | GitHub 默认主说明文档（英文） | Default main README (English) |
| `README.en.md` | 独立英文版项目说明 | Separate English project documentation |
| `README.zh-CN.md` | 简体中文版项目说明 | Simplified Chinese documentation |
| `magcode.py` | 项目主扫描程序（MicroPython），包含AS5600谐波角度校正、舵机控制、点云输出 | Main scan firmware (MicroPython): AS5600 harmonic angle correction, servo control, point cloud output |
| `vl53l0x.py` | VL53L0X TOF激光测距传感器驱动库 | Driver library for VL53L0X TOF ranging sensor |
| `PCB_ofAS5600.json` | AS5600 编码器PCB设计文件 | PCB design source for AS5600 magnetic encoder board |

---
### 使用提示 / Instructions
1. 烧录到ESP32-C3：需要上传 `magcode.py` + `vl53l0x.py` 两个脚本
   Flash to ESP32-C3: upload both `magcode.py` and `vl53l0x.py`
2. `PCB_ofAS5600.json`：AS5600编码器PCB源文件，可导入PCB工具进行编辑与制版
   `PCB_ofAS5600.json`: PCB source file of AS5600 encoder, import into PCB editor for modification and manufacturing
