const placeholders = document.querySelector(".placeholders")

for (let n = 0; n < 3; n++)
{
    const section = document.createElement("section");
    const header = document.createElement("h1")
    header.textContent = "This section is still under development"
    section.appendChild(header)
    placeholders.appendChild(section)
}