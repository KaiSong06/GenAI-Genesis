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
document.addEventListener("DOMContentLoaded", function() {
    fetch("/get_conversation")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error loading conversation:", data.error);
                return;
            }
            const latestConversation = data[data.length - 1];
            if (latestConversation && latestConversation.messages) {
                // Process and display the conversation
                console.log(latestConversation.messages);
            } else {
                console.error("No conversation messages found.");
            }
        })
        .catch(error => console.error("Error loading conversation:", error));
});

document.getElementById("record").addEventListener("click", function() {
    
    
    const audioFile = document.getElementById("audioInput").files[0];
    if (!audioFile) {
        console.error("Audio file is required");
        return;
    }

    const formData = new FormData();
    formData.append("audio", audioFile);

    fetch("/transcribe", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error transcribing audio:", data.error);
            return;
        }
        console.log("Transcription:", data);
    })
    .catch(error => console.error("Error transcribing audio:", error));
});
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
            fetch('/transcribe', { method: 'POST' })
                .then(response => console.log("Recording started:", response))
                .catch(error => console.error("Error starting recording:", error));
                loadConversation();
        } else {
            // Recording just ended, process the conversation
            fetch('/process_conversation', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Conversation processed:", data);
                // Optional: You could automatically display feedback here
                // or just let the user click the feedback button
            })
            .catch(error => console.error("Error processing conversation:", error));
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
        fetch('/get_feedback')
            .then(response => response.json())
            .then(data => {
                // Check if feedback exists in the response
                const feedbackText = data.feedback || "No feedback available.";
                
                // Display the feedback in the AI log
                addMessage(feedbackText, 'FinalSay AI', aiLog);
            })
            .catch(error => {
                console.error("Error fetching feedback:", error);
                addMessage("Error fetching feedback. Please try again.", 'FinalSay AI', aiLog);
            });
    });

    clearChatButton.addEventListener('click', function () {
        fetch('/clear_conversation', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log("Chat history cleared:", data);
                chatLog.innerHTML = "";
                aiLog.innerHTML = ""
            })
            .catch(error => console.error("Error clearing chat history:", error));
    });
});