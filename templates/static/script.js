// const BACKEND = "https://cocktail-recommender-i2nk.onrender.com";
const BACKEND = "http://127.0.0.1:5000";

document.getElementById("search").addEventListener("click", async () => {
    const fileInput = document.getElementById("image-input");
    let res;

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        res = await fetch(`${BACKEND}/recommend`, {
            method: "POST",
            body: formData
        });
    } else {
        const query = document.getElementById("query").value;
        res = await fetch(`${BACKEND}/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
    }

    if (!res.ok) {
        console.error("Request failed:", res.statusText);
        return;
    }

    const { results, recommendation } = await res.json();
    document.getElementById("summary").textContent = recommendation;

    const container = document.getElementById("results");
    container.innerHTML = "";

    results.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="card-img" />
            <h2>${item.name}</h2>
            <div class="similarity">${item.similarity.toFixed(1)}% match</div>
            <p>${item.description}</p>
        `;
        container.appendChild(card);
    });
});
