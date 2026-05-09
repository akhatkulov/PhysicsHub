const CSRF_TOKEN = (document.querySelector('meta[name="csrf-token"]') || {}).content || '';

const _origFetch = window.fetch.bind(window);
window.fetch = (input, init) => {
    init = init || {};
    const method = (init.method || (typeof input === 'object' && input.method) || 'GET').toUpperCase();
    if (CSRF_TOKEN && !['GET', 'HEAD', 'OPTIONS'].includes(method)) {
        init.headers = Object.assign({}, init.headers || {}, { 'X-CSRFToken': CSRF_TOKEN });
        if (init.credentials === undefined) init.credentials = 'same-origin';
    }
    return _origFetch(input, init);
};

function escapeHtml(s) {
    return String(s ?? '').replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
}

function safeRender(el, html) {
    if (!el) return;
    const clean = (typeof DOMPurify !== 'undefined')
        ? DOMPurify.sanitize(html, { ADD_ATTR: ['onclick'] })
        : '';
    el.innerHTML = clean;
}

const con = document.querySelector(".con");
const modals = document.querySelector(".modals");
const qModal = document.querySelector(".question_modal");
const tModal = document.querySelector(".test_modal");
const littleModal = document.querySelector(".little_modal");
const animationModal = document.querySelector(".anima_modal");
const themeModal = document.querySelector(".theme_modal");
const labModal = document.querySelector(".lab_modal");
const hModal = document.querySelector(".handbook_modal");
const lessonModal = document.querySelector(".lesson_modal");
const userModal = document.querySelector(".user_modal");

const q_page = document.querySelector(".question_page");
const t_page = document.querySelector(".test_page");
const a_page = document.querySelector(".animation_page");
const l_page = document.querySelector(".lab_page");
const m_page = document.querySelector(".theme_page");
const hb_page = document.querySelector(".handbook_page");
const ls_page = document.querySelector(".lesson_page");
const u_page = document.querySelector(".user_page");

// Add buttons
const btnQuestion = document.querySelector(".question");
const btnTest = document.querySelector(".test");
const btnAnimation = document.querySelector(".animation");
const btnLabaratory = document.querySelector(".labaratory");
const btnLTest = document.querySelector(".t_plus");
const btnLEditTest = document.querySelector(".t_plus_edit");
const btnTheme = document.querySelector(".theme");
const btnHandbook = document.querySelector(".handbook-add");
const btnLesson = document.querySelector(".lesson-add");

// Exit buttons
const exitQM = document.querySelector(".q_exit");
const exitTM = document.querySelector(".t_exit");
const exitAM = document.querySelector(".a_exit");
const exitLabM = document.querySelector(".l_exit");
const exitLM = document.querySelector(".lm_exit");
const exitMM = document.querySelector(".m_exit");
const exitHM = document.querySelector(".h_exit");
const exitLS = document.querySelector(".ls_exit");
const exitUM = document.querySelector(".u_exit");

// Forms (add)
const qForm = document.querySelector(".q_form");
const tForm = document.querySelector(".t_form");
const aForm = document.querySelector(".a_form");
const lForm = document.querySelector(".l_form");
const mForm = document.querySelector(".m_form");
const hForm = document.querySelector(".h_form");
const lsForm = document.querySelector(".ls_form");

// Forms (edit)
const qFormEdit = document.querySelector(".q_form_edit");
const tFormEdit = document.querySelector(".t_form_edit");
const aFormEdit = document.querySelector(".a_form_edit");
const lFormEdit = document.querySelector(".l_form_edit");
const mFormEdit = document.querySelector(".m_form_edit");
const hFormEdit = document.querySelector(".h_form_edit");
const lsFormEdit = document.querySelector(".ls_form_edit");
const uFormEdit = document.querySelector(".u_form_edit");

// Search inputs
const qSearch = document.getElementById("q_search_input");
const tSearch = document.getElementById("t_search_input");
const aSearch = document.getElementById("a_search_input");
const lSearch = document.getElementById("l_search_input");
const mSearch = document.getElementById("m_search_input");
const hSearch = document.getElementById("h_search_input");
const lsSearch = document.getElementById("ls_search_input");
const uSearch = document.getElementById("u_search_input");

