<script>
  import { onMount } from "svelte";
  import { getDatabase, ref, onValue } from "firebase/database";
  import Nav from "../components/Nav.svelte";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  $: items = []; //반응형 변수로 선언됨. 랜더링

  // 시간 바꾸기
  const calcTime = (Timestamp) => {
    // 한국시간 UTC+9
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - Timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
    else return "방금 전";
  };

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val(); // object 형식으로 가져옴.
      items = Object.values(data).reverse(); // reverse() 순서 거꾸로
    });
  });
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chartbar.svg" alt="chartbar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery-50.svg" alt="battery-50" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <img src="assets/arrow-down.svg" alt="arrow-down" />
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/menu.svg" alt="menu" />
      <img src="assets/bell.svg" alt="bell" />
    </div>
  </div>
</header>
<main>
  {#each items as item}
    <div class="items-list">
      <div class="item-list__img">
        <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="item-list__info-price">{item.price}</div>
        <div>{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+글쓰기</a>
</main>

<Nav location="home" />

<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>

<style>
  .info-bar__time {
    color: blue;
  }
</style>
