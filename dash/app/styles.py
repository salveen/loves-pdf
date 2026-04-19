"""Custom CSS styles for the Priva PDF application."""

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

body {
    font-family: 'Space Grotesk', sans-serif;
    background: linear-gradient(135deg, #1c1917 0%, #292524 100%);
    min-height: 100vh;
    color: #fafaf9;
}

.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.main-header {
    text-align: center;
    padding: 1.5rem 0 0.75rem 0;
}

.main-header h1 {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
}

.main-header p {
    color: #78716c;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    margin-top: 0.25rem;
}

/* Tab styling */
.nav-tabs {
    gap: 4px;
    background-color: rgba(245, 158, 11, 0.08);
    padding: 0.5rem;
    border-radius: 12px;
    border: 1px solid rgba(245, 158, 11, 0.2);
    margin-bottom: 1.5rem;
}

.nav-tabs .nav-link {
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
    background-color: transparent;
    border: none;
    transition: all 0.3s ease;
}

.nav-tabs .nav-link:hover {
    color: rgba(255, 255, 255, 0.9);
    background-color: rgba(245, 158, 11, 0.1);
    border: none;
}

.nav-tabs .nav-link.active {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: #1c1917 !important;
    font-weight: 600 !important;
    border: none !important;
}

/* Upload area */
.upload-area {
    border: 2px dashed rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    background: rgba(245, 158, 11, 0.02);
    cursor: pointer;
}

.upload-area:hover {
    border-color: #f59e0b;
    background-color: rgba(245, 158, 11, 0.05);
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.upload-text {
    color: #a8a29e;
    font-size: 0.95rem;
}

/* File list */
.file-list-container {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(217, 119, 6, 0.08) 100%);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #f59e0b;
}

.file-list-header {
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.reorder-hint {
    color: #78716c;
    font-size: 0.85rem;
}

.sortable-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.file-item-draggable {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: rgba(28, 25, 23, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(245, 158, 11, 0.15);
    transition: all 0.2s ease;
    cursor: grab;
    user-select: none;
}

.file-item-draggable:hover {
    background: rgba(28, 25, 23, 0.8);
    border-color: rgba(245, 158, 11, 0.3);
    transform: translateX(2px);
}

.file-item-draggable:active {
    cursor: grabbing;
}

.file-item-draggable.dragging {
    opacity: 0.9;
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.25);
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.15);
    z-index: 1000;
}

.file-item-draggable.drag-over {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    transform: translateY(2px);
}

.drag-handle {
    color: #78716c;
    font-size: 1.1rem;
    letter-spacing: -3px;
    cursor: grab;
    padding: 0.25rem;
    transition: color 0.2s ease;
}

.file-item-draggable:hover .drag-handle {
    color: #f59e0b;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex: 1;
    min-width: 0;
}

.file-number {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #1c1917;
    font-weight: 700;
    font-size: 0.75rem;
    min-width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.file-name {
    color: #e7e5e4;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.file-size-badge {
    color: #a8a29e;
    font-size: 0.8rem;
    background: rgba(168, 162, 158, 0.15);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    flex-shrink: 0;
}

.remove-btn {
    background: rgba(239, 68, 68, 0.15);
    border: none;
    border-radius: 6px;
    color: #ef4444;
    width: 1.75rem;
    height: 1.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    opacity: 0.7;
}

.file-item-draggable:hover .remove-btn {
    opacity: 1;
}

.remove-btn:hover {
    background: rgba(239, 68, 68, 0.3);
    transform: scale(1.1);
}

/* Move buttons (up/down arrows) */
.file-actions {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-left: auto;
}

.move-btn {
    background: rgba(245, 158, 11, 0.15);
    border: none;
    border-radius: 6px;
    color: #f59e0b;
    width: 1.75rem;
    height: 1.75rem;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    font-weight: bold;
}

.move-btn:hover:not(:disabled) {
    background: rgba(245, 158, 11, 0.35);
    transform: scale(1.1);
}

.move-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.move-btn:active:not(:disabled) {
    transform: scale(0.95);
}

/* Simple list for split/compress (no reordering) */
.simple-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.file-item-simple {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: rgba(28, 25, 23, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(245, 158, 11, 0.1);
}

/* Button styling */
.btn-primary-custom {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #1c1917;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.35);
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary-custom:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
}

.btn-download {
    background: linear-gradient(135deg, #78716c 0%, #57534e 100%);
    color: #fafaf9;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px 0 rgba(120, 113, 108, 0.35);
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    font-size: 1rem;
}

.btn-download:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(120, 113, 108, 0.45);
    color: #fafaf9;
}

/* Input styling */
.form-control, .form-select {
    background-color: rgba(28, 25, 23, 0.8);
    border: 2px solid rgba(245, 158, 11, 0.2);
    border-radius: 8px;
    padding: 0.75rem;
    color: #fafaf9;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
    background-color: rgba(28, 25, 23, 0.9);
    color: #fafaf9;
}

.form-select option {
    background-color: #1c1917;
    color: #fafaf9;
}

.form-label {
    color: #a8a29e;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.08) 100%);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(245, 158, 11, 0.2);
    text-align: center;
}

.metric-label {
    color: #a8a29e;
    font-weight: 500;
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}

.metric-value {
    color: #fafaf9;
    font-weight: 700;
    font-size: 1.25rem;
}

/* Alert styling */
.alert-success-custom {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.1) 100%);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 12px;
    color: #86efac;
    padding: 1rem;
}

.alert-error-custom {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    color: #fca5a5;
    padding: 1rem;
}

/* Total size box */
.total-size-box {
    background: rgba(245, 158, 11, 0.08);
    border-radius: 8px;
    padding: 0.75rem;
    margin-top: 0.5rem;
    text-align: center;
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: #d6d3d1;
}

/* Compression level description */
.compression-desc {
    color: #78716c;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0;
    color: #78716c;
    font-size: 0.875rem;
}

.privacy-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
    color: #f59e0b;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Section header */
.section-header {
    color: #fafaf9;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.section-desc {
    color: #a8a29e;
    margin-bottom: 1.5rem;
}

/* Loading spinner */
.loading-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.spinner {
    border: 3px solid rgba(245, 158, 11, 0.1);
    border-top: 3px solid #f59e0b;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Tab pane content */
.tab-content {
    padding: 1rem 0;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.3), transparent);
    margin: 2rem 0;
}