const inputs = {
    q: {
        title: document.getElementById("title"),
        main: document.getElementById("shart"),
        helper: document.getElementById("izoh"),
        answer: document.getElementById("javob"),
        ball: document.getElementById("ball_q"),
        theme: document.getElementById("mavzusi"),
    },
    qEdit: {
        title: document.getElementById("title_edit"),
        main: document.getElementById("shart_edit"),
        helper: document.getElementById("izoh_edit"),
        answer: document.getElementById("javob_edit"),
        ball: document.getElementById("ball_q_edit"),
        theme: document.getElementById("mavzusi_edit"),
    },
    t: {
        title: document.getElementById("t_title"),
        theme: document.getElementById("t_mavzusi"),
    },
    tEdit: {
        title: document.getElementById("t_title_edit"),
        theme: document.getElementById("t_mavzusi_edit"),
    },
    a: {
        title: document.getElementById("a_title"),
        theme: document.getElementById("a_mavzusi"),
        gif: document.getElementById("a_gif"),
        about: document.getElementById("a_about"),
    },
    aEdit: {
        title: document.getElementById("a_title_edit"),
        theme: document.getElementById("a_mavzusi_edit"),
        gif: document.getElementById("a_gif_edit"),
        about: document.getElementById("a_about_edit"),
    },
    l: {
        title: document.getElementById("l_title"),
        image: document.getElementById("l_image"),
        zip: document.getElementById("l_zip"),
        url: document.getElementById("l_url"),
        about: document.getElementById("l_about"),
    },
    lEdit: {
        title: document.getElementById("l_title_edit"),
        image: document.getElementById("l_image_edit"),
        zip: document.getElementById("l_zip_edit"),
        url: document.getElementById("l_url_edit"),
        about: document.getElementById("l_about_edit"),
    },
    m: {
        title: document.getElementById("m_title"),
        about: document.getElementById("m_about"),
    },
    mEdit: {
        title: document.getElementById("m_title_edit"),
        about: document.getElementById("m_about_edit"),
    },
    h: {
        category: document.getElementById("h_category"),
        title: document.getElementById("h_title"),
        content: document.getElementById("h_content"),
        about: document.getElementById("h_about"),
    },
    hEdit: {
        category: document.getElementById("h_category_edit"),
        title: document.getElementById("h_title_edit"),
        content: document.getElementById("h_content_edit"),
        about: document.getElementById("h_about_edit"),
    },
    ls: {
        title: document.getElementById("ls_title"),
        about: document.getElementById("ls_about"),
        file: document.getElementById("ls_file"),
    },
    lsEdit: {
        title: document.getElementById("ls_title_edit"),
        about: document.getElementById("ls_about_edit"),
        file: document.getElementById("ls_file_edit"),
    },
    uEdit: {
        username: document.getElementById("u_username_edit"),
        name: document.getElementById("u_name_edit"),
        surname: document.getElementById("u_surname_edit"),
        university: document.getElementById("u_university_edit"),
    },
};

const modalTitles = {
    a: document.querySelector(".a_modal_title"),
    l: document.querySelector(".l_modal_title"),
    m: document.querySelector(".m_modal_title"),
    h: document.querySelector(".h_modal_title"),
    ls: document.querySelector(".ls_modal_title"),
};

// Containers
const questionContainer = document.querySelector(".q_boxs");
const quizContainer = document.querySelector(".t_boxs");
const themesContainer = document.querySelector(".th_box");
const animationContainer = document.querySelector(".a_boxs");
const labContainer = document.querySelector(".l_boxs");
const handbookContainer = document.querySelector(".hb_box");
const lessonContainer = document.querySelector(".ls_box");
const userContainer = document.querySelector(".u_box");

const questionBox = document.querySelector(".question_box");
const testBox = document.querySelector(".test_box");
const animationBox = document.querySelector(".animation_box");
const labaratoryBox = document.querySelector(".lab_box");
const themeBox = document.querySelector(".theme_box");
const handbookBox = document.querySelector(".handbook_box");
const lessonBox = document.querySelector(".lesson_box");
const userBox = document.querySelector(".user_box");

const allBoxes = [questionBox, testBox, animationBox, labaratoryBox, themeBox, handbookBox, lessonBox, userBox];

function showOnly(boxToShow) {
    allBoxes.forEach(b => { if (b) b.style.display = (b === boxToShow ? "block" : "none"); });
}

q_page && q_page.addEventListener("click", () => showOnly(questionBox));
t_page && t_page.addEventListener("click", () => showOnly(testBox));
a_page && a_page.addEventListener("click", () => showOnly(animationBox));
l_page && l_page.addEventListener("click", () => showOnly(labaratoryBox));
m_page && m_page.addEventListener("click", () => showOnly(themeBox));
hb_page && hb_page.addEventListener("click", () => showOnly(handbookBox));
ls_page && ls_page.addEventListener("click", () => { showOnly(lessonBox); loadLessons(); });
u_page && u_page.addEventListener("click", () => { showOnly(userBox); loadUsers(); });

