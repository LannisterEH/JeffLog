import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from datetime import datetime

# 設定參數
fs = 44100  # 取樣率
duration = 1  # 每次錄音的時長 (秒)
noise_threshold = 0.015  # 噪音閾值，越小越敏感
save_folder = "audiolog"  # 儲存錄音片段的資料夾

# 如果資料夾不存在，創建它
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def record_and_save_noise():
    """ 持續錄音並保存噪音片段 """
    print("開始持續錄音，檢測噪音...")

    print(sd.query_devices())
    try:
        while True:
            # 錄音 1 秒的音頻數據
            audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, device=1)
            sd.wait()  # 等待錄音完成
            
            # 計算振幅，並檢測是否超過噪音閾值
            max_amplitude = np.max(np.abs(audio_data))
            print(f"當前振幅: {max_amplitude}")
            
            if max_amplitude > noise_threshold:
                # 如果超過閾值，保存音頻
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(save_folder, f"noise_{timestamp}-{max_amplitude}.wav")
                write(filename, fs, audio_data)
                print(f"噪音檢測到，保存片段: {filename}")
    
    except KeyboardInterrupt:
        print("錄音已停止")

if __name__ == "__main__":
    record_and_save_noise()