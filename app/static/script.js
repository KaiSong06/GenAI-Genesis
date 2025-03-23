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
        "Speaker 1": "green",
        "FinalSay AI": "grey"
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

    
    recordButton.addEventListener('click', function () {
        isRecording = !isRecording;
        recordButton.textContent = isRecording ? 'End Recording' : 'Record';
        recordButton.style.backgroundColor = isRecording ? 'red' : '#10a37f';

        if (isRecording) {
            loadConversation();  
        } 
    });

    function addMessage(text, speaker, logElement) {
        
            const messageContainer = document.createElement('div');
            messageContainer.style.margin = '10px 0';
            messageContainer.style.display = 'flex';
        
            
            const messageBox = document.createElement('div');
            messageBox.classList.add('message');
            messageBox.textContent = text;
            messageBox.style.color = 'white';
            messageBox.style.backgroundColor = speakerColors[speaker] || 'gray';
            messageBox.style.fontSize = '3.5rem';
            messageBox.style.padding = '15px 20px';
            messageBox.style.borderRadius = '10px';
            messageBox.style.wordWrap = 'break-word';
            messageBox.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
            messageBox.style.display = 'inline-block'; 
            messageBox.style.maxWidth = '180%';
            messageBox.style.whiteSpace = 'normal';
            
            
            messageContainer.appendChild(messageBox); 
            logElement.appendChild(messageContainer);
            logElement.scrollTop = logElement.scrollHeight;
        }

    feedbackButton.addEventListener('click', function () {
        const feedbackText = "FinalSay AI: "+"concatenate here";
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
