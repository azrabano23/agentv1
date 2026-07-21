// Global variables
let isInitialized = false;
let isLoading = false;

// DOM elements
const statusIndicator = document.getElementById('statusIndicator');
const statusDot = statusIndicator.querySelector('.status-dot');
const statusText = statusIndicator.querySelector('.status-text');
const welcomeSection = document.getElementById('welcomeSection');
const chatContainer = document.getElementById('chatContainer');
const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const loadingModal = document.getElementById('loadingModal');
const loadingText = document.getElementById('loadingText');
const questionChips = document.getElementById('questionChips');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkStatus();
    loadSampleQuestions();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Enter key to send message
    questionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
        }
    });

    // Input validation
    questionInput.addEventListener('input', function() {
        sendButton.disabled = !this.value.trim();
    });
}

// Check agent status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        updateStatusIndicator(status);
        
        if (status.is_initialized) {
            isInitialized = true;
            showChatInterface();
        }
    } catch (error) {
        console.error('Error checking status:', error);
        updateStatusIndicator({ error: 'Connection failed' });
    }
}

// Update status indicator
function updateStatusIndicator(status) {
    if (status.error) {
        statusDot.className = 'status-dot error';
        statusText.textContent = 'Error';
    } else if (status.is_initialized) {
        statusDot.className = 'status-dot ready';
        statusText.textContent = 'Ready';
    } else {
        statusDot.className = 'status-dot';
        statusText.textContent = 'Initializing...';
    }
}

// Load sample questions
async function loadSampleQuestions() {
    try {
        const response = await fetch('/api/sample-questions');
        const data = await response.json();
        
        if (data.success) {
            displaySampleQuestions(data.questions);
        }
    } catch (error) {
        console.error('Error loading sample questions:', error);
    }
}

// Display sample questions
function displaySampleQuestions(questions) {
    questionChips.innerHTML = '';
    
    questions.forEach(question => {
        const chip = document.createElement('button');
        chip.className = 'question-chip';
        chip.textContent = question;
        chip.onclick = () => {
            questionInput.value = question;
            sendButton.disabled = false;
        };
        questionChips.appendChild(chip);
    });
}

// Initialize agent
async function initializeAgent() {
    if (isLoading) return;
    
    isLoading = true;
    showLoadingModal('Initializing knowledge base...');
    
    try {
        const response = await fetch('/api/initialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ force_refresh: false })
        });
        
        const data = await response.json();
        
        if (data.success) {
            isInitialized = true;
            updateStatusIndicator({ is_initialized: true });
            showChatInterface();
            addMessage('assistant', 'Yo! I\'m live and ready to tell you about Azra. What\'s up? 🔥');
        } else {
            throw new Error(data.message || 'Initialization failed');
        }
    } catch (error) {
        console.error('Error initializing agent:', error);
        addMessage('assistant', 'Sorry, I encountered an error during initialization. Please try refreshing the page.');
    } finally {
        hideLoadingModal();
        isLoading = false;
    }
}

// Show chat interface
function showChatInterface() {
    welcomeSection.style.display = 'none';
    chatContainer.style.display = 'flex';
    questionInput.focus();
}

// Ask question
async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question || isLoading) return;
    
    // Add user message
    addMessage('user', question);
    
    // Clear input
    questionInput.value = '';
    sendButton.disabled = true;
    
    // Show loading state
    isLoading = true;
    sendButton.disabled = true;
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('assistant', data.answer, data.sources, data.confidence);
        } else {
            throw new Error(data.message || 'Failed to get answer');
        }
    } catch (error) {
        console.error('Error asking question:', error);
        addMessage('assistant', 'Sorry, I encountered an error while processing your question. Please try again.');
    } finally {
        isLoading = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
}

// Add message to chat
function addMessage(type, content, sources = [], confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    // Add sources if available
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'message-sources';
        
        sources.forEach(source => {
            const sourceTag = document.createElement('span');
            sourceTag.className = 'source-tag';
            sourceTag.textContent = `${source.source} (${source.type})`;
            sourcesDiv.appendChild(sourceTag);
        });
        
        messageContent.appendChild(sourcesDiv);
    }
    
    // Add confidence indicator
    if (confidence) {
        const confidenceDiv = document.createElement('div');
        confidenceDiv.className = 'message-sources';
        confidenceDiv.innerHTML = `<span class="source-tag">Confidence: ${confidence}</span>`;
        messageContent.appendChild(confidenceDiv);
    }
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Refresh knowledge base
async function refreshKnowledgeBase() {
    if (isLoading) return;
    
    isLoading = true;
    showLoadingModal('Refreshing knowledge base...');
    
    try {
        const response = await fetch('/api/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('assistant', 'Knowledge base refreshed! I\'m now loaded with the latest info about Azra. Let\'s go! 🚀');
        } else {
            throw new Error(data.message || 'Refresh failed');
        }
    } catch (error) {
        console.error('Error refreshing knowledge base:', error);
        addMessage('assistant', 'Sorry, I encountered an error while refreshing the knowledge base. Please try again.');
    } finally {
        hideLoadingModal();
        isLoading = false;
    }
}

// Show loading modal
function showLoadingModal(text = 'Loading...') {
    loadingText.textContent = text;
    loadingModal.classList.add('show');
}

// Hide loading modal
function hideLoadingModal() {
    loadingModal.classList.remove('show');
}

// Utility function to format confidence
function formatConfidence(confidence) {
    const confidenceMap = {
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low'
    };
    return confidenceMap[confidence] || confidence;
}

// Auto-resize textarea (if needed in future)
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Handle window resize
window.addEventListener('resize', function() {
    // Adjust chat container height on mobile
    if (window.innerWidth <= 768) {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
});

// Export functions for global access
window.initializeAgent = initializeAgent;
window.askQuestion = askQuestion;
window.refreshKnowledgeBase = refreshKnowledgeBase;
