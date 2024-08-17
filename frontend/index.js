{
  /* <div class="items-list">
        <div class="item-list__img">
          <img src="img/cat_feet.jpg" alt="img" />
        </div>
        <div class="item-list__info">
          <div class="item-list__info-title">고양이 젤리 말랑</div>
          <div class="item-list__info-meta">무타 1분전</div>
          <div class="item-list__info-price">1만원</div>
        </div>
    </div> */
}

// 데이터 html에 올리기
const renderData = (data) => {
  const main = document.querySelector("main");

  data.reverse().forEach(async (obj) => {
    // reverse() list의 순서를 거꾸로 해준다.
    const div = document.createElement("div");
    div.className = "items-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    if (blob.size > 0) {
      const url = URL.createObjectURL(blob);
      img.src = url;
    } else {
      img.src = "/img/img.svg";
    }

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "item-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "item-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);
    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);

    main.appendChild(div);
  });
};

// backend에서 데이터 가져오기기
const fetchList = async () => {
  // token 가져오기
  const accessToken = window.localStorage.getItem("token");
  const res = await fetch("/items", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // token이 없을 경우,
  if (res.status === 401) {
    alert("로그인이 필요합니다.");
    window.location.pathname = "/login.html";
    return;
  }
  const data = await res.json();
  renderData(data);
};

fetchList();
