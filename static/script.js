document.addEventListener('DOMContentLoaded', function () {
  const recordButton = document.getElementById('record');
  const chatLog = document.getElementById('chat-log');
  const aiLog = document.getElementById('ai-log');
  const feedbackButton = document.getElementById('give-feedback');
  const clearChatButton = document.getElementById('clear-chat');

  let isRecording = false;
  let speakers = ['Speaker 1', 'Speaker 2'];
  let currentSpeakerIndex = 0;

  const speakerColors = {
      "Speaker 1": "lightblue",
      "Speaker 2": "lightgreen"
  };

  // Load conversation when recording starts
  function loadConversation() {
      fetch('/get_conversation')
          .then(response => response.json())
          .then(data => {
              chatLog.innerHTML = '';  // Clear chat log before loading

              if (data.length === 0) {
                  chatLog.innerHTML = "<p>No previous conversation found.</p>";
                  return;
              }

              // Get the latest conversation
              const latestConversation = data[data.length - 1];

              latestConversation.messages.forEach(msg => {
                  addMessage(msg.text, msg.speaker, chatLog);
              });
          })
          .catch(error => console.error("Error loading conversation:", error));
  }

  // Toggle Recording
  recordButton.addEventListener('click', function () {
      isRecording = !isRecording;
      recordButton.textContent = isRecording ? 'End Recording' : 'Record';
      recordButton.style.backgroundColor = isRecording ? 'red' : '#10a37f';

      if (isRecording) {
          loadConversation();  // Start pulling conversation
      }
  });

  function addMessage(text, speaker, logElement) {
      const messageBox = document.createElement('div');
      messageBox.classList.add('message');
      messageBox.textContent = text;
      messageBox.style.color = 'white';
      messageBox.style.backgroundColor = speakerColors[speaker] || 'gray';
      messageBox.style.padding = '8px';
      messageBox.style.borderRadius = '5px';
      messageBox.style.margin = '5px 0';
      logElement.appendChild(messageBox);
      logElement.scrollTop = logElement.scrollHeight; // Auto-scroll
  }

  function switchSpeaker() {
      currentSpeakerIndex = (currentSpeakerIndex + 1) % speakers.length;
  }

  feedbackButton.addEventListener('click', function () {
      const feedbackText = "AI Feedback: Your argument was logical, but could use more supporting evidence.";
      addMessage(feedbackText, 'AI', aiLog);
  });

  clearChatButton.addEventListener('click', function () {
      fetch('/clear_conversation', { method: 'POST' })
          .then(response => response.json())
          .then(data => {
              console.log("Chat history cleared:", data);
              chatLog.innerHTML = "";
              aiLog.innerHTML = "";
          })
          .catch(error => console.error("Error clearing chat history:", error));
  });
});
