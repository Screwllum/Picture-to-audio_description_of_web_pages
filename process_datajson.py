import os
import json

# 文件夹路径
UPLOAD_FOLDERS = {
    'action': './uploads/action/',
    'appearance': './uploads/appearance/',
    'attribute': './uploads/attribute/'
}

# JSON 文件路径
JSON_FILE = 'recording_data.json'

# 读取图片名
IMAGE_FOLDER = './static/images/'
image_list = os.listdir(IMAGE_FOLDER)
recording_data = {image: {"action": 0, "appearance": 0, "attribute": 0} for image in image_list}

def update_recording_data():
    """根据文件夹中的音频文件数量，更新 JSON 文件"""
    # 清空当前 JSON 文件的统计
    for image_name in recording_data.keys():
        recording_data[image_name] = {"action": 0, "appearance": 0, "attribute": 0}

    # 遍历每个录音文件夹，统计每张图片对应的录音文件数量
    for recording_type, folder_path in UPLOAD_FOLDERS.items():
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if not filename.endswith(('.wav', '.mp3')):
                    continue  # 跳过非音频文件

                # 从文件名中提取图片名（假设文件名格式为 image_name_recording_type_timestamp.wav）
                image_name = filename.rsplit('_', 2)[0] + ".jpg"  # 保留图片名和扩展名

                if image_name in recording_data:
                    recording_data[image_name][recording_type] += 1

    # 将更新后的数据写回 JSON 文件
    with open(JSON_FILE, 'w') as f:
        json.dump(recording_data, f, indent=4)
    print(f"已成功更新 {JSON_FILE} 文件。")

if __name__ == '__main__':
    update_recording_data()