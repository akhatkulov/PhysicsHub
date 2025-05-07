const con = document.querySelector(".con");
const modals = document.querySelector(".modals");
const qModal = document.querySelector(".question_modal");
const tModal = document.querySelector(".test_modal");
const littleModal = document.querySelector(".little_modal");
const themeModal = document.querySelector(".theme_modal");

// Buttons
const btnQuestion = document.querySelector(".question");
const btnTest = document.querySelector(".test");
const btnLTest = document.querySelector(".t_plus");
const btnLEditTest = document.querySelector(".t_plus_edit")
const btnTheme = document.querySelector(".theme");

// Exit buttons
const exitQM = document.querySelector(".q_exit");
const exitTM = document.querySelector(".t_exit");
const exitLM = document.querySelector(".l_exit");
const exitMM = document.querySelector(".m_exit");

// Forms & inputs
const qForm = document.querySelector(".q_form");
const qFormEdit = document.querySelector(".q_form_edit");
const tForm = document.querySelector(".t_form");
const tFormEdit = document.querySelector(".t_form_edit");
const mForm = document.querySelector(".m_form");

const inputs = {
    q: {
        title: document.getElementById("title"),
        main: document.getElementById("shart"),
        helper: document.getElementById("izoh"),
        answer: document.getElementById("javob"),
        score: document.getElementById("ball_q"),
        theme: document.getElementById("mavzusi")
    },
    qEdit: {
        title: document.getElementById("title_edit"),
        main: document.getElementById("shart_edit"),
        helper: document.getElementById("izoh_edit"),
        answer: document.getElementById("javob_edit"),
        score: document.getElementById("ball_q_edit"),
        theme: document.getElementById("mavzusi_edit")
    },
    t: {
        title: document.getElementById("t_title"),
        theme: document.getElementById("t_mavzusi")
    },
    tEdit: {
        title: document.getElementById("t_title_edit"),
        theme: document.getElementById("t_mavzusi_edit")
    },
    m: {
        title: document.getElementById("m_title"),
        about: document.getElementById("m_about")
    }
};

// Containers
const questionContainer = document.querySelector(".q_boxs");
const quizContainer = document.querySelector(".t_boxs");
const themesContainer = document.querySelector(".th_box");

// Test question elements
const svQ = document.querySelector(".sv_q");
const variants = [
    document.getElementById("variant1"),
    document.getElementById("variant2"),
    document.getElementById("variant3"),
    document.getElementById("variant4")
];
const radios = document.querySelectorAll(".radio");
const qNumber = document.querySelector(".q_number");
const qEditNumber = document.querySelector(".q_number_edit");
const testsWrapper = document.querySelector(".tests--wrapper");
const testsEditWrapper = document.querySelector(".tests_edit--wrapper");

let testData = [];
let currentId = 0;
let questionCount = 0;

// Utility: open modal
function openModal(modal) {
    modals.style.display = "flex";
    modal.style.display = "grid";
    con.style.height = "100vh";
    con.style.overflow = "hidden";
}

// Utility: close all modals
function closeModals() {
    [qModal, tModal, littleModal, themeModal].forEach(m => m && (m.style.display = "none"));
    modals.style.display = "none";
    con.style.height = "auto";
    con.style.overflow = "auto";
}

// Show modals
btnQuestion.addEventListener("click", () => {
    openModal(qModal);
    qForm.style.display = "grid";
    qFormEdit.style.display = "none";
});
btnTest.addEventListener("click", () => {
    openModal(tModal);
    littleModal.style.display = "none";
    tForm.style.display = "grid";
    tFormEdit.style.display = "none";
    testData = [];
    currentId = 0;
    questionCount = 0;
    testsWrapper.innerHTML = "";
    testsEditWrapper.innerHTML = "";
    qNumber.textContent = "0";
});
btnTheme.addEventListener("click", () => openModal(themeModal));
btnLTest.addEventListener("click", () => openModal(littleModal));
btnLEditTest.addEventListener("click", () => openModal(littleModal));
// Exit listeners
exitQM.addEventListener("click", closeModals);
exitTM.addEventListener("click", closeModals);
exitLM.addEventListener("click", () => { littleModal.style.display = "none" });
exitMM.addEventListener("click", closeModals);

