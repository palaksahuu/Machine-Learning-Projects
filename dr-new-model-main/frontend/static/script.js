function predictNPI() {
    let timeInput = document.getElementById("timeInput").value;
    if (!timeInput) {
        alert("Please enter a valid time!");
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ time: timeInput })
    })
    .then(response => response.blob())
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "predicted_doctors.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        document.getElementById("message").innerText = "Download complete!";
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("message").innerText = "Error fetching predictions!";
    });
}
