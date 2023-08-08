const API_KEY = "PASTE-YOUR-API-KEY-HERE"; // Paste your API key here

const themeButton = document.getElementById("theme-btn");
const chatInput = document.getElementById("chat-input");
const chatContainer = document.querySelector(".chat-container");


/**
 * LOAD LOCAL STORAGE
 */
function loadLocalStorage() {
    const defaultText = 
        `<div class="default-text">
            <h1>ChatGPT ......</h1>
                <p>Start a conversation and explore the power of AI.<br> Your chat history will be displayed here.</p>
        </div>`
    chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}

/**
 * lightmode
 */
function toggleLightMode() {
    document.body.classList.toggle("light-mode");
}


/**
 * send chat and display in container
 */
//function sendChat{

//}
/**
 * Sets up the page, adding event listeners and initial values.
 * Called after the page has loaded.
 */
function init() {
    // Add event listeners to buttons
    themeButton.addEventListener("click", toggleLightMode);
    //sendButton = addEventListener("click", sendChat);
    loadLocalStorage();
}


addEventListener('DOMContentLoaded', init);