/* Dropdown styling for dark theme */
.Select-control {
    background-color: rgba(28, 25, 23, 0.8) !important;
    border: 2px solid rgba(245, 158, 11, 0.2) !important;
}

.Select-menu-outer {
    background-color: #1c1917 !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
}

.Select-option {
    background-color: #1c1917 !important;
    color: #fafaf9 !important;
}

.Select-option:hover {
    background-color: rgba(245, 158, 11, 0.2) !important;
}

.Select-value-label {
    color: #fafaf9 !important;
}

/* Retro dropdown styling */
.retro-dropdown .Select-control,
.retro-dropdown > div {
    background: linear-gradient(180deg, rgba(40, 36, 33, 0.95) 0%, rgba(28, 25, 23, 0.98) 100%) !important;
    border: 2px solid rgba(245, 158, 11, 0.25) !important;
    border-radius: 8px !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 0 rgba(245, 158, 11, 0.1) !important;
    min-height: 42px !important;
}

.retro-dropdown .Select-control:hover,
.retro-dropdown > div:hover {
    border-color: rgba(245, 158, 11, 0.4) !important;
}

.retro-dropdown .Select-value-label,
.retro-dropdown .Select-placeholder {
    color: #e7e5e4 !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
}

.retro-dropdown .Select-arrow-zone {
    padding-right: 12px !important;
}

.retro-dropdown .Select-arrow {
    border-color: #f59e0b transparent transparent !important;
}

