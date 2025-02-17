async function getRecommendations() {
    let movie = document.getElementById("movieInput").value;
    let response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ movie: movie })
    });

    let data = await response.json();
    document.getElementById("recommendations").innerText = data.recommendations.join(", ");
}
