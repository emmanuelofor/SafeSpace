const addBox = document.querySelector(".add-box"),
popupBox = document.querySelector(".popup-box"),
popupTitle = popupBox.querySelector("header p"),
closeIcon = popupBox.querySelector("header i"),
titleTag = popupBox.querySelector("input"),
descTag = popupBox.querySelector("textarea"),
addBtn = popupBox.querySelector("button");

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const journals = JSON.parse(localStorage.getItem("journals") || "[]");
let isUpdate = false, updateId;

addBox.addEventListener("click", () => {
    popupTitle.innerText = "Add a new journal";
    addBtn.innerText = "Add journal";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    if(window.innerWidth > 660) titleTag.focus();
});

closeIcon.addEventListener("click", () => {
    isUpdate = false;
    titleTag.value = descTag.value = "";
    popupBox.classList.remove("show");
    document.querySelector("body").style.overflow = "auto";
});

function showjournals() {
    if(!journals) return;
    document.querySelectorAll(".journal").forEach(li => li.remove());
    journals.forEach((journal, id) => {
        let filterDesc = journal.description.replaceAll("\n", '<br/>');
        let liTag = `<li class="journal">
                        <div class="details">
                            <p>${journal.title}</p>
                            <span>${filterDesc}</span>
                        </div>
                        <div class="bottom-content">
                            <span>${journal.date}</span>
                            <div class="settings">
                                <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                <ul class="menu">
                                    <li onclick="updatejournal(${id}, '${journal.title}', '${filterDesc}')"><i class="uil uil-pen"></i>Edit</li>
                                    <li onclick="deletejournal(${id})"><i class="uil uil-trash"></i>Delete</li>
                                </ul>
                            </div>
                        </div>
                    </li>`;
        addBox.insertAdjacentHTML("afterend", liTag);
    });
}
showjournals();

function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if(e.target.tagName != "I" || e.target != elem) {
            elem.parentElement.classList.remove("show");
        }
    });
}

function deletejournal(journalId) {
    let confirmDel = confirm("Are you sure you want to delete this journal?");
    if(!confirmDel) return;
    journals.splice(journalId, 1);
    localStorage.setItem("journals", JSON.stringify(journals));
    showjournals();
}

function updatejournal(journalId, title, filterDesc) {
    let description = filterDesc.replaceAll('<br/>', '\r\n');
    updateId = journalId;
    isUpdate = true;
    addBox.click();
    titleTag.value = title;
    descTag.value = description;
    popupTitle.innerText = "Update a journal";
    addBtn.innerText = "Update journal";
}

addBtn.addEventListener("click", e => {
    e.preventDefault();
    let title = titleTag.value.trim(),
    description = descTag.value.trim();

    if(title || description) {
        let currentDate = new Date(),
        month = months[currentDate.getMonth()],
        day = currentDate.getDate(),
        year = currentDate.getFullYear();

        let journalInfo = {title, description, date: `${month} ${day}, ${year}`}
        if(!isUpdate) {
            journals.push(journalInfo);
        } else {
            isUpdate = false;
            journals[updateId] = journalInfo;
        }
        localStorage.setItem("journals", JSON.stringify(journals));
        showjournals();
        closeIcon.click();
    }
});