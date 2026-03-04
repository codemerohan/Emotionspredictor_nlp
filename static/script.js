// helper to post the text and update the UI
async function predict() {
    console.log("predict() called");

    let text = document.getElementById("text").value;
    if (!text) {
        document.getElementById("result").innerText = "Please enter some text.";
        return;
    }

    // use current origin so the script works whether the page is loaded
    // from the server or from disk (in which case window.location.origin
    // will be "null" and we fall back to the known host).
    const origin = window.location.origin === "null" ?
        "http://127.0.0.1:5000" : window.location.origin;
    const url = `${origin}/predict`;
    console.log("posting to", url);

    try {
        let res = await fetch(url, {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({text:text})
        });

        if (!res.ok) {
            throw new Error(`Server returned ${res.status}`);
        }

        let data = await res.json();
        document.getElementById("result").innerText =
            "Emotion: " + data.emotion;
    } catch (err) {
        console.error(err);
        document.getElementById("result").innerText =
            "Error: " + err.message;
    }
}
