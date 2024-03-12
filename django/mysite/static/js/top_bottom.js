$("#top-circle").click(function () {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })
})

$("#bottom-circle").click(function () {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    })
})