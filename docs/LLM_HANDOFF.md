# KS0223F (Keyestudio Smart Car) – LLM Handoff Brief

## Hardware / Platform
- Kit: Keyestudio KS0223F Smart Car
- Raspberry Pi: 4B
- Camera: Pi Camera (CSI ribbon) – working
- Ultrasonic sensor: HC-SR04 style – present, pins not yet extracted
- OLED: I2C address `0x3c` – present on robot board
- Motor/servo control: GPIO-based (NOT PCA9685 via I2C)

## OS / Camera Stack
- OS: Debian Trixie-based Raspberry Pi OS
- Camera commands: `rpicam-*` (not `libcamera-*`)
- Verified: `rpicam-still -o test.jpg` succeeds

## I2C
- `sudo i2cdetect -y 1` → only `3c` (OLED)
- No `0x40` → no PCA9685

## Vendor Code Location
```
~/KS0223-Keyestudio-Smart-Car-Kit-for-Raspberry-Pi/   # cloned repo
~/RaspberryPiCar/RaspberryPi-Car/                     # extracted vendor code
```

Extraction:
```bash
unzip -o Code.zip -d Code_unzipped
unzip -o Code_unzipped/Code/RaspberryPi-Car.zip -d RaspberryPiCar
```

Key vendor files:
- `RaspberryPiCar/RaspberryPi-Car/MainControl.py`
- `RaspberryPiCar/RaspberryPi-Car/basic_project/bp3_ultrasonic.py`
- `RaspberryPiCar/RaspberryPi-Car/basic_project/bp10_tracking_car.py`
- `RaspberryPiCar/RaspberryPi-Car/basic_project/bp12_avoid_car.py`

## Clean Project Repo
- GitHub: https://github.com/ZapRasdower/keyesrobot
- Local: `~/keyesrobot/`

### Structure
```
keyesrobot/
  hardware/      # bring-up test scripts (run directly on Pi)
  robot/         # abstraction modules (pins, motor, servo, ultrasonic)
  behaviors/     # autonomy modes (manual, follow, avoid, search)
  run/           # entry points
  docs/          # pin mapping, this file
```

## GPIO Pin Map Summary
See `docs/pin_mapping.md` for full table. Short version:

| Group | Pin | BCM | Status |
|-------|-----|-----|--------|
| Servo 1 | SERVO1 | 5 | ✅ confirmed |
| Servo 2 | SERVO2 | 6 | ✅ confirmed |
| Servo 3 | SERVO3 | 7 | ✅ confirmed |
| Left fwd | L_IN1 | 20 | ✅ confirmed |
| Left rev | L_IN2 | 21 | ✅ confirmed |
| Right fwd | R_IN1 | 24 | ✅ confirmed |
| Right rev | R_IN2 | 25 | ✅ confirmed |
| Left PWM | L_PWM1/2 | ??? | ❓ TODO |
| Right PWM | R_PWM1/2 | ??? | ❓ TODO |
| Ultrasonic | TRIG/ECHO | ??? | ❓ TODO |
| Tracking | LEFT/MID/RIGHT | ??? | ❓ TODO |

## Immediate Next Steps
1. **Extract missing pins** from `MainControl.py` and `bp3_ultrasonic.py`:
   ```bash
   grep -E 'PWM|IN3|IN4' ~/RaspberryPiCar/RaspberryPi-Car/MainControl.py
   grep -E 'TRIG|ECHO|trig|echo' \
     ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp3_ultrasonic.py
   ```
   Update `robot/pins.py` with the results.

2. **Run hardware tests** (in order):
   ```bash
   cd ~/keyesrobot
   python3 hardware/servo_test.py
   python3 hardware/motor_test.py    # fill PWM pins first
   python3 hardware/ultrasonic_test.py  # fill TRIG/ECHO first
   ```

3. **Autonomy stack** (after all hardware tests pass):
   - Camera stream via `picamera2`
   - Person detection: lightweight OpenCV DNN (MobileNet-SSD)
   - State machine: idle → search → track → approach
