const modals = document.querySelector(".modals")
const modal = document.querySelector(".modal")
const q_modal = document.querySelector(".question_modal")
const t_modal = document.querySelector(".test_modal")
const question = document.querySelector(".question")
const test = document.querySelector(".test")
const exit_q = document.querySelector(".q_exit")
const exit_t = document.querySelector(".t_exit")
const exit_l = document.querySelector(".l_exit")
const exit_m = document.querySelector(".m_exit")
const sv_q = document.querySelector(".sv_q")
const little_modal = document.querySelector(".little_modal")
const t_plus = document.querySelector(".t_plus")
const q_form = document.querySelector(".q_form")
const t_form = document.querySelector(".t_form")
const m_form = document.querySelector(".m_form")
const title = document.getElementById("title")
const t_title = document.getElementById("t_title")
const m_title = document.getElementById("m_title")
const shart = document.getElementById("shart")
const izoh = document.getElementById("izoh")
const javob = document.getElementById("javob")
const mavzusi = document.getElementById("mavzusi")
const t_mavzusi = document.getElementById("t_mavzusi")
const l_savol = document.getElementById("l_savol")
const variant1 = document.getElementById("variant1")
const variant2 = document.getElementById("variant2")
const variant3 = document.getElementById("variant3")
const variant4 = document.getElementById("variant4")
const tests_w = document.querySelector(".tests--wrapper")
const radio = document.querySelectorAll(".radio")
const q_number = document.querySelector(".q_number")
const theme = document.querySelector(".theme")
const themes = document.querySelector(".theme_modal")
const q_box = document.querySelector(".q_box")
const t_box = document.querySelector(".t_box")
const th_box = document.querySelector(".th_box")

question.addEventListener("click", () => {
    modals.style.display = "flex"
    q_modal.style.display = "grid"
})
test.addEventListener("click", () => {
    modals.style.display = "flex"
    t_modal.style.display = "grid"
    let tests_arr = []
    l = 0
    s = 0
    sv_q.addEventListener("submit", (e) => {
        e.preventDefault()
        let tests_obj = {
            savol: l_savol.value,
            variant1: variant1.value,
            variant2: variant2.value,
            variant3: variant3.value,
            variant4: variant4.value,
            javob: "",
            act: "active"
        }
        radio.forEach(e => {
            if (e.checked) {
                tests_obj.javob = e.value
            }

        })
        l_savol.value = ""
        variant1.value = ""
        variant2.value = ""
        variant3.value = ""
        variant4.value = ""
        tests_arr.push(tests_obj)
        s += 1
        q_number.innerHTML = s

        l++
        tests_w.innerHTML += `
                <div class="savol_box">
                        <span><i>${tests_obj.savol}</i></span>
                        <span class="the_end">
                            . . .
                        </span>
                        <span class="t_edit ${l}">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                </div>
        `
        const t_edit = document.querySelectorAll(".t_edit")
        const savol_box = document.querySelectorAll(".savol_box")
        t_edit.forEach(e => {
            e.addEventListener("click", () => {
                delete_obj = Number(e.classList[1])
                delete tests_arr[delete_obj - 1]
                savol_box[delete_obj - 1].style.display = "none"
                s -= 1
                q_number.innerHTML = s

            })
        })
        little_modal.style.display = "none"
    })
    t_form.addEventListener("submit", (e) => {
        e.preventDefault()
        let t_obj = {
            title: t_title.value,
            mavzular: t_mavzusi.value,
            testlar: tests_arr
        }
        modals.style.display = "none"
        t_modal.style.display = "none"
        console.log(t_obj);

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
    let q_opj = {
        title: title.value,
        shart: shart.value,
        izoh: izoh.value,
        javob: javob.value,
        mavzular: mavzusi.value,
        act: "active"
    }
    title.value = ""
    shart.value = ""
    izoh.value = ""
    javob.value = ""
    console.log(q_opj);
    fetch("/admin/add_matter",{
        method:"POST",
        body: JSON.stringify({
            title:q_opj.title,
            main:q_opj.shart,
            helper:q_opj.izoh,
            theme:q_opj.mavzular,
            correct:q_opj.javob
        })
    })
    //bach-endga post yuborish-------

    modals.style.display = "none"
    q_modal.style.display = "none"
})

theme.addEventListener("click", () => {
    modals.style.display = "flex"
    themes.style.display = "grid"
})

m_form.addEventListener("submit", (e) => {
    e.preventDefault()
    console.log(m_title.value);
    modals.style.display = "none"
    themes.style.display = "none"
    m_title.value = ""
})

fetch("./static/moduls/question.json")
    .then(rec => rec.json())
    .then(data => {
        data.forEach(item =>{
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

fetch("./static/moduls/test.json")
    .then(rec => rec.json())
    .then(data =>{
        data.forEach(item =>{
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

fetch("./static/moduls/theme.json")
.then(rec=>rec.json())
.then(data =>{
    data.forEach(item =>{
        th_box.innerHTML += `
            <div class="box">
                    <div class="savol_box">
                        <span class="q_name"><i>${item.title}</i></span>
                        <span class="t_edit ">
                            <i class="fa-solid fa-xmark"></i>
                        </span>
                    </div>
                </div>
            `
    })
})