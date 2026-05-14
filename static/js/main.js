document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme toggle logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        if (themeToggleBtn) themeToggleBtn.textContent = 'Light Mode';
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (document.body.getAttribute('data-theme') === 'dark') {
                document.body.removeAttribute('data-theme');
                themeToggleBtn.textContent = 'Dark Mode';
                localStorage.setItem('theme', 'light');
            } else {
                document.body.setAttribute('data-theme', 'dark');
                themeToggleBtn.textContent = 'Light Mode';
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // 2. Sidebar active highlighting
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item:not(.ext-link)');

    navItems.forEach(item => {
        const itemPath = item.getAttribute('href');
        if (currentPath === itemPath || (itemPath !== '/' && currentPath.startsWith(itemPath))) {
            item.classList.add('active');
        }
    });

    // 3. Global Checklist interactive Logic
    const checkboxes = document.querySelectorAll('.check-box');

    // Auto-save checklist state in localStorage
    // Using currentPath to create a unique ID per page
    const pageId = 'checklist_' + currentPath.replace(/[^a-z0-9]/gi, '_');
    const savedState = JSON.parse(localStorage.getItem(pageId) || '{}');

    checkboxes.forEach((box, index) => {
        // Restore state
        if (savedState[index]) {
            box.checked = true;
            box.closest('.checklist-item').classList.add('checked');
        }

        // Handle changes
        box.addEventListener('change', function () {
            if (this.checked) {
                this.closest('.checklist-item').classList.add('checked');
                savedState[index] = true;
            } else {
                this.closest('.checklist-item').classList.remove('checked');
                savedState[index] = false;
            }
            localStorage.setItem(pageId, JSON.stringify(savedState));
        });
    });

    // 4. Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');

    copyButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // prevent checkbox toggling
            const codeBlock = btn.nextElementSibling;
            if (!codeBlock) return;

            const codeText = codeBlock.textContent;

            navigator.clipboard.writeText(codeText).then(() => {
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                btn.style.backgroundColor = '#4caf50';
                btn.style.borderColor = '#4caf50';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                    btn.style.borderColor = 'rgba(255,255,255,0.2)';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                btn.textContent = 'Failed';
                setTimeout(() => btn.textContent = 'Copy', 2000);
            });
        });
    });

    // 5. Reset Checklist Logic
    const resetBtn = document.getElementById('reset-checklist');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear all checkboxes on this page?')) {
                checkboxes.forEach((box, index) => {
                    box.checked = false;
                    const item = box.closest('.checklist-item');
                    if (item) item.classList.remove('checked');
                    savedState[index] = false;
                });
                localStorage.setItem(pageId, JSON.stringify(savedState));
            }
        });
    }

    // 6. Save as TXT Logic
    const saveBtn = document.getElementById('save-as-txt');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            let content = "LaTeX to DocX Conversion Checklist\n";
            content += "===================================\n\n";

            const checklistItems = document.querySelectorAll('.checklist-item');
            checklistItems.forEach((item) => {
                const box = item.querySelector('.check-box');
                const isChecked = box ? box.checked : false;
                const status = isChecked ? "[X]" : "[ ]";

                // Get label text cleanly
                const label = item.querySelector('label');
                let text = "";
                if (label) {
                    // Clone to avoid modifying the UI
                    const clone = label.cloneNode(true);
                    // Remove buttons and other UI elements that shouldn't be in text
                    clone.querySelectorAll('.copy-btn').forEach(el => el.remove());
                    text = clone.innerText;
                }

                // Clean up whitespace: replace multiple spaces/newlines with single ones
                // but keep some indentation for readability
                text = text.trim().split('\n').map(line => line.trim()).filter(line => line.length > 0).join('\n    ');

                content += `${status} ${text}\n\n`;
            });

            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `latex2docx_checklist_${new Date().toLocaleDateString().replace(/\//g, '-')}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
});
