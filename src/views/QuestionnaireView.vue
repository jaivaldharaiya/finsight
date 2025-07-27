<!-- src/views/QuestionnaireView.vue -->
<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="8">
        <v-card class="elevation-4">
          <v-card-title class="text-h5 text-center pa-4 bg-primary">
            Financial Persona Agent
          </v-card-title>

          <v-card-text class="pa-5">
            <!-- Chat message display window -->
            <div ref="chatWindow" class="chat-window mb-4">
              <div v-for="(msg, idx) in messages" :key="idx" :class="`message-row ${msg.role}`">
                <v-icon v-if="msg.role === 'bot'" class="mr-2" color="primary">mdi-robot-happy</v-icon>
                <div class="message-bubble pa-3">
                  <div v-if="msg.role === 'user'" class="user-message">
                    {{ msg.text }}
                  </div>
                  <div v-else class="bot-message" v-html="formatBotMessage(msg.text)"></div>
                </div>
                <v-icon v-if="msg.role === 'user'" class="ml-2" color="accent">mdi-account</v-icon>
              </div>
            </div>

            <!-- User input field with microphone icon -->
            <v-text-field
              v-model="userInput"
              label="Ask your financial question..."
              variant="solo"
              @keyup.enter="sendMessage"
              :disabled="loading"
              hide-details
            >
              <template v-slot:append-inner>
                <v-icon
                  @click="toggleListen"
                  :color="isListening ? 'red' : 'grey-darken-1'"
                  :class="{ 'blinking-icon': isListening }"
                >
                  mdi-microphone
                </v-icon>
              </template>
            </v-text-field>

            <!-- Send button -->
            <div class="text-center mt-4">
              <v-btn color="success" size="large" @click="sendMessage" :disabled="loading || !userInput">
                Send Message
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

const userInput = ref('')
const messages = ref([])
const loading = ref(false)
const chatWindow = ref(null) // Reference to the chat window div

// --- NEW: Refs for Voice-to-Text ---
const isListening = ref(false)
let recognition = null;

// --- NEW: Function for Text-to-Voice (Bot Speaking) ---
function speakBotResponse(text) {
  if (!('speechSynthesis' in window)) {
    console.error('Speech Synthesis not supported by this browser.');
    return;
  }
  // Stop any previous speech before starting a new one
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US'; // You can configure the voice
  utterance.rate = 1.0;
  window.speechSynthesis.speak(utterance);
}

// --- NEW: Function to format bot messages with LaTeX-like styling ---
function formatBotMessage(text) {
  if (!text) return '';
  
  // Split text into lines for better processing
  let lines = text.split('\n');
  let formatted = '';
  let inList = false;
  let listItems = [];
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].trim();
    
    if (!line) {
      // Empty line - close any open list and add spacing
      if (inList) {
        formatted += formatList(listItems);
        listItems = [];
        inList = false;
      }
      formatted += '<div class="spacing"></div>';
      continue;
    }
    
    // Check for headers
    if (line.startsWith('###')) {
      if (inList) {
        formatted += formatList(listItems);
        listItems = [];
        inList = false;
      }
      formatted += `<h3>${line.replace(/^###\s*/, '')}</h3>`;
    } else if (line.startsWith('##')) {
      if (inList) {
        formatted += formatList(listItems);
        listItems = [];
        inList = false;
      }
      formatted += `<h2>${line.replace(/^##\s*/, '')}</h2>`;
    } else if (line.startsWith('#')) {
      if (inList) {
        formatted += formatList(listItems);
        listItems = [];
        inList = false;
      }
      formatted += `<h1>${line.replace(/^#\s*/, '')}</h1>`;
    }
    // Check for bullet points (various formats)
    else if (line.match(/^[-•*]\s+/) || line.match(/^\d+\.\s+/)) {
      let content = line.replace(/^[-•*]\s+/, '').replace(/^\d+\.\s+/, '');
      listItems.push(content);
      inList = true;
    }
    // Regular paragraph
    else {
      if (inList) {
        formatted += formatList(listItems);
        listItems = [];
        inList = false;
      }
      formatted += `<p>${formatInlineElements(line)}</p>`;
    }
  }
  
  // Close any remaining list
  if (inList) {
    formatted += formatList(listItems);
  }
  
  return formatted;
}

// Helper function to format lists
function formatList(items) {
  if (items.length === 0) return '';
  
  let listHtml = '<ul class="formatted-list">';
  items.forEach(item => {
    listHtml += `<li>${formatInlineElements(item)}</li>`;
  });
  listHtml += '</ul>';
  return listHtml;
}

// Helper function to format inline elements (bold, italic, code)
function formatInlineElements(text) {
  return text
    // Convert **bold** to <strong>
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Convert *italic* to <em>
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Convert `code` to <code>
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Convert ```code blocks``` (though these should be handled at block level)
    .replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
}

