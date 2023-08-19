const API_KEY = "PASTE-YOUR-API-KEY-HERE"; // Paste your API key here

const themeButton = document.getElementById("theme-btn");
const chatInput = document.getElementById("chat-input");
const chatContainer = document.querySelector(".chat-container");
const sendButton = document.getElementById("send-btn");
const clearButton = document.getElementById("clear-btn");
const saveButton = document.getElementById("save-btn");

const CHAT_WITH_BOT_URL = '/path/to/tasklist/';


const initialInputHeight = chatInput.scrollHeight;
let userText = null;

const createChatElement = (content, className) => {
    // Create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv; // Return the created chat div
}

const getChatResponse = async (incomingChatDiv) => {
    const pElement = document.createElement("p");

    const data = {
        model: "gpt-3.5-turbo",
        messages: [
            {
                role: "user",
                content: `some random prompt`,
            },
        ],
        temperature: 1.0,
    };

    try {
        const res = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + API_KEY,
            },
            body: JSON.stringify(data),
        });

        const outputData = await res.json();
        pElement.textContent = outputData.choices[0].message.content;
    } catch (e) {
        console.log(e);
        pElement.classList.add("error");
        pElement.textContent = "Sorry, I'm having trouble reaching the OpenAI API at the moment.";
    }

    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);

};

/**
 * send chat and display in container
 */
 const handleOutgoingChat = () => {
    userText = chatInput.value.trim(); // Get chatInput value and remove extra spaces
    if (!userText.trim()) {
        return;
    } // If chatInput is empty return from here

    // Clear the input field and reset its height
    chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;

    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="images/user.jpg" alt="user-img">
                        <p>${userText}</p>
                    </div>
                </div>`;

    // Create an outgoing chat div with user's message and append it to chat container
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);

    // Send user input to the server
    fetch(CHAT_WITH_BOT_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token from cookies
        },
        body: new URLSearchParams({
            user_input: userText,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle bot response here
        const botResponseHtml = `<div class="chat-content">
                                    <div class="chat-details">
                                        <img src="images/chatbot.jpg" alt="chatbot-img">
                                        <p>${data.bot_response}</p>
                                    </div>
                                </div>`;

        const incomingChatDiv = createChatElement(botResponseHtml, "incoming");
        chatContainer.appendChild(incomingChatDiv);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    })
    .catch(error => {
        console.error(error);
        
    });
}

/**
 * Sets up the page, adding event listeners and initial values.
 * Called after the page has loaded.
 */
function init() {
    // Add event listeners to buttons
    //themeButton.addEventListener("click", toggleLightMode);
    sendButton.addEventListener("click", handleOutgoingChat);
    //clearButton.addEventListener("click", clear);
    //saveButton.addEventListener("click", saveHandler);
    //saveButton.addEventListener("click", save);

    //displayChatNames()
    //loadLocalStorage();
    //displayChatNames();
}


addEventListener('DOMContentLoaded', init);
