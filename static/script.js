document.getElementById("search").addEventListener("click", async () => {
    const fileInput = document.getElementById("image-input");
    let res;

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        res = await fetch("/recommend", {
            method: "POST",
            body: formData
        });
    } else {
        const query = document.getElementById("query").value;
        res = await fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
    }

    const data = await res.json();
    const container = document.getElementById("results");
    container.innerHTML = "";

    data.forEach(item => {
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
