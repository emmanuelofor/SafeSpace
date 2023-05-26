const addJournalBtn = document.getElementById('addJournalBtn');
const popupBox = document.getElementById('popupBox');
const closeBtn = popupBox.querySelector('.close-btn');
const addBox = document.querySelector('.add-box');
const popupTitle = popupBox.querySelector('header p');
const closeIcon = popupBox.querySelector('header i');
const titleTag = popupBox.querySelector('input');
const descTag = popupBox.querySelector('textarea');
const addBtn = popupBox.querySelector('button');
const journals = JSON.parse(localStorage.getItem('journals') || '[]');
let isUpdate = false;
let updateId;

addJournalBtn.addEventListener('click', () => {
  popupTitle.innerText = 'Add a new journal';
  addBtn.innerText = 'Add journal';
  popupBox.classList.add('show');
  document.querySelector('body').style.overflow = 'hidden';
  if (window.innerWidth > 660) {
    titleTag.focus();
  }
});

closeBtn.addEventListener('click', () => {
  isUpdate = false;
  titleTag.value = '';
  descTag.value = '';
  popupBox.classList.remove('show');
  document.querySelector('body').style.overflow = 'auto';
});

function showJournals() {
  const journalList = document.querySelector('.journal-list');
  journalList.innerHTML = '';
  journals.forEach((journal, id) => {
    const filterDesc = journal.description.replaceAll('\n', '<br/>');
    const liTag = `<li class="journal">
                        <div class="details">
                            <p>${journal.title}</p>
                            <span>${filterDesc}</span>
                        </div>
                        <div class="bottom-content">
                            <span>${journal.date}</span>
                            <div class="settings">
                                <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                <ul class="menu">
                                    <li onclick="updateJournal(${id}, '${journal.title}', '${filterDesc}')"><i class="uil uil-pen"></i>Edit</li>
                                    <li onclick="deleteJournal(${id})"><i class="uil uil-trash"></i>Delete</li>
                                </ul>
                            </div>
                        </div>
                    </li>`;
    journalList.insertAdjacentHTML('beforeend', liTag);
  });
}

showJournals();

function showMenu(elem) {
  elem.parentElement.classList.toggle('show');
  document.addEventListener('click', (e) => {
    if (e.target.tagName !== 'I' || e.target !== elem) {
      elem.parentElement.classList.remove('show');
    }
  });
}

function deleteJournal(journalId) {
  const confirmDel = confirm('Are you sure you want to delete this journal?');
  if (!confirmDel) return;
  journals.splice(journalId, 1);
  localStorage.setItem('journals', JSON.stringify(journals));
  showJournals();
}

function updateJournal(journalId, title, filterDesc) {
  const description = filterDesc.replaceAll('<br/>', '\r\n');
  updateId = journalId;
  isUpdate = true;
  addJournalBtn.click();
  titleTag.value = title;
  descTag.value = description;
  popupTitle.innerText = 'Update a journal';
  addBtn.innerText = 'Update journal';
}

addBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const title = titleTag.value.trim();
  const description = descTag.value.trim();

  if (title || description) {
    const currentDate = new Date();
    const month = months[currentDate.getMonth()];
    const day = currentDate.getDate();
    const year = currentDate.getFullYear();

    const journalInfo = { title, description, date: `${month} ${day}, ${year}` };
    if (!isUpdate) {
      journals.push(journalInfo);
    } else {
      isUpdate = false;
      journals[updateId] = journalInfo;
    }
    localStorage.setItem('journals', JSON.stringify(journals));
    showJournals();
    closeBtn.click();
  }
});