// Test question modal state
const svQ = document.querySelector(".sv_q");
const variants = [
    document.getElementById("variant1"),
    document.getElementById("variant2"),
    document.getElementById("variant3"),
    document.getElementById("variant4"),
];
const radios = document.querySelectorAll(".radio");
const qNumber = document.querySelector(".q_number");
const qEditNumber = document.querySelector(".q_number_edit");
const testsWrapper = document.querySelector(".tests--wrapper");
const testsEditWrapper = document.querySelector(".tests_edit--wrapper");

let testData = [];
let currentId = 0;
let questionCount = 0;

function openModal(modal) {
    modals.style.display = "flex";
    modal.style.display = "grid";
    con.style.height = "100vh";
    con.style.overflow = "hidden";
}

function closeModals() {
    [qModal, tModal, littleModal, animationModal, labModal, themeModal, hModal, lessonModal, userModal]
        .forEach(m => m && (m.style.display = "none"));
    modals.style.display = "none";
    con.style.height = "auto";
    con.style.overflow = "auto";
}

function showAddForm(addForm, editForm, titleEl, addTitle) {
    if (addForm) addForm.style.display = "grid";
    if (editForm) editForm.style.display = "none";
    if (titleEl && addTitle) titleEl.textContent = addTitle;
}

function showEditForm(addForm, editForm, titleEl, editTitle) {
    if (addForm) addForm.style.display = "none";
    if (editForm) editForm.style.display = "grid";
    if (titleEl && editTitle) titleEl.textContent = editTitle;
}

// ----- Add modal openers -----
btnQuestion && btnQuestion.addEventListener("click", () => {
    openModal(qModal);
    qForm.style.display = "grid";
    qFormEdit.style.display = "none";
});
btnTest && btnTest.addEventListener("click", () => {
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
btnAnimation && btnAnimation.addEventListener("click", () => {
    openModal(animationModal);
    showAddForm(aForm, aFormEdit, modalTitles.a, "Animatsiya qo'shish");
    aForm.reset();
});
btnTheme && btnTheme.addEventListener("click", () => {
    openModal(themeModal);
    showAddForm(mForm, mFormEdit, modalTitles.m, "Bo'lim qo'shish");
    mForm.reset();
});
btnLTest && btnLTest.addEventListener("click", () => openModal(littleModal));
btnLEditTest && btnLEditTest.addEventListener("click", () => openModal(littleModal));
btnLabaratory && btnLabaratory.addEventListener("click", () => {
    openModal(labModal);
    showAddForm(lForm, lFormEdit, modalTitles.l, "Labaratoriya qo'shish");
    lForm.reset();
});
btnHandbook && btnHandbook.addEventListener("click", () => {
    openModal(hModal);
    showAddForm(hForm, hFormEdit, modalTitles.h, "Qo'llanma qo'shish");
    hForm.reset();
});
btnLesson && btnLesson.addEventListener("click", () => {
    openModal(lessonModal);
    showAddForm(lsForm, lsFormEdit, modalTitles.ls, "Mavzu qo'shish");
    lsForm.reset();
});

// Exit listeners
exitQM && exitQM.addEventListener("click", closeModals);
exitTM && exitTM.addEventListener("click", closeModals);
exitAM && exitAM.addEventListener("click", closeModals);
exitLabM && exitLabM.addEventListener("click", closeModals);
exitLM && exitLM.addEventListener("click", () => { littleModal.style.display = "none"; });
exitMM && exitMM.addEventListener("click", closeModals);
exitHM && exitHM.addEventListener("click", closeModals);
exitLS && exitLS.addEventListener("click", closeModals);
exitUM && exitUM.addEventListener("click", closeModals);

// Add a sub-test question
svQ && svQ.addEventListener("submit", e => {
    e.preventDefault();
    const questionText = document.getElementById("l_savol").value.trim();
    const ball = document.getElementById("l_ball").value;
    const opts = variants.map(v => v.value.trim());
    const answerIndex = Array.from(radios).findIndex(r => r.checked);
    if (!questionText || answerIndex < 0) return;
    const obj = { id: currentId++, question: questionText, ball, options: opts, answer: opts[answerIndex] };
    testData.push(obj);
    questionCount++;
    qNumber.textContent = questionCount;
    const box = document.createElement('div');
    box.className = 'box test_savol';
    box.dataset.id = obj.id;
    const titleP = document.createElement('p');
    titleP.className = 'box_title';
    titleP.textContent = obj.question;
    const crud = document.createElement('div');
    crud.className = 'edit_box_crud';
    const delBtn = document.createElement('span');
    delBtn.className = 'delete-btn';
    const delIcon = document.createElement('i');
    delIcon.className = 'fa-solid fa-trash';
    delBtn.appendChild(delIcon);
    crud.appendChild(delBtn);
    box.appendChild(titleP);
    box.appendChild(crud);
    testsWrapper.appendChild(box);
    testsEditWrapper.appendChild(box.cloneNode(true));
    delBtn.addEventListener('click', () => {
        testsWrapper.removeChild(box);
        const clone = testsEditWrapper.querySelector(`[data-id="${obj.id}"]`);
        if (clone) testsEditWrapper.removeChild(clone);
        testData = testData.filter(q => q.id !== obj.id);
        questionCount--;
        qNumber.textContent = questionCount;
    });
    document.getElementById("l_savol").value = "";
    document.getElementById("l_ball").value = "";
    variants.forEach(v => v.value = "");
    radios.forEach(r => r.checked = false);
    littleModal.style.display = "none";
});

// ----- ADD form submissions -----
tForm && tForm.addEventListener("submit", e => {
    e.preventDefault();
    if (!testData.length) return;
    fetch("/admin/add_quiz", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: inputs.t.title.value, theme: inputs.t.theme.value, data: testData }),
    }).then(() => location.reload());
});