// --- NEW: Function to start/stop listening to the user ---
function toggleListen() {
  if (isListening.value) {
    recognition.stop();
    isListening.value = false;
  } else {
    recognition.start();
    isListening.value = true;
  }
}

// --- NEW: Initialize Speech Recognition on component mount ---
onMounted(() => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.error('Speech Recognition not supported by this browser.');
    return;
  }
  
  recognition = new SpeechRecognition();
  recognition.continuous = false; // Stop listening after a pause
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  // Event handler for when speech is successfully recognized
  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
    isListening.value = false;
    // Automatically send the message after successful transcription
    sendMessage();
  };

  // Event handler for errors
  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    isListening.value = false;
  };

  // Ensure listening stops if ended unexpectedly
  recognition.onend = () => {
    isListening.value = false;
  }
});


// --- UPDATED: Function to send message to the API ---
async function sendMessage() {
  if (!userInput.value || loading.value) return;

  const userMessage = userInput.value;
  messages.value.push({ role: 'user', text: userMessage });
  userInput.value = ''; // Clear input immediately
  loading.value = true;

  // Scroll to the bottom of the chat window
  await nextTick();
  if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight;

  // Call your AI agent server on port 8000
  const url = 'http://localhost:8000/chat';

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userMessage, user_id: 'hackathon_user' })
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    const botResponse = data.response || data.message || 'Sorry, I could not process your request.';
    
    // Add the bot's response
    messages.value.push({ role: 'bot', text: botResponse });
    
    // Speak the response (without HTML formatting)
    const plainTextResponse = botResponse.replace(/<[^>]*>/g, '');
    speakBotResponse(plainTextResponse);

    // Auto-scroll to bottom
    await nextTick();
    if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight;

  } catch (err) {
    const errorText = 'Sorry, I encountered an error. Please try again.';
    messages.value.push({ role: 'bot', text: errorText });
    speakBotResponse(errorText);
    console.error('API call failed:', err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.chat-window {
  height: 400px; /* Increased height */
  overflow-y: auto;
  background: #f7f9fc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e0e0e0;
}

.message-row {
  display: flex;
  align-items: flex-end; /* Align to the bottom of the row */
  margin-bottom: 12px;
}

.message-row.user {
  justify-content: flex-end; /* User messages on the right */
}

.message-row.bot {
  justify-content: flex-start; /* Bot messages on the left */
}

.message-bubble {
  max-width: 70%;
  border-radius: 18px;
  word-wrap: break-word;
}

.user .message-bubble {
  background-color: #d1eaff; /* Light blue for user */
}

.bot .message-bubble {
  background-color: #ffffff; /* White for bot */
  border: 1px solid #e0e0e0;
}

/* Bot message formatting - LaTeX-like styling */
.bot-message {
  line-height: 1.7;
  font-family: 'Times New Roman', serif;
  font-size: 15px;
  color: #2c3e50;
  text-align: justify;
}

.bot-message h1, .bot-message h2, .bot-message h3 {
  margin: 20px 0 12px 0;
  font-weight: 700;
  color: #1565c0;
  font-family: 'Arial', sans-serif;
}

.bot-message h1 { 
  font-size: 1.6em; 
  border-bottom: 2px solid #1565c0;
  padding-bottom: 5px;
}
.bot-message h2 { 
  font-size: 1.4em; 
  border-bottom: 1px solid #1976d2;
  padding-bottom: 3px;
}
.bot-message h3 { 
  font-size: 1.2em; 
  color: #1976d2;
}

.bot-message p {
  margin: 12px 0;
  text-indent: 0;
  line-height: 1.8;
}

.bot-message .spacing {
  height: 16px;
}

.bot-message .formatted-list {
  margin: 16px 0;
  padding-left: 0;
  list-style: none;
}

.bot-message .formatted-list li {
  margin: 8px 0;
  padding-left: 25px;
  position: relative;
  line-height: 1.7;
  text-align: justify;
}

.bot-message .formatted-list li::before {
  content: "•";
  color: #1565c0;
  font-weight: bold;
  font-size: 1.2em;
  position: absolute;
  left: 8px;
  top: -2px;
}

.bot-message strong {
  font-weight: 700;
  color: #0d47a1;
  font-family: 'Arial', sans-serif;
}

.bot-message em {
  font-style: italic;
  color: #424242;
  font-family: 'Times New Roman', serif;
}

.bot-message code {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 3px 8px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  color: #e83e8c;
}

.bot-message pre {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bot-message pre code {
  background: none;
  border: none;
  padding: 0;
  display: block;
  white-space: pre;
  color: #495057;
  font-size: 0.9em;
}

.user-message {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  font-size: 14px;
}

/* --- NEW: Blinking animation for the microphone icon --- */
.blinking-icon {
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.3; }
  100% { opacity: 1; }
}
</style>