.retro-dropdown .Select-menu-outer {
    background: linear-gradient(180deg, #1c1917 0%, #292524 100%) !important;
    border: 2px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(245, 158, 11, 0.1) !important;
    overflow: hidden !important;
}

.retro-dropdown .Select-option {
    background: transparent !important;
    color: #d6d3d1 !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid rgba(245, 158, 11, 0.08) !important;
    transition: all 0.15s ease !important;
}

.retro-dropdown .Select-option:last-child {
    border-bottom: none !important;
}

.retro-dropdown .Select-option:hover,
.retro-dropdown .Select-option.is-focused {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
    color: #f59e0b !important;
}

.retro-dropdown .Select-option.is-selected {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.25) 0%, rgba(245, 158, 11, 0.1) 100%) !important;
    color: #f59e0b !important;
    font-weight: 600 !important;
}
"""


def get_index_string() -> str:
    """Generate the custom HTML template with injected CSS."""
    return '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
''' + CUSTOM_CSS + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
        // Drag and drop visual feedback for file reordering
        // Actual reordering is done via button clicks which are more reliable
        document.addEventListener('DOMContentLoaded', function() {
            let draggedItem = null;
            let draggedIndex = null;

            function initDragDrop() {
                const sortableLists = document.querySelectorAll('.sortable-list');
                
                sortableLists.forEach(list => {
                    const items = list.querySelectorAll('.file-item-draggable[draggable="true"]');
                    
                    items.forEach(item => {
                        // Avoid duplicate listeners
                        if (item.dataset.dragInitialized) return;
                        item.dataset.dragInitialized = 'true';
                        
                        item.addEventListener('dragstart', handleDragStart);
                        item.addEventListener('dragend', handleDragEnd);
                        item.addEventListener('dragover', handleDragOver);
                        item.addEventListener('dragenter', handleDragEnter);
                        item.addEventListener('dragleave', handleDragLeave);
                        item.addEventListener('drop', handleDrop);
                    });
                });
            }

            function handleDragStart(e) {
                draggedItem = this;
                draggedIndex = parseInt(this.dataset.index);
                this.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', draggedIndex);
                
                setTimeout(() => {
                    this.style.opacity = '0.5';
                }, 0);
            }

            function handleDragEnd(e) {
                this.classList.remove('dragging');
                this.style.opacity = '1';
                
                document.querySelectorAll('.file-item-draggable').forEach(item => {
                    item.classList.remove('drag-over');
                });
                
                draggedItem = null;
                draggedIndex = null;
            }

            function handleDragOver(e) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            }

            function handleDragEnter(e) {
                e.preventDefault();
                if (this !== draggedItem) {
                    this.classList.add('drag-over');
                }
            }

            function handleDragLeave(e) {
                this.classList.remove('drag-over');
            }

            function handleDrop(e) {
                e.preventDefault();
                e.stopPropagation();
                
                this.classList.remove('drag-over');
                
                if (draggedItem && this !== draggedItem) {
                    const fromIndex = parseInt(draggedItem.dataset.index);
                    const toIndex = parseInt(this.dataset.index);
                    
                    // Use the arrow buttons to move items step by step
                    // This triggers the reliable Dash callbacks
                    const direction = fromIndex < toIndex ? 'down' : 'up';
                    const steps = Math.abs(toIndex - fromIndex);
                    
                    let currentIndex = fromIndex;
                    for (let i = 0; i < steps; i++) {
                        const btnType = direction === 'down' ? 'merge-move-down' : 'merge-move-up';
                        const btn = document.querySelector(
                            `button[id*='"type":"${btnType}"'][id*='"index":${currentIndex}']`
                        );
                        if (btn && !btn.disabled) {
                            btn.click();
                            currentIndex = direction === 'down' ? currentIndex + 1 : currentIndex - 1;
                        }
                    }
                }
            }

            // Initialize on page load and watch for DOM changes
            initDragDrop();
            
            // Re-initialize when Dash updates the DOM
            const observer = new MutationObserver((mutations) => {
                let shouldInit = false;
                mutations.forEach((mutation) => {
                    if (mutation.addedNodes.length > 0) {
                        mutation.addedNodes.forEach(node => {
                            if (node.nodeType === 1 && 
                                (node.classList?.contains('file-item-draggable') ||
                                 node.querySelector?.('.file-item-draggable'))) {
                                shouldInit = true;
                            }
                        });
                    }
                });
                if (shouldInit) {
                    setTimeout(initDragDrop, 50);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
        </script>
    </body>
</html>
'''
