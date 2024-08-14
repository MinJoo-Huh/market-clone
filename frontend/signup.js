const form = document.querySelector("#signup-form");

// 비밀번호 확인 함수
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

// submit 제출되었을 때 함수
const handleSubmit = async (event) => {
  event.preventDefault();

  // form 정보 가져오기기
  const formData = new FormData(form);
  // hash 함수 사용
  const sha256Pw = sha256(formData.get("password"));
  formData.set("password", sha256Pw);
  console.log(formData.get("password"));

  // 비밀번호 확인용
  const div = document.querySelector("#info");

  // 비밀번호 확인
  if (checkPassword()) {
    // true
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });

    const data = await res.json();

    // data가 제대로 갔을 경우, 회원가입에 성공
    if (data === "200") {
      div.innerText = "회원가입에 성공했습니다!";
      div.style.color = "blue";
    }
  } else {
    // false
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
