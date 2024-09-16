let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const uploadButton = document.getElementById('uploadButton');
const audioPlayback = document.getElementById('audioPlayback');
const imageFilename = document.getElementById('imageFilename').value;  // 获取图片文件名

// 点击“开始录音”按钮
recordButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            recordButton.disabled = true;
            stopButton.disabled = false;

            audioChunks = [];  // 清空上次录音的数据

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                uploadButton.disabled = false;  // 启用上传按钮
            });
        });
});

// 点击“停止录音”按钮
stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
});

// 点击“上传录音”按钮
uploadButton.addEventListener('click', () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();

    // 生成唯一的文件名，包括时间戳和图片文件名
    const timestamp = new Date().toISOString().replace(/[-:.]/g, '');  // 去掉无效字符
    const filename = `${imageFilename.replace(/\.[^/.]+$/, "")}_${timestamp}.wav`;

    formData.append('audio', audioBlob, filename);

    fetch('/upload-audio', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('音频上传成功！');
            window.location.reload();  // 上传成功后刷新页面
        } else {
            alert('音频上传失败！');
        }
    });

    uploadButton.disabled = true;  // 上传完成后禁用上传按钮
});