// Add a test question
svQ.addEventListener("submit", e => {
    e.preventDefault();
    const questionText = document.getElementById("l_savol").value.trim();
    const score = document.getElementById("l_ball").value;
    const opts = variants.map(v => v.value.trim());
    const answerIndex = Array.from(radios).findIndex(r => r.checked);
    if (!questionText || answerIndex < 0) return;
    const obj = { id: currentId++, question: questionText, score, options: opts, answer: opts[answerIndex] };
    testData.push(obj);
    questionCount++;
    qNumber.textContent = questionCount;
    const box = document.createElement('div');
    box.className = 'box test_savol';
    box.dataset.id = obj.id;
    box.innerHTML = `<p class="box_title">${obj.question}</p><div class="edit_box_crud">
        <span class="delete-btn"><i class="fa-solid fa-trash"></i></span>
        </div>`;
    testsWrapper.appendChild(box);
    testsEditWrapper.appendChild(box.cloneNode(true));
    box.querySelector('.delete-btn').addEventListener('click', () => {
        testsWrapper.removeChild(box);
        testsEditWrapper.removeChild(box);
        testData = testData.filter(q => q.id !== obj.id);
        questionCount--;
        qNumber.textContent = questionCount;
    });
    document.getElementById("l_savol").value = "";
    document.getElementById("l_ball").value = "";
    variants.forEach(v => v.value = "");
    radios.forEach(r => r.checked = false);
    littleModal.style.display = "none"
});

// Submit full quiz
tForm.addEventListener("submit", e => {
    if (!testData.length) return;
    e.preventDefault();
    fetch("/admin/add_quiz", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: inputs.t.title.value, theme: inputs.t.theme.value, data: testData })
    }).then(() => location.reload());
});

// Submit question
qForm.addEventListener("submit", e => {
    e.preventDefault();
    fetch("/admin/add_matter", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: inputs.q.title.value, main: inputs.q.main.value, helper: inputs.q.helper.value, correct: inputs.q.answer.value, ball: inputs.q.score.value, theme: inputs.q.theme.value })
    }).then(() => location.reload());
});

// Submit theme
mForm.addEventListener("submit", e => {
    e.preventDefault();
    fetch("/admin/add_theme", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: inputs.m.title.value, about: inputs.m.about.value })
    }).then(() => location.reload());
});

// Load themes into selects
function loadThemes() {
    fetch("/api/themes").then(res => res.json()).then(data => {
        data.forEach(item => {
            const opt = `<option value="${item.name}">${item.name}</option>`;
            inputs.q.theme.insertAdjacentHTML('beforeend', opt);
            inputs.qEdit.theme.insertAdjacentHTML('beforeend', opt);
            inputs.t.theme.insertAdjacentHTML('beforeend', opt);
            inputs.tEdit.theme.insertAdjacentHTML('beforeend', opt);
        });
    });
}

// Load question list
function loadQuestions() {
    fetch("/api/get_matter").then(res => res.json()).then(data => {
        questionContainer.innerHTML = data.length ? data.map(item => `
      <div class="box">
        <p class="box_title">#${item.id} | ${item.title}</p>
        <div class="edit_box_crud">
          <span class="edit_box_eq" onclick="editQuestion(${item.id})"><i class="fa-solid fa-pencil"></i></span>
          <span class="edit_box_aq" onclick="hiddenQuestion(${item.id})"><i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i></span>
          <span class="edit_box_dq" onclick="deleteQuestion(${item.id})"><i class="fa-solid fa-trash"></i></span>
        </div>
      </div>
    `).join('') : `<span class="edit_empty"><i class="fa-solid fa-box-open"></i><p>Ma'lumot topilmadi</p></span>`;
    });
}

// Load quiz list
function loadQuizzes() {
    fetch("/api/get_quiz").then(res => res.json()).then(data => {
        quizContainer.innerHTML = data.length ? data.map(item => `
      <div class="box">
        <p class="box_title">#${item.id} | ${item.title}</p>
        <div class="edit_box_crud">
          <span class="edit_box_et" onclick="editQuiz(${item.id})"><i class="fa-solid fa-pencil"></i></span>
          <span class="edit_box_at" onclick="hiddenQuiz(${item.id})"><i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i></span>
          <span class="edit_box_dt" onclick="deleteQuiz(${item.id})"><i class="fa-solid fa-trash"></i></span>
        </div>
      </div>
    `).join('') : `<span class="edit_empty"><i class="fa-solid fa-box-open"></i><p>Ma'lumot topilmadi</p></span>`;
    });
}

// Load theme list display
function loadThemeList() {
    fetch("/api/themes").then(res => res.json()).then(data => {
        themesContainer.innerHTML = data.length ? data.map(item => `
      <div class="box">
        <p class="box_title">#${item.id} | ${item.name}</p>
        <div class="edit_box_crud">
          <span onclick="deleteTheme(${item.id})"><i class="fa-solid fa-trash"></i></span>
        </div>
      </div>
    `).join('') : `<span class="edit_empty"><i class="fa-solid fa-box-open"></i><p>Ma'lumot topilmadi</p></span>`;
    });
}

