from flask import Flask, render_template, request
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './uploads/'
IMAGE_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}  # 允许上传的音频文件类型

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# 用于检查文件扩展名是否有效
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    image_list = os.listdir(IMAGE_FOLDER)
    random_image = random.choice(image_list)
    return render_template('index.html', image_file=random_image)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    # 检查请求中是否包含文件
    if 'audio' not in request.files:
        return "未找到音频文件", 400

    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)

    # 确保文件有一个有效的音频扩展名
    if allowed_file(filename):
        # 保存文件到uploads文件夹
        audio_file.save(os.path.join(UPLOAD_FOLDER, filename))
        return "音频上传成功", 200
    else:
        return "不支持的文件类型", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)



