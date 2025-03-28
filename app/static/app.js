const modals = document.querySelector(".modals");
const modal = document.querySelector(".modal");
const q_modal = document.querySelector(".question_modal");
const t_modal = document.querySelector(".test_modal");
const question = document.querySelector(".question");
const test = document.querySelector(".test");
const exit_q = document.querySelector(".q_exit");
const exit_t = document.querySelector(".t_exit");
const exit_l = document.querySelector(".l_exit");
const exit_m = document.querySelector(".m_exit");
const sv_q = document.querySelector(".sv_q");
const little_modal = document.querySelector(".little_modal");
const t_plus = document.querySelector(".t_plus");
const q_form = document.querySelector(".q_form");
const t_form = document.querySelector(".t_form");
const m_form = document.querySelector(".m_form");
const title = document.getElementById("title");
const t_title = document.getElementById("t_title");
const m_title = document.getElementById("m_title");
const m_about = document.getElementById("m_about");
const shart = document.getElementById("shart");
const izoh = document.getElementById("izoh");
const javob = document.getElementById("javob");
const ball_q = document.getElementById("ball_q");
const mavzusi = document.getElementById("mavzusi");
const t_mavzusi = document.getElementById("t_mavzusi");
const l_savol = document.getElementById("l_savol");
const l_ball = document.getElementById("l_ball");
const variant1 = document.getElementById("variant1");
const variant2 = document.getElementById("variant2");
const variant3 = document.getElementById("variant3");
const variant4 = document.getElementById("variant4");
const tests_w = document.querySelector(".tests--wrapper");
const radio = document.querySelectorAll(".radio");
const q_number = document.querySelector(".q_number");
const theme = document.querySelector(".theme");
const themes = document.querySelector(".theme_modal");
const q_box = document.querySelector(".q_box");
const t_box = document.querySelector(".t_box");
const th_box = document.querySelector(".th_box");
const edit_q = document.querySelector(".edit_q");
const edit_t = document.querySelector(".edit_t");

question.addEventListener("click", () => {
    modals.style.display = "flex"
    q_modal.style.display = "grid"
})
let id = 0;
test.addEventListener("click", () => {
    modals.style.display = "flex"
    t_modal.style.display = "grid"
    let tests_arr = []
    l = 0
    s = 0
    sv_q.addEventListener("submit", (e) => {
        e.preventDefault()
        let tests_obj = {
            id: id,
            question: l_savol.value,
            ball: l_ball.value,
            options: [
                variant1.value,
                variant2.value,
                variant3.value,
                variant4.value,
            ],
            answer: "",
        }
        id++;
        radio.forEach(e => {
            if (e.checked) {
                tests_obj.answer = tests_obj.options[e.value];
            }

        })
        l_savol.value = ""
        l_ball.value = ""
        variant1.value = ""
        variant2.value = ""
        variant3.value = ""
        variant4.value = ""
        tests_arr.push(tests_obj)
        s += 1
        q_number.innerHTML = s
        l++
        tests_w.innerHTML += `
                <div class="savol_box test_savol">
                        <span><i>${tests_obj.question}</i></span>
                        <span class="the_end">
                            . . .
                        </span>
                        <span class="t_edit ${l}">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                </div>
        `
        const t_edit = document.querySelectorAll(".t_edit")
        const test_box = document.querySelectorAll(".test_savol")
        t_edit.forEach(e => {
            e.addEventListener("click", () => {
                delete_obj = Number(e.classList[1])
                delete tests_arr[delete_obj - 1]
                test_box[delete_obj - 1].style.display = "none"
                s -= 1
                q_number.innerHTML = s
            })
        })
        little_modal.style.display = "none"
    })
    t_form.addEventListener("submit", (e) => {
        console.log(t_mavzusi);

        if (s != 0) {
            e.preventDefault()
            tests_arr = tests_arr.filter(item => item !== undefined);
            let t_obj = {
                title: t_title.value,
                theme: t_mavzusi.value,
                data: tests_arr,
                status: "active"
            }
            fetch("/admin/add_quiz", {
                method: "POST",
                body: JSON.stringify({
                    title: t_obj.title,
                    theme: t_obj.theme,
                    data: t_obj.data
                })
            })

            modals.style.display = "none"
            t_modal.style.display = "none"
            console.log(t_obj);
            // location.reload()
        }

    })
})

exit_q.addEventListener("click", () => {
    modals.style.display = "none"
    q_modal.style.display = "none"
})
exit_t.addEventListener("click", () => {
    modals.style.display = "none"
    t_modal.style.display = "none"
})
exit_l.addEventListener("click", () => {
    modals.style.display = "none"
    t_modal.style.display = "none"
})
exit_m.addEventListener("click", () => {
    modals.style.display = "none"
    themes.style.display = "none"
})

t_plus.addEventListener("click", () => {
    little_modal.style.display = "flex"
    modal.style.display = "grid"
})
exit_l.addEventListener("click", () => {
    little_modal.style.display = "none"
    modal.style.display = "none"
    modals.style.display = "flex"
    t_modal.style.display = "grid"
})
q_form.addEventListener("submit", (e) => {
    e.preventDefault()
    let q_obj = {
        title: title.value,
        shart: shart.value,
        izoh: izoh.value,
        javob: javob.value,
        ball_q: ball_q.value,
        mavzular: mavzusi.value,
        act: "active"
    }
    title.value = ""
    shart.value = ""
    izoh.value = ""
    javob.value = ""
    ball_q.value = ""
    console.log(q_obj);
    fetch("/admin/add_matter", {
        method: "POST",
        body: JSON.stringify({
            title: q_obj.title,
            main: q_obj.shart,
            helper: q_obj.izoh,
            theme: q_obj.mavzular,
            correct: q_obj.javob,
            ball: q_obj.ball_q
        })
    })
    //bach-endga post yuborish-------
    modals.style.display = "none"
    q_modal.style.display = "none"
    location.reload()
})