qForm && qForm.addEventListener("submit", e => {
    e.preventDefault();
    fetch("/admin/add_matter", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: inputs.q.title.value,
            main: inputs.q.main.value,
            helper: inputs.q.helper.value,
            correct: inputs.q.answer.value,
            ball: inputs.q.ball.value,
            theme: inputs.q.theme.value,
        }),
    }).then(() => location.reload());
});

aForm && aForm.addEventListener("submit", e => {
    e.preventDefault();
    const gif = inputs.a.gif.files[0];
    if (!gif) return alert("Fayl yuklang!");
    const fd = new FormData();
    fd.append("title", inputs.a.title.value);
    fd.append("about", inputs.a.about.value);
    fd.append("theme", inputs.a.theme.value);
    fd.append("gif", gif);
    fetch("/admin/add_animation", { method: "POST", body: fd }).then(() => location.reload());
});

lForm && lForm.addEventListener("submit", e => {
    e.preventDefault();
    const image = inputs.l.image.files[0];
    const zip = inputs.l.zip.files[0];
    if (!image) return alert("Rasm yuklang!");
    const fd = new FormData();
    fd.append("title", inputs.l.title.value);
    fd.append("about", inputs.l.about.value);
    fd.append("link", inputs.l.url.value);
    fd.append("pic", image);
    if (zip) fd.append("zip", zip);
    fetch("/admin/add_lab", { method: "POST", body: fd }).then(() => location.reload());
});

mForm && mForm.addEventListener("submit", e => {
    e.preventDefault();
    fetch("/admin/add_theme", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: inputs.m.title.value, about: inputs.m.about.value }),
    }).then(r => r.json()).then(d => {
        if (d.error) return alert(d.error);
        location.reload();
    });
});

hForm && hForm.addEventListener("submit", e => {
    e.preventDefault();
    fetch("/admin/add_handbook", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            category: inputs.h.category.value,
            title: inputs.h.title.value,
            content: inputs.h.content.value,
            about: inputs.h.about.value,
        }),
    }).then(r => r.json()).then(d => {
        if (d.error) return alert(d.error);
        closeModals();
        loadHandbook();
    });
});

lsForm && lsForm.addEventListener("submit", e => {
    e.preventDefault();
    const f = inputs.ls.file.files[0];
    if (!f) return alert("Fayl yuklang!");
    const fd = new FormData();
    fd.append("title", inputs.ls.title.value);
    fd.append("about", inputs.ls.about.value);
    fd.append("file", f);
    fetch("/admin/add_lesson", { method: "POST", body: fd })
        .then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadLessons();
        });
});

// ----- Theme dropdowns -----
function loadThemes() {
    fetch("/api/themes").then(res => res.json()).then(data => {
        const opts = data.map(item => `<option value="${escapeHtml(item.name)}">${escapeHtml(item.name)}</option>`).join('');
        [inputs.q.theme, inputs.qEdit.theme, inputs.a.theme, inputs.aEdit.theme,
         inputs.t.theme, inputs.tEdit.theme].forEach(sel => {
            if (sel) safeRender(sel, opts);
        });
    });
}

