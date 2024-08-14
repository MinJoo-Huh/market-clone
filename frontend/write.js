const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();

  // body에서 받은 데이터 보내기
  const body = new FormData(form);
  // 세계 시간 기준;;
  body.append("insertAt", new Date().getTime()); // insertAt 데이터 추가하기

  try {
    const res = await fetch("/items", {
      method: "POST",
      body, // body : body,
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/"; // 데이터 보내면 다시 홈 화면으로 돌아가기.
  } catch (e) {
    console.error(e.toString()); // 문자열 안주면 에러남...
  } // try 하다가 error가 나면 catch 를 실행.
};

form.addEventListener("submit", handleSubmitForm);