theme.addEventListener("click", () => {
    modals.style.display = "flex"
    themes.style.display = "grid"
})

m_form.addEventListener("submit", (e) => {
    e.preventDefault()
    fetch("/admin/add_theme", {
        method: "POST",
        body: JSON.stringify({
            name: m_title.value,
            about: m_about.value
        })
    })
    console.log({
        name: m_title.value,
        about: m_about.value
    });

    modals.style.display = "none"
    themes.style.display = "none"
    m_title.value = ""
    location.reload()
})

fetch("/api/themes")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            th_box.innerHTML += `
            <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.name}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                    </div>
                </div>
            `
        })
    })
fetch("/api/themes")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            mavzusi.innerHTML += `
                <option value="${item.name}">${item.name}</option>
            `
            t_mavzusi.innerHTML += `
                <option value="${item.name}">${item.name}</option>
            `

        })
    })

edit_q.addEventListener(("click"), () => {
    document.querySelector(".edit_search_modal").style.display = "flex"

    fetch("/api/get_matter")
        .then(rec => rec.json())
        .then(data => {
            document.querySelector(".edit_boxs").innerHTML = "";
            if (data.length > 0) {
                data.forEach(item => {
                    document.querySelector(".edit_boxs").innerHTML += `
                        <div class="edit_box">
                            <p class="edit_box_title">
                            ${item.id}.    
                            ${item.title}
                            </p>
                            <div class="edit_box_crud">
                                <span class="edit_box_eq">
                                    <i class="fa-solid fa-pencil"></i>
                                </span>
                                <span class="edit_box_aq">
                                    <i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i>
                                </span>
                                <span class="edit_box_dq">
                                    <i class="fa-solid fa-trash"></i>
                                </span>
                            <div>
                        </div>
                    `;
                })
            } else {
                document.querySelector(".edit_boxs").innerHTML = `
                    <span class="edit_empty">
                        <i class="fa-solid fa-box-open"></i>
                        <p>Ma'lumot topilmadi</p>
                    </span>
                `;
            }
        })
        .catch(error => console.log(error))
    searchFunc("/api/get_matter", "q")
})



edit_t.addEventListener(("click"), () => {
    document.querySelector(".edit_search_modal").style.display = "flex"

    fetch("/api/get_quiz")
        .then(rec => rec.json())
        .then(data => {
            document.querySelector(".edit_boxs").innerHTML = "";
            if (data.length > 0) {
                data.forEach(item => {
                    document.querySelector(".edit_boxs").innerHTML += `
                        <div class="edit_box">
                            <p class="edit_box_title">
                            ${item.id}.    
                            ${item.title}
                            </p>
                            <div class="edit_box_crud">
                                <span class="edit_box_et">
                                    <i class="fa-solid fa-pencil"></i>
                                </span>
                                <span class="edit_box_at">
                                    <i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i>
                                </span>
                                <span class="edit_box_dt">
                                    <i class="fa-solid fa-trash"></i>
                                </span>
                            <div>
                        </div>
                    `;
                })
            } else {
                document.querySelector(".edit_boxs").innerHTML = `
                    <span class="edit_empty">
                        <i class="fa-solid fa-box-open"></i>
                        <p>Ma'lumot topilmadi</p>
                    </span>
                `;
            }
        })
        .catch(error => console.log(error))
    searchFunc("/api/get_quiz", "t")
})



function searchFunc(p, q) {
    let interval = null;
    document.getElementById("edit_search_input").addEventListener("input", (e) => {
        if (interval) return
        interval = setTimeout(() => {
            let prefix = e.target.value.trim();

            let url = prefix === "" ? p : `${p}?prefix=${prefix}`;

            console.log(document.querySelector(".edit_loader"));

            document.querySelector(".edit_loader").style.display = "flex";

            fetch(url)
                .then(rec => rec.json())
                .then(data => {
                    document.querySelector(".edit_boxs").innerHTML = "";
                    if (data.length > 0) {
                        data.forEach(item => {
                            document.querySelector(".edit_boxs").innerHTML += `
                                <div class="edit_box">
                                    <p class="edit_box_title">
                                    ${item.id}.    
                                    ${item.title}
                                    </p>
                                    <div class="edit_box_crud">
                                        <span class="edit_box_e${q}">
                                            <i class="fa-solid fa-pencil"></i>
                                        </span>
                                        <span class="edit_box_a${q}">
                                            <i class="fa-solid fa-eye${item.status ? "" : "-slash"}"></i>
                                        </span>
                                        <span class="edit_box_d${q}">
                                            <i class="fa-solid fa-trash"></i>
                                        </span>
                                    <div>
                                </div>
                            `;
                        })
                    } else {
                        document.querySelector(".edit_boxs").innerHTML = `
                            <span class="edit_empty">
                                <i class="fa-solid fa-box-open"></i>
                                <p>Ma'lumot topilmadi</p>
                            </span>
                        `;
                    }
                })
                .catch(error => console.log(error))
            document.querySelector(".edit_loader").style.display = "none";
            interval = null;
        }, 1000);
    })
}

document.querySelector(".search_exit").addEventListener("click", () => {
    document.querySelector(".edit_search_modal").style.display = "none"
    document.querySelector(".edit_boxs").innerHTML = "";
    document.getElementById("edit_search_input").value = "";
})