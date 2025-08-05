fetch('https://u2l5m8yrz4.execute-api.us-east-1.amazonaws.com/Prod/put')
    .then(() => fetch('https://u2l5m8yrz4.execute-api.us-east-1.amazonaws.com/Prod/get'))
    .then(response => response.json())
    .then(data => {
        document.getElementById('visitorCount').innerText = data['counter']
})


    
// Chatbot UI toggle
document.addEventListener('DOMContentLoaded', function() {
        const header = document.getElementById('chatbot-header');
        const body = document.getElementById('chatbot-body');
        header.onclick = () => body.style.display = body.style.display === 'none' ? 'block' : 'none';
    
        // Chatbot logic
        const messages = document.getElementById('chatbot-messages');
        const input = document.getElementById('chatbot-input');
        const send = document.getElementById('chatbot-send');
    
        let visitorNumber = null;
        let greeted = false;
        let guestBookStep = 0;
    
        // Wait for visitor counter to load
        function checkVisitorCount() {
            const countElem = document.getElementById('visitorCount');
            if (countElem && countElem.textContent !== 'loading...') {
                visitorNumber = countElem.textContent.trim();
                if (!greeted) {
                    addBotMessage("👋 Hi! I'm Ian's Guest Greeter bot. I use a combination of deterministic code and non-deterministic LLM injection in my responses.");
                    addBotMessage(`You are guest #${visitorNumber}. Would you like to be added to the Guest Book? (yes/no)`);
                    greeted = true;
                }
            } else {
                setTimeout(checkVisitorCount, 500);
            }
        }
        checkVisitorCount();
    
        function addBotMessage(text) {
            const msg = document.createElement('div');
            msg.style.margin = '10px 0';
            msg.innerHTML = `<b>Greeter:</b> ${text}`;
            messages.appendChild(msg);
            messages.scrollTop = messages.scrollHeight;
        }
    
        function addUserMessage(text) {
            const msg = document.createElement('div');
            msg.style.margin = '10px 0';
            msg.style.textAlign = 'right';
            msg.innerHTML = `<b>You:</b> ${text}`;
            messages.appendChild(msg);
            messages.scrollTop = messages.scrollHeight;
        }
    
        send.onclick = handleUserInput;
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') handleUserInput();
        });
    
        function handleUserInput() {
            const text = input.value.trim();
            if (!text) return;
            addUserMessage(text);
            input.value = '';

            // Guest Book logic
            if (guestBookStep === 0) {
                if (/^y(es)?$/i.test(text)) {
                    addBotMessage("Great! What's your name? First name and last initial is fine.");
                    guestBookStep = 1;
                } else {
                    addBotMessage("No problem! Let me know if you have any questions about Ian's resume.");
                    guestBookStep = -1;
                }
            } else if (guestBookStep === 1) {
                // Save name, ask for role/title
                window.guestName = text;
                addBotMessage("Thanks! What is your current role or title?");
                guestBookStep = 2;
            } else if (guestBookStep === 2) {
                let role = text;
                // Send to backend
                fetch('https://YOUR_BACKEND_API/guestbook', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        name: window.guestName,
                        role: role,
                        visitorNumber: visitorNumber
                    })
                }).then(() => {
                    addBotMessage("You're on the guest book! 🎉 Thank you for visiting.");
                }).catch(() => {
                    addBotMessage("Sorry, the Guest Book is currently unavailable. Your information was not stored.");
                });
                guestBookStep = -1;
            } else {
                // Optionally, send to LLM for general Q&A
                fetch('https://YOUR_BACKEND_API/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                })
                .then(res => res.json())
                .then(data => addBotMessage(data.reply))
                .catch(() => addBotMessage("Sorry, I couldn't process that."));
            }
        }
    });