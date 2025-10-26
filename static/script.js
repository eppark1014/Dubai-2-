let selectedFile = null;

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadBox = document.getElementById('uploadBox');
    
    // 파일 선택 이벤트
    fileInput.addEventListener('change', handleFileSelect);
    
    // 드래그 앤 드롭 이벤트
    uploadBox.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);
});

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        showFileInfo(file);
    } else {
        alert('PDF 파일만 선택 가능합니다.');
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        document.getElementById('fileInput').files = e.dataTransfer.files;
        showFileInfo(file);
    } else {
        alert('PDF 파일만 업로드 가능합니다.');
    }
}

function showFileInfo(file) {
    document.getElementById('uploadBox').style.display = 'none';
    document.getElementById('fileInfo').style.display = 'block';
    document.getElementById('fileName').textContent = file.name;
}

function resetUpload() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadBox').style.display = 'block';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
}

async function uploadFile() {
    if (!selectedFile) {
        alert('파일을 선택해주세요.');
        return;
    }
    
    // UI 업데이트
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            alert('오류: ' + (data.error || '알 수 없는 오류가 발생했습니다.'));
            resetUpload();
        }
    } catch (error) {
        console.error('업로드 오류:', error);
        alert('업로드 중 오류가 발생했습니다: ' + error.message);
        resetUpload();
    } finally {
        document.getElementById('loadingSection').style.display = 'none';
    }
}

function displayResults(data) {
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultFileName').textContent = data.filename;
    document.getElementById('totalPages').textContent = data.total_pages;
    
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';
    
    data.results.forEach(pageResult => {
        const pageDiv = createPageResultElement(pageResult);
        resultsContainer.appendChild(pageDiv);
    });
    
    // 결과 섹션으로 스크롤
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function createPageResultElement(pageResult) {
    const div = document.createElement('div');
    div.className = 'page-result';
    
    const hasEdits = pageResult.edits && pageResult.edits.length > 0;
    
    let html = `
        <div class="page-header">
            <div class="page-title">📄 페이지 ${pageResult.page}</div>
            <div>
                <span class="badge ${hasEdits ? 'badge-success' : 'badge-info'}">
                    ${hasEdits ? `${pageResult.edits.length}개 수정사항 발견` : '수정사항 없음'}
                </span>
            </div>
        </div>
    `;
    
    // 이미지 미리보기
    if (pageResult.image_url) {
        html += `
            <div class="image-preview">
                <div class="image-grid">
                    <div class="image-container">
                        <h4>원본 페이지</h4>
                        <img src="${pageResult.image_url}" alt="페이지 ${pageResult.page}" 
                             onclick="window.open('${pageResult.image_url}', '_blank')">
                    </div>
        `;
        
        if (pageResult.debug_url) {
            html += `
                    <div class="image-container">
                        <h4>붉은색 영역 감지</h4>
                        <img src="${pageResult.debug_url}" alt="디버그 이미지" 
                             onclick="window.open('${pageResult.debug_url}', '_blank')">
                    </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
    }
    
    // 수정사항 테이블
    if (hasEdits) {
        html += createTableHTML(pageResult.table);
    } else {
        html += `
            <div class="empty-result">
                <div class="icon">✅</div>
                <p>이 페이지에는 붉은색 수정/삭제 지시사항이 없습니다.</p>
            </div>
        `;
    }
    
    div.innerHTML = html;
    return div;
}

function createTableHTML(tableData) {
    if (!tableData.rows || tableData.rows.length === 0) {
        return '<div class="empty-result"><p>분석 결과가 없습니다.</p></div>';
    }
    
    let html = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>순번</th>
                        <th>지시사항</th>
                        <th>대상문구</th>
                        <th>변환문구</th>
                        <th>위치</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    tableData.rows.forEach(row => {
        const actionClass = `action-${row.action}`;
        const originalTextClass = row.action === '삭제' ? 'text-deleted' : '';
        
        html += `
            <tr>
                <td>${row.order}</td>
                <td><span class="${actionClass}">${row.action}</span></td>
                <td class="${originalTextClass}">${formatMultilineText(row.original_text)}</td>
                <td>${formatMultilineText(row.new_text)}</td>
                <td><em>${escapeHtml(row.location)}</em></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    return html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMultilineText(text) {
    // \n을 <br>로 변환하여 여러 줄 표시
    if (!text) return '';
    return escapeHtml(text).replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
}
