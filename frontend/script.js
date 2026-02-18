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
            responseText.innerText =
                "RESULT:\n" +
                JSON.stringify(data.data, null, 2) +
                "\n\nEXPLANATION:\n" +
                data.explanation;
        }else {
            responseText.innerText =
            "ERROR TYPE: " + data.error_type +
            "\nMESSAGE: " + data.message +
            "\n\nEXPLANATION:\n" +
            data.explanation;

}

    } catch (error) {
        responseText.innerText = "Error connecting to backend";
    }
});
