const form = document.querySelector("#login-form");

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

  // 로그인 성공 or 에러 처리
  if (res.status === 200) {
    // 성공
    //alert("로그인에 성공했습니다.");
    const accessToken = data.access_token;
    window.localStorage.setItem("token", accessToken);
    //window.sessionStorage.setItem("token", accessToken);
    alert("로그인되었습니다.");

    // const infoDiv = document.querySelector("#info");
    // infoDiv.innerText = "로그인되었습니다";

    window.location.pathname = "/";

    // const btn = document.createElement("button");
    // btn.innerText = "상품 가져오기";
    // btn.addEventListener("click", async () => {
    //   const res = await fetch("/items", {
    //     headers: {
    //       Authorization: `Bearer ${accessToken}`, //bearer : prefix
    //     },
    //   });

    //   const data = await res.json();
    //   console.log(data);
    // });
    // infoDiv.appendChild(btn);

    //window.location.pathname = "/";
  } else if (res.status === 401) {
    // Unauthorized
    alert("id 혹은 password가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleSubmit);
