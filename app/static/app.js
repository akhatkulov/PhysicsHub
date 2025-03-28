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

fetch("/admin/questions")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            q_box.innerHTML += `
                <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.title}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-edit"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-circle"></i>
                        </span>
                    </div>
                </div>
    `

        })

    })

fetch("/admin/quizs")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            t_box.innerHTML += `
            <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.title}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-edit"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-circle"></i>
                        </span>
                    </div>
                </div>
            `
        })
    })
fetch("/api/questions")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            q_box.innerHTML += `
                <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.title}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-edit"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-circle"></i>
                        </span>
                    </div>
                </div>
    `

        })

    })


fetch("/admin/quizs")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item => {
            t_box.innerHTML += `
            <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.title}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-edit"></i>
                        </span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-circle"></i>
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
