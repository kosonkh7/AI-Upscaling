document.addEventListener('DOMContentLoaded', () => {
    // UI 요소 가져오기
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

    let selectedFile = null; // 선택된 파일 저장

    // --- UI 상태 관리 함수 ---
    function showSection(section) {
        uploadSection.style.display = 'none';
        processingSection.style.display = 'none';
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        section.style.display = 'flex'; // flex로 설정하여 중앙 정렬 유지
    }

    function resetUI() {
        selectedFile = null;
        imageUpload.value = ''; // 파일 입력 초기화
        fileInfo.textContent = '';
        upscaleButton.disabled = true;
        originalImage.src = '';
        upscaledImage.src = '';
        downloadLink.href = '';
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

        // 원본 이미지 미리보기
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // 업스케일 버튼 클릭
    upscaleButton.addEventListener('click', async () => {
        if (!selectedFile) {
            showError('업스케일할 이미지를 선택해주세요.');
            return;
        }

        showSection(processingSection);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/upscale/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                // 백엔드에서 JSON 에러 응답을 보낼 경우를 대비
                const errorText = await response.text();
                let errorDetail = '알 수 없는 오류가 발생했습니다.';
                try {
                    const errorJson = JSON.parse(errorText);
                    errorDetail = errorJson.detail || errorDetail;
                } catch (e) {
                    errorDetail = errorText || errorDetail;
                }
                throw new Error(`업스케일링 실패: ${errorDetail}`);
            }

            // 응답이 이미지 Blob이므로 직접 Blob으로 받음
            const imageBlob = await response.blob();

            // Blob을 URL로 변환하여 이미지 표시
            const upscaledImageUrl = URL.createObjectURL(imageBlob);
            upscaledImage.src = upscaledImageUrl;

            // 다운로드 링크 설정
            downloadLink.href = upscaledImageUrl;
            downloadLink.download = `upscaled_${selectedFile.name}`; // 다운로드 파일명 설정

            // 이미지 로딩 완료 후 결과 섹션 표시
            upscaledImage.onload = () => {
                showSection(resultSection);
            };
            upscaledImage.onerror = () => {
                showError('업스케일된 이미지 로딩에 실패했습니다.');
                URL.revokeObjectURL(upscaledImageUrl); // 에러 발생 시 URL 해제
            };

        } catch (error) {
            console.error('Error:', error);
            showError(`오류가 발생했습니다: ${error.message}`);
        }
    });

    // 다시 시작 버튼 클릭
    resetButton.addEventListener('click', resetUI);
    errorResetButton.addEventListener('click', resetUI);

    // 초기 UI 설정
    resetUI();
});