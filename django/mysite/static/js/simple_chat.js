const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerSelect = get(".msger-select");
const msgerChat = get(".msger-chat");

// Icons made by Freepik from www.flaticon.com
// const BOT_IMG = "https://cdn3.vectorstock.com/i/1000x1000/31/67/robot-icon-bot-sign-design-chatbot-symbol-vector-27973167.jpg";
// const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "CHAT BOT";

// 비로그인 시 로그인 요청
if (PERSON_NAME == "비회원") {
  window.onload = function () {
    Swal.fire({
      icon: 'warning',
      title: '로그인 후 사용가능합니다.',
      text: '로그인 페이지로 이동합니다.',
    }).then(function () {
      var link = window.location.href;
      var list = link.split('/');
      list.splice(0, 3);
      var redir = '/'.concat(list.join('/'));
      location.href = loginURL + redir;
    })
  };

  // 뒤로가기 편법 컷
  window.onpageshow = function (event) {
    if (event.persisted || (window.performance && window.performance.navigation.type == 2)) {
      Swal.fire({
        icon: 'error',
        title: '로그인 후 사용가능합니다.',
        text: '로그인 페이지로 이동합니다.',
      }).then(function () {
        var link = window.location.href;
        var list = link.split('/');
        list.splice(0, 3);
        var redir = '/'.concat(list.join('/'));
        location.href = loginURL + redir;
      })
    }
  }
};

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  const msgSelect = msgerSelect.value;

  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  // alert("wait a seconds...");
  // 여기서 ajax 통신을 통해 모델 호출
  // https://hooongs.tistory.com/23
  // https://shiningyouandme.tistory.com/23

  $.ajax({
    //요청이 전송될 URL 주소
    url: '../chatbot_solve/',
    type: "POST",
    dataType: "JSON",
    data: {
      'input': msgText,
      'selected_number': msgSelect,
    },
    success: function (data) {
      const port_data = JSON.stringify(data);
      var port_data_json = JSON.parse(port_data);
      botResponse(port_data_json.output_text);
    },
    error: function (xhr, textStatus, thrownError) {
      alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
    }
  });

  msgerInput.value = "";
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(text) {
  const msgText = text.replace(/\n/g, '<br>').replace(/\. /g, '.<br>');
  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  });
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

// $.ajax({
//   //요청이 전송될 URL 주소
//   url: 'test2/',
//   type: "POST",
//   dataType: "JSON",
//   data: {
//     'input': msgText,
//     csrfmiddlewaretoken: '{{ csrf_token }}'
//   },
//   headers: { "X-CSRFToken": "{{ csrf_token }}" },

//   success: function (data) {

//     const port_data = JSON.stringify(data);
//     var port_data_json = JSON.parse(port_data);
//   },
//   error: function (xhr, textStatus, thrownError) {
//     alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
//   }
// });

