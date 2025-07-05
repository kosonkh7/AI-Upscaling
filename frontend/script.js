document.addEventListener('DOMContentLoaded', () => {
    const uploadSection = document.getElementById('upload-section');
    const dropArea = document.getElementById('drop-area');
    const imageUpload = document.getElementById('image-upload');
    const fileInfo = document.getElementById('file-info');
    const upscaleButton = document.getElementById('upscale-button');

    const processingSection = document.getElementById('processing-section');

    const resultSection = document.getElementById('result-section');
    const originalImage = document.getElementById('original-image');
    const upscaledImage = document.getElementById('upscaled-image');
    const downloadLink = document.getElementById('download-link');
    const resetButton = document.getElementById('reset-button');

    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    const errorResetButton = document.getElementById('error-reset-button');

    // Slider elements
    const imageComparisonSlider = document.getElementById('image-comparison-slider');
    const upscaledImageContainer = document.querySelector('.upscaled-image-container');
    const sliderHandle = document.getElementById('slider-handle');

    let selectedFile = null;
    let isDragging = false;

    // --- UI 상태 관리 함수 ---
    function showSection(section) {
        uploadSection.style.display = 'none';
        processingSection.style.display = 'none';
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        section.style.display = 'flex';
    }

    function resetUI() {
        if (upscaledImage.src && upscaledImage.src.startsWith('blob:')) {
            URL.revokeObjectURL(upscaledImage.src);
        }

        selectedFile = null;
        imageUpload.value = '';
        fileInfo.textContent = '';
        upscaleButton.disabled = true;
        originalImage.src = '';
        upscaledImage.src = '';
        downloadLink.href = '';

        // Reset slider position
        upscaledImageContainer.style.width = '50%';
        sliderHandle.style.left = '50%';
        imageComparisonSlider.style.height = 'auto'; // Reset height

        showSection(uploadSection);
    }

    function showError(message) {
        errorMessage.textContent = message;
        showSection(errorSection);
    }

    // --- 이벤트 리스너 ---

    // 드래그 앤 드롭 기능
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    dropArea.addEventListener('dragenter', () => dropArea.classList.add('highlight'), false);
    dropArea.addEventListener('dragleave', () => dropArea.classList.remove('highlight'), false);
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        dropArea.classList.remove('highlight');
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // 파일 입력 변경 감지
    imageUpload.addEventListener('change', (event) => {
        handleFiles(event.target.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];

        if (!file.type.startsWith('image/')) {
            showError('이미지 파일만 업로드할 수 있습니다.');
            return;
        }

        selectedFile = file;
        fileInfo.textContent = `선택된 파일: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        upscaleButton.disabled = false;

        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
            // Set slider height based on original image aspect ratio
            originalImage.onload = () => {
                const aspectRatio = originalImage.naturalHeight / originalImage.naturalWidth;
                imageComparisonSlider.style.height = `${imageComparisonSlider.offsetWidth * aspectRatio}px`;
            };
        };
        reader.readAsDataURL(file);
    }

    // 업스케일 버튼 클릭
    upscaleButton.addEventListener('click', async () => {
        if (!selectedFile) {
            showError('업스케일할 이미지를 선택해주세요.');
            return;
        }

        upscaleButton.disabled = true;
        showSection(processingSection);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/upscale/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                let errorDetail = '알 수 없는 오류가 발생했습니다.';
                try {
                    const errorJson = JSON.parse(errorText);
                    errorDetail = errorJson.detail || errorJson.detail[0].msg || errorDetail;
                } catch (e) {
                    errorDetail = errorText || errorDetail;
                }
                throw new Error(`업스케일링 실패: ${errorDetail}`);
            }

            const imageBlob = await response.blob();
            const upscaledImageUrl = URL.createObjectURL(imageBlob);
            upscaledImage.src = upscaledImageUrl;

            downloadLink.href = upscaledImageUrl;
            downloadLink.download = `upscaled_${selectedFile.name}`;

            await new Promise((resolve, reject) => {
                upscaledImage.onload = resolve;
                upscaledImage.onerror = reject;
            });

            showSection(resultSection);

        } catch (error) {
            console.error('Error:', error);
            showError(`오류가 발생했습니다: ${error.message}`);
        } finally {
            // No explicit re-enable needed here.
        }
    });

    // Slider functionality
    sliderHandle.addEventListener('mousedown', (e) => {
        isDragging = true;
        imageComparisonSlider.classList.add('active');
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        imageComparisonSlider.classList.remove('active');
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const sliderRect = imageComparisonSlider.getBoundingClientRect();
        let x = e.clientX - sliderRect.left;

        // Clamp x within slider bounds
        if (x < 0) x = 0;
        if (x > sliderRect.width) x = sliderRect.width;

        const percentage = (x / sliderRect.width) * 100;

        upscaledImageContainer.style.width = `${percentage}%`;
        sliderHandle.style.left = `${percentage}%`;
    });

    // Handle window resize for slider height
    window.addEventListener('resize', () => {
        if (originalImage.naturalWidth && originalImage.naturalHeight) {
            const aspectRatio = originalImage.naturalHeight / originalImage.naturalWidth;
            imageComparisonSlider.style.height = `${imageComparisonSlider.offsetWidth * aspectRatio}px`;
        }
    });

    // 다시 시작 버튼 클릭
    resetButton.addEventListener('click', resetUI);
    errorResetButton.addEventListener('click', resetUI);

    // 초기 UI 설정
    resetUI();
});