// ----- Search hooks -----
qSearch && qSearch.addEventListener("input", e => loadQuestions(e.target.value.toLowerCase()));
tSearch && tSearch.addEventListener("input", e => loadQuizzes(e.target.value.toLowerCase()));
aSearch && aSearch.addEventListener("input", e => loadAnimationList(e.target.value.toLowerCase()));
lSearch && lSearch.addEventListener("input", e => loadLabs(e.target.value.toLowerCase()));
mSearch && mSearch.addEventListener("input", e => loadThemeList(e.target.value.toLowerCase()));
hSearch && hSearch.addEventListener("input", e => loadHandbook(e.target.value.toLowerCase()));
lsSearch && lsSearch.addEventListener("input", e => loadLessons(e.target.value.toLowerCase()));
uSearch && uSearch.addEventListener("input", e => loadUsers(e.target.value.toLowerCase()));

const EMPTY_HTML = `<span class="edit_empty"><i class="fa-solid fa-box-open"></i><p>Ma'lumot topilmadi</p></span>`;

// ----- List loaders -----
function loadQuestions(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/get_matter" + prefix).then(res => res.json()).then(data => {
        const html = data.length ? data.map(item => `
            <div class="box">
                <p class="box_title">#${item.id} | ${escapeHtml(item.title)}</p>
                <div class="edit_box_crud">
                    <span class="edit_box_eq" onclick="editQuestion(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span class="edit_box_aq" onclick="hiddenQuestion(${item.id})"><i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i></span>
                    <span class="edit_box_dq" onclick="deleteQuestion(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(questionContainer, html);
    });
}

function loadQuizzes(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/get_quiz" + prefix).then(res => res.json()).then(data => {
        const html = data.length ? data.map(item => `
            <div class="box">
                <p class="box_title">#${item.id} | ${escapeHtml(item.title)}</p>
                <div class="edit_box_crud">
                    <span class="edit_box_et" onclick="editQuiz(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span class="edit_box_at" onclick="hiddenQuiz(${item.id})"><i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i></span>
                    <span class="edit_box_dt" onclick="deleteQuiz(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(quizContainer, html);
    });
}

function loadThemeList(searchE) {
    fetch("/api/themes").then(res => res.json()).then(data => {
        const filter = (searchE || "").toLowerCase();
        const filtered = filter ? data.filter(t => t.name.toLowerCase().startsWith(filter)) : data;
        const html = filtered.length ? filtered.map(item => `
            <div class="box">
                <p class="box_title">#${item.id} | ${escapeHtml(item.name)} <small style="color:#888;">— ${escapeHtml(item.about || '')}</small></p>
                <div class="edit_box_crud">
                    <span onclick="editTheme(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span onclick="deleteTheme(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(themesContainer, html);
    });
}

function loadAnimationList(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/get_animation" + prefix).then(res => res.json()).then(data => {
        const html = data.length ? data.map(item => `
            <div class="anima_box">
                <div>
                    <img src="/static/${escapeHtml(item.gif_path)}" style="width: 300px;" alt="">
                    <div class="anima_title">
                        <p><b>Animatsiya nomi:</b> ${escapeHtml(item.title)}</p>
                        <p><b>Ma'lumot:</b> ${escapeHtml(item.about)}</p>
                        <p><b>Bo'lim:</b> ${escapeHtml(item.theme)}</p>
                    </div>
                </div>
                <div class="edit_box_crud">
                    <span onclick="editAnima(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span onclick="deleteAnima(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(animationContainer, html);
    });
}

function loadLabs(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/get_labs" + prefix).then(res => res.json()).then(data => {
        const html = data.length ? data.map(item => `
            <div class="anima_box">
                <div>
                    <img src="/static/${escapeHtml(item.pic_path)}" style="width: 300px;" alt="">
                    <div class="anima_title">
                        <p><b>Laboratoriya nomi:</b> ${escapeHtml(item.title)}</p>
                        <p><b>Ma'lumot:</b> ${escapeHtml(item.about)}</p>
                        ${item.link ? `<p><b>Link:</b> <a href="${escapeHtml(item.link)}" target="_blank" rel="noopener">${escapeHtml(item.link)}</a></p>` : ''}
                    </div>
                </div>
                <div class="edit_box_crud">
                    <span onclick="editLab(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span onclick="deleteLab(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(labContainer, html);
    });
}

function loadHandbook(searchE) {
    fetch("/api/handbook").then(res => res.json()).then(data => {
        const filter = (searchE || "").toLowerCase();
        const filtered = filter
            ? data.filter(i =>
                (i.title || "").toLowerCase().includes(filter) ||
                (i.category || "").toLowerCase().includes(filter))
            : data;
        const html = filtered.length ? filtered.map(item => `
            <div class="box">
                <p class="box_title">[${escapeHtml(item.category)}] ${escapeHtml(item.title)}</p>
                <div class="edit_box_crud">
                    <span onclick="editHandbook(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span onclick="deleteHandbook(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(handbookContainer, html);
    });
}

function loadLessons(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/get_lessons" + prefix).then(res => res.json()).then(data => {
        const html = data.length ? data.map(item => `
            <div class="box">
                <p class="box_title">
                    <span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:800;
                        ${item.file_type === 'pdf' ? 'background:#ef4444;color:white;' : 'background:#2563eb;color:white;'}">
                        ${escapeHtml(item.file_type.toUpperCase())}
                    </span>
                    #${item.id} | ${escapeHtml(item.title)}
                    <small style="color:#888; display:block; margin-top:4px;">${escapeHtml(item.about || '')}</small>
                </p>
                <div class="edit_box_crud">
                    <a href="/lessons/${item.id}" target="_blank" rel="noopener" title="Ko'rish"><i class="fa-solid fa-eye"></i></a>
                    <span onclick="editLesson(${item.id})"><i class="fa-solid fa-pencil"></i></span>
                    <span onclick="deleteLesson(${item.id})"><i class="fa-solid fa-trash"></i></span>
                </div>
            </div>
        `).join('') : EMPTY_HTML;
        safeRender(lessonContainer, html);
    });
}

