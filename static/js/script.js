let mediaRecorder;
let audioChunks = [];
let mediaStream;
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const uploadButton = document.getElementById('uploadButton');
const audioPlayback = document.getElementById('audioPlayback');
const imageFilename = document.getElementById('imageFilename').value;  // 获取图片文件名
const nextImageButton = document.getElementById('nextImageButton');

let isRecording = false;
const talkButton = document.getElementById('talkButton');
const recordingIndicator = document.getElementById('recordingIndicator');

function toggleRecording() {
    if (!isRecording) {
        // 开始录音
        startRecording();
        talkButton.textContent = '停止录音';  // 按钮文字变为“停止说话”
        recordingIndicator.style.display = 'block';  // 显示动画提示
    } else {
        // 停止录音
        stopRecording();
        talkButton.textContent = '重新录音';  // 按钮文字变为“开始说话”
        recordingIndicator.style.display = 'none';  // 隐藏动画提示
    }
    isRecording = !isRecording;
}

// 开始录音
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaStream = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                uploadButton.disabled = false;
            });
        });
}

// 停止录音并释放资源
function stopRecording() {
    mediaRecorder.stop();
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());  // 释放音频流
    }
}

// 绑定按钮点击事件
talkButton.addEventListener('click', toggleRecording);

// 上传音频
uploadButton.addEventListener('click', () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();

    // 生成文件名，包括图片名
    const timestamp = new Date().toISOString().replace(/[-:.]/g, '');
    const filename = `${imageFilename.replace(/\.[^/.]+$/, "")}_${timestamp}.wav`;

    formData.append('audio', audioBlob, filename);
    formData.append('image_name', imageFilename);  // 提交图片名

    fetch('/upload-audio', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('音频上传成功！');
            recordButton.disabled = true;
        } else {
            alert('音频上传失败！');
        }
    });

    uploadButton.disabled = true;
});

// 点击“下一张图片”按钮
nextImageButton.addEventListener('click', () => {
    window.location.href = '/';  // 重新加载页面，显示下一张图片
});
