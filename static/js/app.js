// Vietnamese Spell Checker JavaScript

class SpellCheckerApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.checkHealth();
        this.performanceStats = {
            totalRequests: 0,
            averageResponseTime: 0,
            cacheHitRate: 0
        };
    }

    initializeElements() {
        this.textInput = document.getElementById('text-input');
        this.checkBtn = document.getElementById('check-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.copyBtn = document.getElementById('copy-btn');
        this.autoEvaluateBtn = document.getElementById('auto-evaluate-btn');
        this.generateTestBtn = document.getElementById('generate-test-btn');
        this.resultsSection = document.getElementById('results-section');
        this.loading = document.getElementById('loading');
        this.errorMessage = document.getElementById('error-message');
        this.errorText = document.getElementById('error-text');
        
        // Stats elements
        this.errorCount = document.getElementById('error-count');
        this.confidence = document.getElementById('confidence');
        this.processingTime = document.getElementById('processing-time');
        
        // Text content elements
        this.originalText = document.getElementById('original-text');
        this.correctedText = document.getElementById('corrected-text');
        this.errorsContainer = document.getElementById('errors-container');
    }

    bindEvents() {
        this.checkBtn.addEventListener('click', () => this.checkSpelling());
        this.clearBtn.addEventListener('click', () => this.clearText());
        this.copyBtn.addEventListener('click', () => this.copyResults());
        this.autoEvaluateBtn.addEventListener('click', () => this.autoEvaluate());
        this.generateTestBtn.addEventListener('click', () => this.generateTest());
        
        // Auto-check on Enter
        this.textInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.checkSpelling();
            }
        });
    }

    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (!data.spell_checker_ready) {
                this.showError('Spell checker đang khởi tạo, vui lòng đợi...');
            }
            
            // Update performance stats
            if (data.performance_stats) {
                this.performanceStats = data.performance_stats;
                this.updatePerformanceDisplay();
            }
        } catch (error) {
            console.log('Health check failed:', error);
        }
    }

    updatePerformanceDisplay() {
        // Update performance info if available
        const performanceInfo = document.getElementById('performance-info');
        if (performanceInfo && this.performanceStats) {
            performanceInfo.innerHTML = `
                <div class="performance-stats">
                    <span>Requests: ${this.performanceStats.total_requests || 0}</span>
                    <span>Avg Time: ${this.performanceStats.average_response_time || 0}ms</span>
                    <span>Cache Hit: ${this.performanceStats.cache_hit_rate || 0}%</span>
                </div>
            `;
        }
    }

    async checkSpelling() {
        const text = this.textInput.value.trim();
        
        if (!text) {
            this.showError('Vui lòng nhập văn bản cần kiểm tra');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        const startTime = performance.now();

        try {
            const response = await fetch('/api/check_spelling', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            const result = await response.json();
            const endTime = performance.now();
            const processingTime = Math.round(endTime - startTime);

            this.hideLoading();

            if (response.ok) {
                this.displayResults(result, processingTime);
                this.updatePerformanceStats();
            } else {
                this.showError(result.error || 'Có lỗi xảy ra khi kiểm tra chính tả');
            }

        } catch (error) {
            this.hideLoading();
            this.showError('Không thể kết nối đến server');
            console.error('Error:', error);
        }
    }

    async updatePerformanceStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            
            if (data.performance_stats) {
                this.performanceStats = data.performance_stats;
                this.updatePerformanceDisplay();
            }
        } catch (error) {
            console.log('Failed to update performance stats:', error);
        }
    }

    displayResults(result, processingTime) {
        // Update stats
        this.errorCount.textContent = result.error_count || 0;
        this.confidence.textContent = `${Math.round((result.confidence || 0) * 100)}%`;
        this.processingTime.textContent = `${result.processing_time_ms || processingTime}ms`;
        
        // Display error categories if available
        if (result.error_categories && Object.keys(result.error_categories).length > 0) {
            this.displayErrorCategories(result.error_categories);
        }
        
        // Display original text with error highlighting
        this.displayOriginalText(result.original_text, result.errors || [], result.word_probabilities || {});
        
        // Display corrected text
        this.displayCorrectedText(result.corrected_text);
        
        // Display errors list
        this.displayErrorsList(result.errors || []);
        
        // Show cache status if available
        if (result.cached !== undefined) {
            this.showCacheStatus(result.cached);
        }
        
        this.showResults();
    }

    showCacheStatus(cached) {
        const cacheStatus = document.getElementById('cache-status');
        if (cacheStatus) {
            cacheStatus.textContent = cached ? '💾 From Cache' : '🔄 Fresh Result';
            cacheStatus.className = cached ? 'cache-hit' : 'cache-miss';
        }
    }

    displayErrorCategories(categories) {
        const container = document.getElementById('categories-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        Object.entries(categories).forEach(([category, count]) => {
            const categoryItem = document.createElement('div');
            categoryItem.className = 'category-item';
            categoryItem.innerHTML = `
                <div class="category-name">${this.getCategoryDisplayName(category)}</div>
                <div class="category-count">${count}</div>
                <div class="category-description">${this.getCategoryDescription(category)}</div>
            `;
            container.appendChild(categoryItem);
        });
        
        document.getElementById('error-categories').style.display = 'block';
    }

    getCategoryDisplayName(category) {
        const names = {
            'tone_error': 'Lỗi dấu thanh',
            'sticky_typing': 'Lỗi dính chữ',
            'typo_error': 'Lỗi gõ nhầm',
            'capitalization': 'Lỗi viết hoa',
            'spacing_punctuation': 'Lỗi dấu cách',
            'compound_word': 'Lỗi từ ghép'
        };
        return names[category] || category;
    }

    getCategoryDescription(category) {
        const descriptions = {
            'tone_error': 'Lỗi về dấu thanh và ký tự',
            'sticky_typing': 'Lỗi dính chữ khi gõ nhanh',
            'typo_error': 'Lỗi gõ nhầm phím',
            'capitalization': 'Lỗi viết hoa không đúng',
            'spacing_punctuation': 'Lỗi về dấu cách và dấu câu',
            'compound_word': 'Lỗi về từ ghép'
        };
        return descriptions[category] || '';
    }

    displayOriginalText(text, errors, wordProbabilities) {
        // Hiển thị văn bản gốc đơn giản, không highlight
        this.originalText.textContent = text;
        
        // Nếu có lỗi, thêm thông tin về lỗi ở dưới
        if (errors && errors.length > 0) {
            const errorInfo = document.createElement('div');
            errorInfo.className = 'error-info';
            errorInfo.innerHTML = `
                <div class="error-summary">
                    <strong>Phát hiện ${errors.length} lỗi chính tả:</strong>
                </div>
                <div class="error-list">
                    ${errors.map(error => `
                        <span class="error-item">
                            <strong>"${error.word}"</strong> → <em>"${error.corrected}"</em>
                        </span>
                    `).join(', ')}
                </div>
            `;
            
            // Xóa error info cũ nếu có
            const oldErrorInfo = this.originalText.parentNode.querySelector('.error-info');
            if (oldErrorInfo) {
                oldErrorInfo.remove();
            }
            
            // Thêm error info mới
            this.originalText.parentNode.appendChild(errorInfo);
        }
    }

    getProbabilityClass(probability) {
        if (probability >= 0.8) return 'probability-high';
        if (probability >= 0.6) return 'probability-medium';
        if (probability >= 0.4) return 'probability-low';
        return 'probability-very-low';
    }

    highlightErrors(text, errors) {
        let highlightedText = text;
        
        errors.forEach(error => {
            const word = error.word;
            const corrected = error.corrected;
            const replacement = `<span class="error-highlight" title="Gợi ý: ${corrected}">${word}</span>`;
            
            // Use regex to replace the word
            const regex = new RegExp(`\\b${this.escapeRegex(word)}\\b`, 'g');
            highlightedText = highlightedText.replace(regex, replacement);
        });
        
        return highlightedText;
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    displayErrorsList(errors) {
        const container = this.errorsContainer;
        container.innerHTML = '';
        
        if (errors.length === 0) {
            container.innerHTML = '<div class="no-errors">✅ Không tìm thấy lỗi chính tả!</div>';
            return;
        }
        
        errors.forEach(error => {
            const errorItem = document.createElement('div');
            errorItem.className = 'error-item';
            errorItem.innerHTML = `
                <div class="error-word">${error.word}</div>
                <div class="suggestions">
                    ${error.suggestions ? error.suggestions.map(suggestion => 
                        `<span class="suggestion" onclick="app.replaceWord('${error.word}', '${suggestion}')">${suggestion}</span>`
                    ).join('') : ''}
                </div>
                <div class="error-category">${this.getCategoryDisplayName(error.category)}</div>
            `;
            container.appendChild(errorItem);
        });
    }

    replaceWord(oldWord, newWord) {
        const textInput = this.textInput;
        const text = textInput.value;
        const regex = new RegExp(`\\b${this.escapeRegex(oldWord)}\\b`, 'g');
        const newText = text.replace(regex, newWord);
        textInput.value = newText;
        
        this.showSuccessMessage(`Đã thay thế "${oldWord}" bằng "${newWord}"`);
    }

    clearText() {
        this.textInput.value = '';
        this.hideResults();
        this.hideError();
    }

    async copyResults() {
        const correctedText = document.getElementById('corrected-text');
        if (correctedText && correctedText.textContent) {
            try {
                await navigator.clipboard.writeText(correctedText.textContent);
                this.showSuccessMessage('Đã sao chép văn bản đã sửa!');
            } catch (error) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = correctedText.textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                this.showSuccessMessage('Đã sao chép văn bản đã sửa!');
            }
        } else {
            this.showError('Không có văn bản để sao chép');
        }
    }

    showLoading() {
        this.loading.style.display = 'flex';
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    showResults() {
        this.resultsSection.style.display = 'block';
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.style.display = 'flex';
    }

    hideError() {
        this.errorMessage.style.display = 'none';
    }

    showSuccessMessage(message) {
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(successMessage);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (successMessage.parentNode) {
                successMessage.parentNode.removeChild(successMessage);
            }
        }, 3000);
    }

    displayCorrectedText(text) {
        this.correctedText.textContent = text;
    }

    async autoEvaluate() {
        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/api/auto_evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            this.hideLoading();

            if (response.ok && result.success) {
                this.displayEvaluationResults(result.results);
            } else {
                this.showError(result.error || 'Có lỗi xảy ra khi chạy đánh giá tự động');
            }

        } catch (error) {
            this.hideLoading();
            this.showError('Không thể kết nối đến server');
            console.error('Error:', error);
        }
    }

    displayEvaluationResults(results) {
        // Tạo HTML cho kết quả đánh giá
        const evaluationHTML = `
            <div class="evaluation-results">
                <h3><i class="fas fa-chart-line"></i> Kết quả đánh giá tự động</h3>
                
                <div class="evaluation-summary">
                    <div class="summary-item">
                        <span class="summary-label">Tổng số test:</span>
                        <span class="summary-value">${results.total_tests}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Test thành công:</span>
                        <span class="summary-value">${results.successful_tests}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Điểm trung bình:</span>
                        <span class="summary-value score-${this.getScoreClass(results.average_score)}">${results.average_score.toFixed(1)}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Thời gian xử lý TB:</span>
                        <span class="summary-value">${results.performance_stats.average_processing_time.toFixed(2)}ms</span>
                    </div>
                </div>

                <div class="category-scores">
                    <h4>Điểm theo danh mục:</h4>
                    <div class="category-grid">
                        ${Object.entries(results.category_scores).map(([category, score]) => `
                            <div class="category-score">
                                <span class="category-name">${category.toUpperCase()}</span>
                                <span class="category-value score-${this.getScoreClass(score)}">${score.toFixed(1)}%</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="evaluation-details">
                    <h4>Chi tiết từng test:</h4>
                    <div class="test-details">
                        ${results.detailed_results.map((result, index) => {
                            if (result.success && result.evaluation) {
                                const evaluation = result.evaluation;
                                return `
                                    <div class="test-item">
                                        <div class="test-header">
                                            <span class="test-number">Test ${index + 1}</span>
                                            <span class="test-category">${result.test_case.category.toUpperCase()}</span>
                                            <span class="test-score score-${this.getScoreClass(evaluation.score_percentage)}">${evaluation.score_percentage.toFixed(1)}%</span>
                                        </div>
                                        <div class="test-original">${result.test_case.original}</div>
                                        <div class="test-metrics">
                                            <span>Precision: ${evaluation.precision.toFixed(2)}</span>
                                            <span>Recall: ${evaluation.recall.toFixed(2)}</span>
                                            <span>F1: ${evaluation.f1_score.toFixed(2)}</span>
                                            <span>Time: ${result.processing_time.toFixed(2)}ms</span>
                                        </div>
                                    </div>
                                `;
                            } else {
                                return `
                                    <div class="test-item failed">
                                        <div class="test-header">
                                            <span class="test-number">Test ${index + 1}</span>
                                            <span class="test-category">${result.test_case.category.toUpperCase()}</span>
                                            <span class="test-score failed">FAILED</span>
                                        </div>
                                        <div class="test-error">${result.error || 'Unknown error'}</div>
                                    </div>
                                `;
                            }
                        }).join('')}
                    </div>
                </div>
            </div>
        `;

        // Hiển thị kết quả
        this.resultsSection.innerHTML = evaluationHTML;
        this.showResults();
    }

    getScoreClass(score) {
        if (score >= 90) return 'excellent';
        if (score >= 80) return 'good';
        if (score >= 70) return 'average';
        if (score >= 60) return 'poor';
        return 'very-poor';
    }

    async generateTest() {
        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/api/generate_test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num_cases: 5,
                    categories: null,
                    error_type: null
                })
            });

            const result = await response.json();
            this.hideLoading();

            if (response.ok && result.success) {
                this.displayGeneratedTest(result.test_case);
            } else {
                this.showError(result.error || 'Có lỗi xảy ra khi tạo test data');
            }

        } catch (error) {
            this.hideLoading();
            this.showError('Không thể kết nối đến server');
            console.error('Error:', error);
        }
    }

    displayGeneratedTest(testCase) {
        // Hiển thị test case được tạo
        const testHTML = `
            <div class="generated-test">
                <h3><i class="fas fa-magic"></i> Test Data Generated</h3>
                
                <div class="test-info">
                    <div class="test-category">
                        <span class="label">Category:</span>
                        <span class="value">${testCase.category.toUpperCase()}</span>
                    </div>
                    <div class="test-errors">
                        <span class="label">Expected Errors:</span>
                        <span class="value">${Object.keys(testCase.expected_corrections).length}</span>
                    </div>
                </div>

                <div class="test-content">
                    <div class="test-original">
                        <h4>Generated Text (with errors):</h4>
                        <div class="text-content">${testCase.original}</div>
                    </div>
                    
                    <div class="test-expected">
                        <h4>Expected Corrections:</h4>
                        <div class="corrections-list">
                            ${Object.entries(testCase.expected_corrections).map(([wrong, correct]) => `
                                <div class="correction-item">
                                    <span class="wrong">"${wrong}"</span>
                                    <span class="arrow">→</span>
                                    <span class="correct">"${correct}"</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div class="test-actions">
                    <button class="btn btn-primary" onclick="app.loadTestIntoInput('${testCase.original.replace(/'/g, "\\'")}')">
                        <i class="fas fa-edit"></i> Load into Input
                    </button>
                    <button class="btn btn-success" onclick="app.checkSpelling()">
                        <i class="fas fa-search"></i> Check Spelling
                    </button>
                </div>
            </div>
        `;

        // Hiển thị kết quả
        this.resultsSection.innerHTML = testHTML;
        this.showResults();
    }

    loadTestIntoInput(text) {
        this.textInput.value = text;
        this.textInput.focus();
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize the application
const app = new SpellCheckerApp(); 