const button = document.getElementById("checkBackendBtn");
const responseText = document.getElementById("responseText");

button.addEventListener("click", async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/");
        const data = await response.json();
        responseText.innerText = data.message;
    } catch (error) {
        responseText.innerText = "Error connecting to backend";
    }
});
