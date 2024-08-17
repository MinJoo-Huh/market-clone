<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Nav.svelte";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";
  import Nav from "../components/Nav.svelte";

  let title;
  let price;
  let description;
  let place;
  let files;

  const storage = getStorage();
  const db = getDatabase();

  function writeUserData(imgUrl) {
    push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });
    alert("글쓰기 완료"); // 실제로는 잘 안쓰는 UX
    window.location.hash = "/";

    // 'file' comes from the Blob or File API
    // uploadBytes(storageRef, file).then((snapshot) => {
    //   console.log("Uploaded a blob or file!");
    // });
  }

  // $: if (files) console.log(files[0]); // files가 바뀔때마다 찍히게

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, "/imgs" + name);
    const res = await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef);

    return url;
  };

  const handleSubmit = async () => {
    const url = await uploadFile();
    writeUserData(url);
  };
</script>

<!-- <div>
  form 안에 하니깐 submit이랑 상충해서 안먹음
  <button on:click={uploadFile}>테스트</button>
</div> -->

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <!--event동작 멈춤 추가 가능-->
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">제출</button>
  </div>
</form>

<Nav location="write" />

<style>
  .write-button {
    background-color: rgb(254, 111, 15);
    margin: 10px;
    border-radius: 10px;
    padding: 5px 12px 5px 12px;
    color: white;
    cursor: pointer;
  }
</style>
