document.getElementById("search").addEventListener("click", async () => {
  const query = document.getElementById("query").value;
  const res = await fetch("/recommend", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({query})
  });
  const data = await res.json();
  const ul = document.getElementById("results");
  ul.innerHTML = "";
  data.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${item.name}</strong> - ${item.similarity.toFixed(1)}%<br>${item.description}`;
    ul.appendChild(li);
  });
});
