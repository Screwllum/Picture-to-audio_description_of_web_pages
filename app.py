from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import json
import random

app = Flask(__name__)

# 上传文件夹路径
UPLOAD_FOLDER = './uploads/recordings/'
IMAGE_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

# 创建上传文件夹和图片文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

JSON_FILE = 'recording_data.json'
if not os.path.exists(JSON_FILE):
    image_list = os.listdir(IMAGE_FOLDER)
    recording_data = {image: 0 for image in image_list}  # 每张图片只记录一个录音数
    with open(JSON_FILE, 'w') as f:
        json.dump(recording_data, f)
else:
    with open(JSON_FILE, 'r') as f:
        recording_data = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_with_fewest_recordings():
    """从 JSON 文件中找到录音文件数最少的图片"""
    min_recordings = min(recording_data.values())
    images_with_min_recordings = [image for image, count in recording_data.items() if count == min_recordings]
    return random.choice(images_with_min_recordings)

@app.route('/')
def index():
    random_image = get_image_with_fewest_recordings()  # 获取录音文件数最少的图片
    return render_template('index.html', image_file=random_image)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return "未找到音频文件", 400

    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    image_name = request.form['image_name']  # 获取图片名

    # 检查文件是否已经存在，防止重复上传
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(upload_path):
        return "录音已经存在，不能重复上传", 400

    if allowed_file(filename):
        audio_file.save(upload_path)
        # 将录音文件名记录到日志中
        with open('recordings_log.txt', 'a') as log_file:
            log_file.write(f"{request.remote_addr} {filename}\n")
        # 更新 JSON 文件中的录音计数
        recording_data[image_name] += 1
        with open(JSON_FILE, 'w') as f:
            json.dump(recording_data, f)
        return "音频上传成功", 200
    else:
        return "不支持的文件类型", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