function loadUsers(searchE) {
    const prefix = searchE ? `?prefix=${encodeURIComponent(searchE)}` : "";
    fetch("/api/users" + prefix).then(res => {
        if (!res.ok) throw new Error("auth");
        return res.json();
    }).then(data => {
        const html = data.length ? data.map(u => `
            <div class="box">
                <p class="box_title">
                    #${u.id} | <b>@${escapeHtml(u.username)}</b>${u.is_admin ? ' <span style="color:#f59e0b;">[ADMIN]</span>' : ''}
                    <small style="color:#888; display:block; margin-top:4px;">
                        ${escapeHtml(u.name)} ${escapeHtml(u.surname)} · ${escapeHtml(u.university)}
                        · ${u.points} ball · ${u.problems_solved} masala · ${u.tests_passed} test
                    </small>
                </p>
                <div class="edit_box_crud">
                    <span onclick="editUser(${u.id})"><i class="fa-solid fa-pencil"></i></span>
                    ${u.is_admin ? '' : `<span onclick="deleteUser(${u.id})"><i class="fa-solid fa-trash"></i></span>`}
                </div>
            </div>
        `).join('') : `<span class="edit_empty"><i class="fa-solid fa-box-open"></i><p>Foydalanuvchi yo'q</p></span>`;
        safeRender(userContainer, html);
    }).catch(err => {
        console.error(err);
        safeRender(userContainer, `<span class="edit_empty"><p>Yuklab bo'lmadi</p></span>`);
    });
}

