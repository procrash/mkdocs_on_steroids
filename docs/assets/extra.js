/**
 * Custom JavaScript for C++ Advanced Library Documentation
 * Erweitert Material Theme mit zusätzlicher Funktionalität
 */

(function() {
    'use strict';

    // ========================================
    // Utility Functions
    // ========================================

    /**
     * Check if element is in viewport
     */
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    /**
     * Debounce function
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ========================================
    // Code Block Enhancements
    // ========================================

    /**
     * Add line numbers to code blocks
     */
    function enhanceCodeBlocks() {
        document.querySelectorAll('pre code').forEach((block) => {
            // Add data attribute for language
            const language = block.className.match(/language-(\w+)/);
            if (language) {
                const pre = block.parentElement;
                pre.setAttribute('data-language', language[1].toUpperCase());
            }

            // Add copy feedback
            const copyButton = block.parentElement.querySelector('.md-clipboard');
            if (copyButton) {
                copyButton.addEventListener('click', () => {
                    const originalText = copyButton.textContent;
                    copyButton.textContent = 'Copied!';
                    setTimeout(() => {
                        copyButton.textContent = originalText;
                    }, 2000);
                });
            }
        });
    }

    // ========================================
    // Smooth Scroll for Anchor Links
    // ========================================

    function enableSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // Update URL without jumping
                    history.pushState(null, null, href);
                }
            });
        });
    }

    // ========================================
    // Table of Contents Highlighter
    // ========================================

    function highlightTOC() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    if (id) {
                        // Remove active class from all TOC links
                        document.querySelectorAll('.md-nav--secondary .md-nav__link').forEach(link => {
                            link.classList.remove('md-nav__link--active');
                        });

                        // Add active class to current section
                        const tocLink = document.querySelector(`.md-nav--secondary a[href="#${id}"]`);
                        if (tocLink) {
                            tocLink.classList.add('md-nav__link--active');
                        }
                    }
                }
            });
        }, {
            rootMargin: '-20% 0px -80% 0px'
        });

        // Observe all headings
        document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
            observer.observe(heading);
        });
    }

    // ========================================
    // External Link Indicator
    // ========================================

    function markExternalLinks() {
        document.querySelectorAll('a[href^="http"]').forEach(link => {
            // Skip if already has icon
            if (link.querySelector('.external-link-icon')) return;

            // Check if external
            if (!link.href.includes(window.location.hostname)) {
                link.classList.add('external-link');
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');

                // Add icon
                const icon = document.createElement('span');
                icon.className = 'external-link-icon';
                icon.innerHTML = ' ↗';
                icon.style.fontSize = '0.8em';
                icon.style.opacity = '0.6';
                link.appendChild(icon);
            }
        });
    }

    // ========================================
    // Code Example Tabs Memory
    // ========================================

    function rememberTabSelections() {
        const storageKey = 'advlib-tab-selections';

        // Load saved selections
        const savedSelections = JSON.parse(localStorage.getItem(storageKey) || '{}');

        // Apply saved selections
        document.querySelectorAll('.tabbed-set').forEach((tabSet, setIndex) => {
            const savedTab = savedSelections[setIndex];
            if (savedTab !== undefined) {
                const input = tabSet.querySelector(`input[id$="-${savedTab}"]`);
                if (input) {
                    input.checked = true;
                }
            }
        });

        // Save selections on change
        document.querySelectorAll('.tabbed-set input[type="radio"]').forEach((input, index) => {
            input.addEventListener('change', () => {
                if (input.checked) {
                    // Find which set this belongs to
                    const tabSet = input.closest('.tabbed-set');
                    const setIndex = Array.from(document.querySelectorAll('.tabbed-set')).indexOf(tabSet);

                    // Find which tab within the set
                    const tabInputs = Array.from(tabSet.querySelectorAll('input[type="radio"]'));
                    const tabIndex = tabInputs.indexOf(input);

                    // Save to localStorage
                    savedSelections[setIndex] = tabIndex;
                    localStorage.setItem(storageKey, JSON.stringify(savedSelections));
                }
            });
        });
    }

    // ========================================
    // Reading Progress Indicator
    // ========================================

    function addReadingProgress() {
        // Create progress bar
        const progressBar = document.createElement('div');
        progressBar.id = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: var(--md-accent-fg-color);
            z-index: 1000;
            transition: width 0.2s ease;
        `;
        document.body.appendChild(progressBar);

        // Update progress on scroll
        const updateProgress = debounce(() => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            const progress = (scrollTop / (documentHeight - windowHeight)) * 100;
            progressBar.style.width = Math.min(progress, 100) + '%';
        }, 10);

        window.addEventListener('scroll', updateProgress);
        updateProgress();
    }

    // ========================================
    // Back to Top Button
    // ========================================

    function addBackToTop() {
        const button = document.createElement('button');
        button.id = 'back-to-top';
        button.innerHTML = '↑';
        button.title = 'Back to top';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--md-primary-fg-color);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 24px;
            display: none;
            z-index: 999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        `;

        button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.1)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });

        document.body.appendChild(button);

        // Show/hide based on scroll position
        const toggleButton = debounce(() => {
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        }, 100);

        window.addEventListener('scroll', toggleButton);
    }

    // ========================================
    // Search Keyboard Shortcut
    // ========================================

    function enableSearchShortcut() {
        document.addEventListener('keydown', (e) => {
            // Cmd/Ctrl + K or / to focus search
            if ((e.metaKey || e.ctrlKey) && e.key === 'k' || e.key === '/') {
                e.preventDefault();
                const searchInput = document.querySelector('.md-search__input');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // Escape to close search
            if (e.key === 'Escape') {
                const searchInput = document.querySelector('.md-search__input');
                if (searchInput && document.activeElement === searchInput) {
                    searchInput.blur();
                }
            }
        });
    }

    // ========================================
    // Print Optimization
    // ========================================

    function optimizePrint() {
        window.addEventListener('beforeprint', () => {
            // Expand all details/summary elements
            document.querySelectorAll('details').forEach(detail => {
                detail.setAttribute('open', '');
            });
        });
    }

    // ========================================
    // Performance Monitoring
    // ========================================

    function logPerformance() {
        if (window.performance && console.table) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    if (perfData) {
                        console.log('📊 Page Performance:');
                        console.table({
                            'DOM Content Loaded': Math.round(perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart) + 'ms',
                            'Page Load': Math.round(perfData.loadEventEnd - perfData.loadEventStart) + 'ms',
                            'Total Load Time': Math.round(perfData.loadEventEnd - perfData.fetchStart) + 'ms'
                        });
                    }
                }, 0);
            });
        }
    }

    // ========================================
    // MkDocs Build Control Toggle
    // ========================================

    const BUILD_CONTROL_URL = 'http://localhost:8001';

    async function addBuildControlToggle() {
        // First check if Build Control Server is available
        const serverAvailable = await checkBuildStatus();

        if (!serverAvailable) {
            // Server not available - don't show UI, no errors
            console.log('ℹ️ Build Control Server not available - feature disabled');
            return;
        }

        console.log('✅ Build Control Server available - enabling toggle');

        const storageKey = 'advlib-build-enabled';

        // Get saved preference (default: enabled)
        let buildEnabled = localStorage.getItem(storageKey) !== 'false';

        // Sync with server status
        if (serverAvailable.paused !== undefined) {
            buildEnabled = !serverAvailable.paused;
            localStorage.setItem(storageKey, buildEnabled.toString());
        }

        // Create toggle container
        const toggleContainer = document.createElement('div');
        toggleContainer.id = 'build-control-toggle-container';
        toggleContainer.title = 'MkDocs HTML-Build ein-/ausschalten';

        // Create toggle checkbox
        const toggleCheckbox = document.createElement('input');
        toggleCheckbox.type = 'checkbox';
        toggleCheckbox.id = 'build-control-toggle';
        toggleCheckbox.checked = buildEnabled;

        // Create label
        const toggleLabel = document.createElement('label');
        toggleLabel.htmlFor = 'build-control-toggle';
        toggleLabel.className = 'build-control-toggle-label';

        // Create icon/text
        const toggleText = document.createElement('span');
        toggleText.className = 'build-control-toggle-text';
        toggleText.innerHTML = '🔨';
        toggleText.title = 'HTML-Build ' + (buildEnabled ? 'aktiviert' : 'pausiert');

        // Create status indicator
        const statusDot = document.createElement('span');
        statusDot.className = 'build-control-status-dot';
        statusDot.style.cssText = `
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: ${buildEnabled ? '#4caf50' : '#ff9800'};
            margin-left: 8px;
        `;

        toggleLabel.appendChild(toggleCheckbox);
        toggleLabel.appendChild(toggleText);
        toggleLabel.appendChild(statusDot);
        toggleContainer.appendChild(toggleLabel);

        // Add to document
        document.body.appendChild(toggleContainer);

        // Handle toggle change
        toggleCheckbox.addEventListener('change', async () => {
            buildEnabled = toggleCheckbox.checked;
            localStorage.setItem(storageKey, buildEnabled);

            // Send request to control server
            try {
                const endpoint = buildEnabled ? '/resume' : '/pause';
                const response = await fetch(BUILD_CONTROL_URL + endpoint, {
                    method: 'POST',
                    mode: 'cors'
                });

                if (response.ok) {
                    const data = await response.json();
                    updateToggleUI(buildEnabled, toggleText, statusDot);
                    showNotification(
                        buildEnabled
                            ? '🟢 HTML-Build aktiviert - Dokumentation wird aktualisiert'
                            : '🟡 HTML-Build pausiert - LLM-Generierung läuft weiter'
                    );
                    console.log('Build Control:', data.message);
                } else {
                    throw new Error('Server nicht erreichbar');
                }
            } catch (error) {
                console.error('Build Control Server Error:', error);
                showNotification(
                    '⚠️ Build Control Server nicht erreichbar!\n' +
                    'Starte: python mkdocs_build_control.py',
                    5000
                );
                // Revert checkbox
                toggleCheckbox.checked = !buildEnabled;
                buildEnabled = !buildEnabled;
                localStorage.setItem(storageKey, buildEnabled);
            }
        });
    }

    function updateToggleUI(enabled, toggleText, statusDot) {
        toggleText.title = 'HTML-Build ' + (enabled ? 'aktiviert' : 'pausiert');
        statusDot.style.backgroundColor = enabled ? '#4caf50' : '#ff9800';
    }

    async function checkBuildStatus() {
        try {
            const response = await fetch(BUILD_CONTROL_URL + '/status', {
                method: 'GET',
                mode: 'cors',
                signal: AbortSignal.timeout(2000)  // 2 second timeout
            });
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            // Server not available - this is normal if Build Control Server is not running
            // No error logging needed
        }
        return null;
    }

    function showNotification(message, duration = 3000) {
        // Remove any existing notification
        const existing = document.getElementById('build-control-notification');
        if (existing) {
            existing.remove();
        }

        // Create notification
        const notification = document.createElement('div');
        notification.id = 'build-control-notification';
        notification.className = 'build-control-notification';
        notification.textContent = message;

        document.body.appendChild(notification);

        // Trigger animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        // Remove after duration
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    }

    // ========================================
    // Initialize Everything
    // ========================================

    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🚀 AdvLib Documentation Enhanced');

        // Execute enhancements
        enhanceCodeBlocks();
        enableSmoothScroll();
        highlightTOC();
        markExternalLinks();
        rememberTabSelections();
        addReadingProgress();
        addBackToTop();
        addBuildControlToggle();
        enableSearchShortcut();
        optimizePrint();
        logPerformance();
    }

    // Start initialization
    init();

    // Re-run on page navigation (for SPA-like behavior)
    document.addEventListener('DOMContentLoaded', () => {
        const observer = new MutationObserver(() => {
            enhanceCodeBlocks();
            markExternalLinks();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });

})();