// Delete handlers
window.deleteQuestion = id => { if (confirm("Masala o'chirilsinmi ?")) fetch(`/api/delete_matter/${id}`, { method: 'DELETE' }).then(loadQuestions); };
window.deleteQuiz = id => { if (confirm("Test o'chirilsinmi ?")) fetch(`/api/delete_quiz/${id}`, { method: 'DELETE' }).then(loadQuizzes); };
window.deleteTheme = id => { if (confirm("Mavzu o'chirilsinmi ?")) fetch(`/api/delete_theme/${id}`, { method: 'DELETE' }).then(loadThemeList); };
window.editQuestion = function (id) {
    // Open edit modal
    openModal(qModal);
    qForm.style.display = "none";
    qFormEdit.style.display = "grid";
    // Fetch single question data
    fetch(`/api/get_matter`) // or endpoint `/api/get_matter/${id}` if available
        .then(res => res.json())
        .then(data => {
            const item = data.find(q => q.id === id);
            if (!item) return;
            // Populate edit inputs
            inputs.qEdit.title.value = item.title;
            inputs.qEdit.main.value = item.main || item.shart;
            inputs.qEdit.helper.value = item.helper || item.izoh;
            inputs.qEdit.answer.value = item.correct;
            inputs.qEdit.score.value = item.ball;
            inputs.qEdit.theme.value = item.theme;
        });
    // Handle edit form submission
    qFormEdit.onsubmit = function (e) {
        e.preventDefault();
        const payload = {
            id: id,
            title: inputs.qEdit.title.value,
            main: inputs.qEdit.main.value,
            helper: inputs.qEdit.helper.value,
            correct: inputs.qEdit.answer.value,
            ball: inputs.qEdit.score.value,
            theme: inputs.qEdit.theme.value,
            status: true
        };
        fetch("/api/edit_matter", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(res => res.json())
            .then(() => {
                closeModals();
                loadQuestions();
            })
            .catch(err => console.error(err));
    };
};
window.editQuiz = function (id) {
    testsEditWrapper.innerHTML = '';
    openModal(tModal);
    tForm.style.display = 'none';
    tFormEdit.style.display = 'grid';
    littleModal.style.display = 'none';
    testData = [];
    currentId = 0;
    questionCount = 0;
    testsWrapper.innerHTML = '';
    qNumber.textContent = '0';
    fetch('/api/get_quiz')
        .then(res => res.json())
        .then(data => {
            const item = data.find(q => q.id === id);
            if (!item) return;
            inputs.tEdit.title.value = item.title;
            inputs.tEdit.theme.value = item.theme;
            // Safely parse questions array
            let questions;
            try {
                questions = Array.isArray(item.data) ? item.data : JSON.parse(item.data);
            } catch (e) {
                console.error('Failed to parse quiz data', e);
                return;
            }
            questions.forEach(q => {
                testData.push(q);
                const box = document.createElement('div');
                box.className = 'box test_savol';
                box.dataset.id = q.id;
                box.innerHTML = `<p class="box_title">${q.question}</p><div class="edit_box_crud">
                <span class="delete-btn"><i class="fa-solid fa-trash"></i></span>
                </div>`;
                testsEditWrapper.appendChild(box);
                box.querySelector('.delete-btn').addEventListener('click', () => {
                    testsEditWrapper.removeChild(box);
                    testData = testData.filter(item => item.id !== q.id);
                    questionCount--;
                    qEditNumber.textContent = questionCount;
                });
                questionCount++;
            });
            qEditNumber.textContent = questionCount;
        });
    tFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_quiz", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, title: inputs.tEdit.title.value, theme: inputs.tEdit.theme.value, data: testData, status: true })
        })
            .then(res => res.json())
            .then(() => {
                closeModals();
                loadQuizzes();
            })
            .catch(err => console.error(err));
    };
};
window.hiddenQuestion = function (id) {
    fetch('/api/toggle_matter_status', {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    })
        .then(res => res.json())
        .then(() => {
            loadQuestions();
            closeModals();
        })
        .catch(err => console.error(err));
}
window.hiddenQuiz = function (id) {
    fetch('/api/toggle_quiz_status', {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    })
        .then(res => res.json())
        .then(({ new_status }) => {
            // kerak bo'lsa statusni ekranga chiqarish yoki styling o'zgartirish:
            console.log('Yangi status:', new_status);
            loadQuizzes();    // ma'lumotlarni qayta yuklash
            closeModals();    // modal oynani yopish
        })
        .catch(err => console.error(err));
}

// Initialize
loadThemes();
loadQuestions();
loadQuizzes();
loadThemeList();

