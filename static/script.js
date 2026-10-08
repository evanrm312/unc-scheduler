const button = document.querySelector("#test-button");
const output = document.querySelector("#output");

button.addEventListener("click", async() => {
    const response = await fetch("/api/schedules");
    const data = await response.json();

    console.log(schedules);
})