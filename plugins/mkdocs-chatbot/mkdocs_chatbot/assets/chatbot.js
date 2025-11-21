/**
 * MkDocs ChatBot - Client-side implementation
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatBot);
    } else {
        initChatBot();
    }

    function initChatBot() {
        const config = window.CHATBOT_CONFIG || {};

        // Validate configuration - API key is optional for local LLM servers
        const isLocalServer = config.apiBaseUrl && !config.apiBaseUrl.includes('api.openai.com');
        if (!config.apiKey && !isLocalServer) {
            console.warn('ChatBot: No API key configured. Plugin will not function.');
            return;
        }

        const elements = {
            toggleBtn: document.getElementById('chatbot-toggle-btn'),
            closeBtn: document.getElementById('chatbot-close-btn'),
            window: document.getElementById('chatbot-window'),
            messages: document.getElementById('chatbot-messages'),
            input: document.getElementById('chatbot-input'),
            sendBtn: document.getElementById('chatbot-send-btn'),
            title: document.getElementById('chatbot-title')
        };

        // Check if all elements exist
        if (!Object.values(elements).every(el => el)) {
            console.error('ChatBot: Required DOM elements not found');
            return;
        }

        // State
        let conversationHistory = [];
        let isProcessing = false;

        // Initialize UI
        initializeUI();

        // Event listeners
        elements.toggleBtn.addEventListener('click', openChat);
        elements.closeBtn.addEventListener('click', closeChat);
        elements.sendBtn.addEventListener('click', sendMessage);
        elements.input.addEventListener('keydown', handleInputKeydown);
        elements.input.addEventListener('input', autoResizeTextarea);

        function initializeUI() {
            // Set colors
            elements.toggleBtn.style.backgroundColor = config.buttonColor;
            elements.toggleBtn.style.color = config.buttonTextColor;

            // Set title
            elements.title.textContent = config.chatTitle;

            // Set placeholder
            elements.input.placeholder = config.placeholderText;

            // Set position
            const container = document.getElementById('mkdocs-chatbot-container');
            container.classList.add(`position-${config.position}`);

            // Add welcome message
            if (config.welcomeMessage) {
                addMessage('assistant', config.welcomeMessage);
            }
        }

        function openChat() {
            elements.window.classList.remove('chatbot-hidden');
            elements.toggleBtn.classList.add('chatbot-hidden');
            elements.input.focus();
        }

        function closeChat() {
            elements.window.classList.add('chatbot-hidden');
            elements.toggleBtn.classList.remove('chatbot-hidden');
        }

        function handleInputKeydown(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        }

        function autoResizeTextarea() {
            elements.input.style.height = 'auto';
            elements.input.style.height = Math.min(elements.input.scrollHeight, 120) + 'px';
        }

        async function sendMessage() {
            const message = elements.input.value.trim();

            if (!message || isProcessing) {
                return;
            }

            // Clear input
            elements.input.value = '';
            elements.input.style.height = 'auto';

            // Add user message to UI
            addMessage('user', message);

            // Add to conversation history
            conversationHistory.push({
                role: 'user',
                content: message
            });

            // Show typing indicator
            const typingId = addTypingIndicator();
            isProcessing = true;

            try {
                // Call OpenAI API
                const response = await callOpenAI(conversationHistory);

                // Remove typing indicator
                removeTypingIndicator(typingId);

                // Add assistant message
                addMessage('assistant', response);

                // Add to conversation history
                conversationHistory.push({
                    role: 'assistant',
                    content: response
                });

            } catch (error) {
                console.error('ChatBot error:', error);
                removeTypingIndicator(typingId);
                addMessage('error', 'Sorry, I encountered an error. Please try again.');
            } finally {
                isProcessing = false;
            }
        }

        async function callOpenAI(messages) {
            // Check if backend API is available (for RAG/MCP tools)
            const useBackendAPI = config.enableRag || config.enableMcpTools || config.enableN8n;

            if (useBackendAPI) {
                return await callBackendAPI(messages);
            }

            // Original direct OpenAI call
            // Prepare messages with system prompt
            const apiMessages = [
                {
                    role: 'system',
                    content: config.systemPrompt + '\n\nCurrent page: ' + config.currentPage.title
                },
                ...messages
            ];

            // Build API endpoint URL
            const apiUrl = `${config.apiBaseUrl}/chat/completions`;

            // Build headers - only add Authorization if API key is provided
            const headers = {
                'Content-Type': 'application/json'
            };
            if (config.apiKey) {
                headers['Authorization'] = `Bearer ${config.apiKey}`;
            }

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    model: config.model,
                    messages: apiMessages,
                    temperature: config.temperature,
                    max_tokens: config.maxTokens
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error?.message || 'API request failed');
            }

            const data = await response.json();
            return data.choices[0].message.content;
        }

        async function callBackendAPI(messages) {
            // Call enhanced backend API with RAG/MCP tools/n8n
            const apiUrl = `http://${config.apiServerHost}:${config.apiServerPort}/api/query`;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: messages[messages.length - 1].content,
                    page_context: config.currentPage,
                    conversation_history: messages.slice(0, -1)  // All except last message
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Backend API request failed');
            }

            const data = await response.json();

            // Display sources if available
            if (data.sources && data.sources.length > 0) {
                displaySources(data.sources);
            }

            return data.response;
        }

        function displaySources(sources) {
            // Display RAG sources in the chat
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'chatbot-message chatbot-message-assistant chatbot-sources';
            sourcesDiv.innerHTML = `
                <div class="chatbot-message-content">
                    <details>
                        <summary>📚 Sources (${sources.length})</summary>
                        <ul class="chatbot-sources-list">
                            ${sources.map((source, i) => `
                                <li>
                                    <strong>${source.metadata.title || `Source ${i + 1}`}</strong><br>
                                    ${source.content}<br>
                                    <small>Relevance: ${(source.score * 100).toFixed(0)}%</small>
                                </li>
                            `).join('')}
                        </ul>
                    </details>
                </div>
            `;
            elements.messages.appendChild(sourcesDiv);
            elements.messages.scrollTop = elements.messages.scrollHeight;
        }

        function addMessage(type, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chatbot-message chatbot-message-${type}`;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'chatbot-message-content';

            if (type === 'assistant' || type === 'error') {
                // Render markdown for assistant messages
                contentDiv.innerHTML = renderMarkdown(content);
            } else {
                contentDiv.textContent = content;
            }

            messageDiv.appendChild(contentDiv);
            elements.messages.appendChild(messageDiv);

            // Scroll to bottom
            elements.messages.scrollTop = elements.messages.scrollHeight;
        }

        function addTypingIndicator() {
            const id = 'typing-' + Date.now();
            const typingDiv = document.createElement('div');
            typingDiv.id = id;
            typingDiv.className = 'chatbot-message chatbot-message-assistant';
            typingDiv.innerHTML = `
                <div class="chatbot-message-content">
                    <div class="chatbot-typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            `;
            elements.messages.appendChild(typingDiv);
            elements.messages.scrollTop = elements.messages.scrollHeight;
            return id;
        }

        function removeTypingIndicator(id) {
            const indicator = document.getElementById(id);
            if (indicator) {
                indicator.remove();
            }
        }

        function renderMarkdown(text) {
            // Simple markdown rendering (you can replace with a library like marked.js for full support)
            return text
                // Code blocks
                .replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code>$2</code></pre>')
                // Inline code
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                // Bold
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                // Italic
                .replace(/\*(.+?)\*/g, '<em>$1</em>')
                // Links
                .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
                // Line breaks
                .replace(/\n/g, '<br>');
        }
    }
})();
