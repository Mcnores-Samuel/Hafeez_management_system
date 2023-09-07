const start_options = document.querySelector("#start-list")
const end_options = document.querySelector("#end")
const rangeStart = document.querySelector("#rangeStart")
const rangeEnd = document.querySelector("#rangeEnd")

for (let i = 1; i < 1001; i++)
{
    const start = document.createElement("option")
    const end = document.createElement("option")
    start.textContent = `${i}`
    end.textContent = `${i}`
    rangeStart.appendChild(start)
    rangeEnd.appendChild(end)
}

for (let i = 65; i < 91; i++)
{
    const options1 = document.createElement("option")
    const options2 = document.createElement("option")
    options1.textContent = `${String.fromCharCode(i)}`;
    options2.textContent = `${String.fromCharCode(i)}`;
    start_options.appendChild(options1);
    end_options.appendChild(options2);
}