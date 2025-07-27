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

  // IMPORTANT SECURITY NOTE: See below
  const url = 'https://us-central1-aiplatform.googleapis.com/v1/projects/driven-edition-467110-p6/locations/us-central1/reasoningEngines/8728635784820686848:streamQuery?alt=sse';
  const bearerToken = 'ya29.a0AS3H6NzYPIQgI3Pv5GIJsdbBPJJa-e8gaU4pZiY1on_eVtTghDW6fspUKi5QXdDQPZ3qwD_yI_lXwV2Og1c64hjByN_uhFf20JsAX1-zixluLdjROLSXLbvOHcEdXCwkphywkc6tUJaaRPXoYZ6rL57NA65PnIPBPDrwRDfZA1qBdQaCgYKAVcSARMSFQHGX2Mi5gUSfEZ1ogC3emwxY-46zg0181';

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${bearerToken}`
      },
      body: JSON.stringify({ input: { message: userMessage, user_id: 'hackathon_user' }})
    });

    if (!response.ok || !response.body) throw new Error(`HTTP error! status: ${response.status}`);
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let botMsg = '';
    let botMsgIndex = -1;

    // Add a placeholder for the bot's message
    messages.value.push({ role: 'bot', text: '...' });
    botMsgIndex = messages.value.length - 1;

    // Stream the response
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      // Clean up SSE data format which might look like "data: {...}"
      const cleanedChunk = chunk.replace(/^data: /, '').trim();
      if(cleanedChunk) botMsg += cleanedChunk;

      messages.value[botMsgIndex].text = botMsg + '...';

      // Auto-scroll as message comes in
      await nextTick();
      if(chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
    }

    // Finalize the bot message
    messages.value[botMsgIndex].text = botMsg;
    // --- NEW: Speak the final response ---
    speakBotResponse(botMsg);

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