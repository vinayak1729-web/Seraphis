document.getElementById('uploadForm').addEventListener('submit', function () {
    document.querySelector('.loader-container').style.display = 'flex';
    document.querySelector('.upload-btn').style.display = 'none';
});

// Preview image before upload
document.getElementById('file-upload').addEventListener('change', function (e) {
    if (e.target.files && e.target.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let previewContainer = document.createElement('div');
            previewContainer.className = 'preview-container';
            previewContainer.innerHTML = `
                <h3>Selected Image Preview</h3>
                <div class="image-container">
                    <img src="${e.target.result}" alt="Preview" class="upload-preview">
                </div>
            `;

            let existingPreview = document.querySelector('.preview-container');
            if (existingPreview) {
                existingPreview.remove();
            }

            document.querySelector('.upload-section').appendChild(previewContainer);
        };
        reader.readAsDataURL(e.target.files[0]);
    }
});