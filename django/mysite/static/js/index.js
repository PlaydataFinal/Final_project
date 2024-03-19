
function alreadyLogin() {
    Swal.fire({
        icon: 'info',
        title: '로그인 상태',
        text: '이미 회원이십니다.',
    })
}

function goSignup() {
    Swal.fire({
        title: '아직 회원이 아니시군요',
        html: "회원가입을 하러가실까요?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '네!',
        cancelButtonText: '안할래요',
        reverseButtons: true, // 버튼 순서 거꾸로
    }).then((confirmed) => {
        if (Object.values(confirmed)[0])
            location.href = '{% url "common:signup" %}';
    });
}