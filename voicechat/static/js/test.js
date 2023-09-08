const API_KEY = "PASTE-YOUR-API-KEY-HERE"; // Paste your API key here

const themeButton = document.getElementById("theme-btn");
const chatInput = document.getElementById("chat-input");
const chatContainer = document.querySelector(".chat-container");
const hisContainer = document.querySelector(".history-container");
const sendButton = document.getElementById("send-btn");
const clearButton = document.getElementById("clear-btn");
const saveButton = document.getElementById("save-btn");
const newChatBox = document.getElementById("new-chat-box");



const initialInputHeight = chatInput.scrollHeight;
let userText = null;

/**
 * LOAD LOCAL STORAGE
 */
function loadLocalStorage() {
    const defaultText =
        `<div class="default-text">
            <h1>ChatGPT ......</h1>
                <p>Start a conversation and explore the power of AI.<br> Your chat history will be displayed here.</p>
        </div>`
    chatContainer.innerHTML = defaultText;
}

/**
 * lightmode
 */
function toggleLightMode() {
    document.body.classList.toggle("light-mode");
}


// create a div element for the chat and name the class as 'chat'
const createChatElement = (content, className) => {
    // Create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv; // Return the created chat div
}

const createHistoryElement = (content, className) => {
    // Create new div and apply chat, specified class and set html content of div
    const hisDiv = document.createElement("div");
    hisDiv.classList.add("his", className);
    hisDiv.innerHTML = content;
    return hisDiv; // Return the created chat div
}


// Call ChatGPT API to get the response
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
        if (outputData.choices && outputData.choices[0] && outputData.choices[0].message) {
            pElement.textContent = outputData.choices[0].message.content;
        } else {
            // Handle the case where the response data is incomplete or missing
            pElement.classList.add("error");
            pElement.textContent = "Incomplete response data received.";
        }

    } catch (e) {
        console.log(e);
        pElement.classList.add("error");
        pElement.textContent = "Sorry, I'm having trouble reaching the OpenAI API at the moment.";
    }
    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);

};

const showTypingAnimation = () => {
    // Display the typing animation and call the getChatResponse function
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="images/chatbot.jpg" alt="chatbot-img">
                    </div>
                </div>`;
    // Create an incoming chat div with typing animation and append it to chat container
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
}

/**
 * clear the whole page
 */
function clear() {
    // Remove the chats from local storage and call loadDataFromLocalstorage function
    if (confirm("Are you sure you want to delete all the chats?")) {
        localStorage.removeItem("names");
        displaySavedChats();
    }

}

function generateUniqueId() {
    return 'id_' + Date.now(); // Using current timestamp as part of the ID
}


function saveHandler() {
    if (confirm("Are you sure you want to save this chat?")) {
        var namesArr = JSON.parse(localStorage.getItem('names')) || [];
        var currentDate = new Date().toISOString();
        var uniqueId = generateUniqueId();
        var generatedName = (namesArr.length + 1).toString();

        var conversation = []; // Array to store conversation messages
        chatContainer.querySelectorAll(".chat").forEach(chat => {
            conversation.push(chat.outerHTML); // Save each chat message
        });
        
        console.log(uniqueId); 
        
        var nameData = {
            id: uniqueId,
            name: generatedName,
            date: currentDate,
            conversation: conversation, // Save the conversation array
        };
        console.log(nameData.id);
        
        document.getElementsByClassName("chatContent").value = nameData.conversation // Set chatContent
        document.getElementsByClassName("chat_id").value = nameData.id; // Set chat_id
        document.getElementsByClassName("chat_name").value = nameData.name;
        
        namesArr.push(nameData);
        // Save the updated array in local storage
        localStorage.setItem('names', JSON.stringify(namesArr));
        // Refresh the displayed history list
        displaySavedChats();
    }
        // namesArr.push(nameData); // Add the new chat to the array of saved chats
        // localStorage.setItem('names', JSON.stringify(namesArr)); // Save the updated array
        // displaySavedChats(); // Refresh the displayed history list
        // fetch('/interface/', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': csrfToken, // Replace with your CSRF token
        //     },
        //     body: JSON.stringify(nameData),
        // })
        // .then(response => response.json())
        // .then(data => {
        //     console.log(nameData); // Response from the server
        //     // Perform any further actions based on the response
        // })
        // .catch(error => {
        //     console.error('Error:', error);
        // });
    //}
}




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
    setTimeout(showTypingAnimation, 500);
}

function startNewChat() {
    // Clear the chatContainer and any existing content
    chatContainer.innerHTML = "";
    // You might want to include additional initialization logic here
    // For example, resetting variables, loading default messages, etc.
    // Scroll to the bottom after clearing the content
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    loadLocalStorage();
}

function displaySavedChats() {
    const historyList = document.querySelector(".history-list");
    historyList.innerHTML = ''; // Clear existing content

    const namesArr = JSON.parse(localStorage.getItem('names')) || [];

    namesArr.forEach(function (nameData, index) {
        const historyEntry = document.createElement('div');
        historyEntry.className = 'chat-history-entry';
        historyEntry.dataset.index = index;

        const nameParagraph = document.createElement('p');
        nameParagraph.classList.add('material-symbols-rounded');
        nameParagraph.innerHTML = `<strong>Name:</strong> ${nameData.name}`;
        historyEntry.appendChild(nameParagraph);

        historyEntry.addEventListener('click', function () {
            chatContainer.innerHTML = ''; // Clear the chat container
            nameData.conversation.forEach(message => {
                chatContainer.innerHTML += message; // Display each chat message
            });
            chatContainer.scrollTo(0, chatContainer.scrollHeight);
        });
        historyList.appendChild(historyEntry);
    });
}




/**
 * Sets up the page, adding event listeners and initial values.
 * Called after the page has loaded.
 */
function init() {
    // Add event listeners to buttons
    themeButton.addEventListener("click", toggleLightMode);
    sendButton.addEventListener("click", handleOutgoingChat);
    clearButton.addEventListener("click", clear);
    saveButton.addEventListener("click", saveHandler);
    newChatBox.addEventListener("click", startNewChat);

    displaySavedChats();
    loadLocalStorage();
}

addEventListener('DOMContentLoaded', init);