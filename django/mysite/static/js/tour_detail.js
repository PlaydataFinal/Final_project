const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function (element) {
    element.addEventListener('click', function () {
        Swal.fire({
            title: '정말로 삭제하시겠습니까?',
            html: "삭제하면 다시 되돌릴 수 없습니다.<br>신중하세요.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '지울래요',
            cancelButtonText: '안할래요',
            reverseButtons: true, // 버튼 순서 거꾸로
        }).then((confirmed) => {
            if (Object.values(confirmed)[0])
                location.href = this.dataset.uri;
        });
    });
});

const like_elements = document.getElementsByClassName("like");
Array.from(like_elements).forEach(function (element) {
    element.addEventListener('click', function () {
        Swal.fire({
            title: '정말로 추천하시겠습니까?',
            html: "추천은 한번만 적용되고<br>취소가 불가능합니다.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '추천이요',
            cancelButtonText: '안할래요',
            reverseButtons: true, // 버튼 순서 거꾸로
        }).then((confirmed) => {
            if (Object.values(confirmed)[0])
                location.href = this.dataset.uri;
        });
    });
});
function like_self() {
    Swal.fire({
        title: '본인 의견 추천',
        html: "본인이 작성한 의견은 추천이 불가합니다.",
        icon: 'error'
    })
};
function duplicatedLike() {
    Swal.fire({
        title: '이미 추천하셨습니다.',
        html: "여행지 당 한번만 추천 가능합니다.",
        icon: 'error'
    })
};
function notLogin() {
    Swal.fire({
        title: '추천은 로그인 후 가능합니다.',
        html: "로그인 페이지로 이동합니다.",
        icon: 'error'
    }).then(function () {
        var link = window.location.href;
        var list = link.split('/');
        list.splice(0, 3);
        var redir = '/'.concat(list.join('/'));
        location.href = loginURL + redir;
    })
};
const colors = ['#FC4F4F', '#FFBC80', '#FF9F45', '#F76E11']
// const shapes = ['square', 'circle', 'triangle', 'heart']
const shapes = ['heart']

const randomIntBetween = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

class Particle {
    constructor({ x, y, rotation, shape, color, size, duration, parent }) {
        this.x = x
        this.y = y
        this.parent = parent
        this.rotation = rotation
        this.shape = shape
        this.color = color
        this.size = size
        this.duration = duration
        this.children = document.createElement('div')
    }

    draw() {
        this.children.style.setProperty('--x', this.x + 'px')
        this.children.style.setProperty('--y', this.y + 'px')
        this.children.style.setProperty('--r', this.rotation + 'deg')
        this.children.style.setProperty('--c', this.color)
        this.children.style.setProperty('--size', this.size + 'px')
        this.children.style.setProperty('--d', this.duration + 'ms')
        this.children.className = `shape ${this.shape}`
        this.parent.append(this.children)
    }

    animate() {
        this.draw()

        const timer = setTimeout(() => {
            this.parent.removeChild(this.children)
            clearTimeout(timer)
        }, this.duration)
    }
}

function animateParticles({ total }) {
    for (let i = 0; i < total; i++) {
        const particle = new Particle({
            x: randomIntBetween(-200, 200),
            y: randomIntBetween(-100, -300),
            rotation: randomIntBetween(-360 * 5, 360 * 5),
            shape: shapes[randomIntBetween(0, shapes.length - 1)],
            color: colors[randomIntBetween(0, colors.length - 1)],
            size: randomIntBetween(4, 7),
            duration: randomIntBetween(400, 800),
            parent
        })
        particle.animate()
    }
}

const parent = document.querySelector('span2')
parent.addEventListener("touchstart", () => { }, false);
parent.addEventListener('click', function () {
    Swal.fire({
        title: '정말로 추천하시겠습니까?',
        html: "추천은 한번만 적용되고<br>취소가 불가능합니다.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '추천해요!',
        cancelButtonText: '안할래요',
        reverseButtons: true, // 버튼 순서 거꾸로
    }).then((confirmed) => {
        if (Object.values(confirmed)[0]) {
            animateParticles({ total: 40 });
            setTimeout(1000);
            location.href = this.dataset.uri;
        };
    });
});