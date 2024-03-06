const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "CHAT BOT";
const PERSON_NAME = "Sajad";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  alert("wait a seconds...");
  // 여기서 ajax 통신을 통해 모델 호출
  // https://hooongs.tistory.com/23
  // https://shiningyouandme.tistory.com/23

  $.ajax({
    //요청이 전송될 URL 주소
    url: '../test2/',
    type: "POST",
    dataType: "JSON",
    data: {
      'input': msgText,
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
  // const r = random(0, BOT_MSGS.length - 1);
  const msgText = text.replace(/\n/g, '<br>');
  // const msgText2 = msgText.replace(/\n/g, '<br>')
  // const delay = msgText.split(" ").length * 100;
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

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
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
