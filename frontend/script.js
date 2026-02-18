const runButton = document.getElementById("runQueryBtn");
const responseText = document.getElementById("responseText");

runButton.addEventListener("click", async () => {
    const query = document.getElementById("sqlInput").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        if (data.status === "success") {
            responseText.innerText = JSON.stringify(data.data, null, 2);
        } else {
            responseText.innerText = `Error Type: ${data.error_type}\nMessage: ${data.message}`;
}

    } catch (error) {
        responseText.innerText = "Error connecting to backend";
    }
});
