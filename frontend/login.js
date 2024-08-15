const form = document.querySelector("#login-form");

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
  //console.log(formData.get("password"));

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });

  const data = await res.json();
  console.log("access token : ", data);

  // 로그인 성공 or 에러 처리
  if (res.status === 200) {
    // 성공
    alert("로그인에 성공했습니다.");
    window.location.pathname = "/";
  } else if (res.status === 401) {
    // Unauthorized
    alert("id 혹은 password가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleSubmit);