// ----- DELETE handlers -----
window.deleteQuestion = id => { if (confirm("Masala o'chirilsinmi ?")) fetch(`/api/delete_matter/${id}`, { method: 'DELETE' }).then(() => loadQuestions()); };
window.deleteQuiz = id => { if (confirm("Test o'chirilsinmi ?")) fetch(`/api/delete_quiz/${id}`, { method: 'DELETE' }).then(() => loadQuizzes()); };
window.deleteTheme = id => {
    if (!confirm("Bo'lim o'chirilsinmi ? (Tegishli masalalar/testlar/animatsiyalar bo'limsiz qoladi)")) return;
    fetch(`/api/delete_theme/${id}`, { method: 'DELETE' }).then(() => { loadThemeList(); loadThemes(); });
};
window.deleteAnima = id => { if (confirm("Animatsiya o'chirilsinmi ?")) fetch(`/api/delete_animation/${id}`, { method: 'DELETE' }).then(() => loadAnimationList()); };
window.deleteLab = id => { if (confirm("Labaratoriya o'chirilsinmi ?")) fetch(`/api/delete_labs/${id}`, { method: 'DELETE' }).then(() => loadLabs()); };
window.deleteHandbook = id => { if (confirm("O'chirilsinmi?")) fetch(`/api/delete_handbook/${id}`, { method: 'DELETE' }).then(() => loadHandbook()); };
window.deleteLesson = id => { if (confirm("Mavzu (va fayl) o'chirilsinmi?")) fetch(`/api/delete_lesson/${id}`, { method: 'DELETE' }).then(() => loadLessons()); };
window.deleteUser = id => {
    if (!confirm("Foydalanuvchi va uning barcha natijalari o'chirilsinmi? Bu amalni qaytarib bo'lmaydi.")) return;
    fetch(`/api/delete_user/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(d => { if (d.error) alert(d.error); loadUsers(); });
};

// ----- EDIT handlers -----
window.editQuestion = function (id) {
    openModal(qModal);
    qForm.style.display = "none";
    qFormEdit.style.display = "grid";
    fetch(`/api/get_matter`).then(res => res.json()).then(data => {
        const item = data.find(q => q.id === id);
        if (!item) return;
        inputs.qEdit.title.value = item.title;
        inputs.qEdit.main.value = item.main || "";
        inputs.qEdit.helper.value = item.helper || "";
        inputs.qEdit.answer.value = item.correct;
        inputs.qEdit.ball.value = item.ball;
        inputs.qEdit.theme.value = item.theme;
    });
    qFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_matter", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id,
                title: inputs.qEdit.title.value,
                main: inputs.qEdit.main.value,
                helper: inputs.qEdit.helper.value,
                correct: inputs.qEdit.answer.value,
                ball: inputs.qEdit.ball.value,
                theme: inputs.qEdit.theme.value,
                status: true,
            }),
        }).then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadQuestions();
        });
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
    fetch('/api/get_quiz').then(res => res.json()).then(data => {
        const item = data.find(q => q.id === id);
        if (!item) return;
        inputs.tEdit.title.value = item.title;
        inputs.tEdit.theme.value = item.theme;
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
            const titleP = document.createElement('p');
            titleP.className = 'box_title';
            titleP.textContent = q.question;
            const crud = document.createElement('div');
            crud.className = 'edit_box_crud';
            const delBtn = document.createElement('span');
            delBtn.className = 'delete-btn';
            const delIcon = document.createElement('i');
            delIcon.className = 'fa-solid fa-trash';
            delBtn.appendChild(delIcon);
            crud.appendChild(delBtn);
            box.appendChild(titleP);
            box.appendChild(crud);
            testsEditWrapper.appendChild(box);
            delBtn.addEventListener('click', () => {
                testsEditWrapper.removeChild(box);
                testData = testData.filter(item => item.id !== q.id);
                questionCount--;
                qEditNumber.textContent = questionCount;
            });
            questionCount++;
        });
        qEditNumber.textContent = questionCount;
        currentId = Math.max(0, ...testData.map(q => q.id || 0)) + 1;
    });
    tFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_quiz", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, title: inputs.tEdit.title.value, theme: inputs.tEdit.theme.value, data: testData, status: true }),
        }).then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadQuizzes();
        });
    };
};

window.editTheme = function (id) {
    fetch("/api/themes").then(res => res.json()).then(data => {
        const item = data.find(t => t.id === id);
        if (!item) return;
        inputs.mEdit.title.value = item.name;
        inputs.mEdit.about.value = item.about;
        openModal(themeModal);
        showEditForm(mForm, mFormEdit, modalTitles.m, "Bo'limni tahrirlash");
    });
    mFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_theme", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, name: inputs.mEdit.title.value, about: inputs.mEdit.about.value }),
        }).then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadThemeList();
            loadThemes();
            loadQuestions();
            loadQuizzes();
            loadAnimationList();
        });
    };
};

window.editAnima = function (id) {
    fetch("/api/get_animation").then(res => res.json()).then(data => {
        const item = data.find(g => g.id === id);
        if (!item) return;
        inputs.aEdit.title.value = item.title;
        inputs.aEdit.about.value = item.about;
        inputs.aEdit.theme.value = item.theme;
        inputs.aEdit.gif.value = "";
        openModal(animationModal);
        showEditForm(aForm, aFormEdit, modalTitles.a, "Animatsiyani tahrirlash");
    });
    aFormEdit.onsubmit = function (e) {
        e.preventDefault();
        const fd = new FormData();
        fd.append("id", id);
        fd.append("title", inputs.aEdit.title.value);
        fd.append("about", inputs.aEdit.about.value);
        fd.append("theme", inputs.aEdit.theme.value);
        if (inputs.aEdit.gif.files[0]) fd.append("gif", inputs.aEdit.gif.files[0]);
        fetch("/admin/edit_animation", { method: "POST", body: fd })
            .then(r => r.json()).then(d => {
                if (d.error) return alert(d.error);
                closeModals();
                loadAnimationList();
            });
    };
};

window.editLab = function (id) {
    fetch("/api/get_labs").then(res => res.json()).then(data => {
        const item = data.find(l => l.id === id);
        if (!item) return;
        inputs.lEdit.title.value = item.title;
        inputs.lEdit.about.value = item.about;
        inputs.lEdit.url.value = item.link || "";
        inputs.lEdit.image.value = "";
        inputs.lEdit.zip.value = "";
        openModal(labModal);
        showEditForm(lForm, lFormEdit, modalTitles.l, "Labaratoriyani tahrirlash");
    });
    lFormEdit.onsubmit = function (e) {
        e.preventDefault();
        const fd = new FormData();
        fd.append("id", id);
        fd.append("title", inputs.lEdit.title.value);
        fd.append("about", inputs.lEdit.about.value);
        fd.append("link", inputs.lEdit.url.value);
        if (inputs.lEdit.image.files[0]) fd.append("pic", inputs.lEdit.image.files[0]);
        if (inputs.lEdit.zip.files[0]) fd.append("zip", inputs.lEdit.zip.files[0]);
        fetch("/admin/edit_lab", { method: "POST", body: fd })
            .then(r => r.json()).then(d => {
                if (d.error) return alert(d.error);
                closeModals();
                loadLabs();
            });
    };
};

window.editHandbook = function (id) {
    fetch("/api/handbook").then(res => res.json()).then(data => {
        const item = data.find(h => h.id === id);
        if (!item) return;
        inputs.hEdit.category.value = item.category;
        inputs.hEdit.title.value = item.title;
        inputs.hEdit.content.value = item.content;
        inputs.hEdit.about.value = item.about || "";
        openModal(hModal);
        showEditForm(hForm, hFormEdit, modalTitles.h, "Qo'llanmani tahrirlash");
    });
    hFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_handbook", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id,
                category: inputs.hEdit.category.value,
                title: inputs.hEdit.title.value,
                content: inputs.hEdit.content.value,
                about: inputs.hEdit.about.value,
            }),
        }).then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadHandbook();
        });
    };
};

window.editLesson = function (id) {
    fetch("/api/get_lessons").then(res => res.json()).then(data => {
        const item = data.find(l => l.id === id);
        if (!item) return;
        inputs.lsEdit.title.value = item.title;
        inputs.lsEdit.about.value = item.about || "";
        inputs.lsEdit.file.value = "";
        openModal(lessonModal);
        showEditForm(lsForm, lsFormEdit, modalTitles.ls, "Mavzuni tahrirlash");
    });
    lsFormEdit.onsubmit = function (e) {
        e.preventDefault();
        const fd = new FormData();
        fd.append("id", id);
        fd.append("title", inputs.lsEdit.title.value);
        fd.append("about", inputs.lsEdit.about.value);
        if (inputs.lsEdit.file.files[0]) fd.append("file", inputs.lsEdit.file.files[0]);
        fetch("/admin/edit_lesson", { method: "POST", body: fd })
            .then(r => r.json()).then(d => {
                if (d.error) return alert(d.error);
                closeModals();
                loadLessons();
            });
    };
};

window.editUser = function (id) {
    fetch("/api/users").then(res => res.json()).then(data => {
        const u = data.find(x => x.id === id);
        if (!u) return;
        inputs.uEdit.username.value = u.username;
        inputs.uEdit.name.value = u.name;
        inputs.uEdit.surname.value = u.surname;
        inputs.uEdit.university.value = u.university;
        openModal(userModal);
    });
    uFormEdit.onsubmit = function (e) {
        e.preventDefault();
        fetch("/api/edit_user", {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id,
                name: inputs.uEdit.name.value,
                surname: inputs.uEdit.surname.value,
                university: inputs.uEdit.university.value,
            }),
        }).then(r => r.json()).then(d => {
            if (d.error) return alert(d.error);
            closeModals();
            loadUsers();
        });
    };
};

// ----- TOGGLE status -----
window.hiddenQuestion = function (id) {
    fetch('/api/toggle_matter_status', {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id }),
    }).then(() => { loadQuestions(); closeModals(); });
};
window.hiddenQuiz = function (id) {
    fetch('/api/toggle_quiz_status', {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id }),
    }).then(() => { loadQuizzes(); closeModals(); });
};

// ----- Init -----
loadThemes();
loadQuestions();
loadQuizzes();
loadThemeList();
loadAnimationList();
loadLabs();
loadHandbook();
loadLessons();
