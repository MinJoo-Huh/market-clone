<script>
  import Login from "./pages/Login.svelte"; // 모듈 방식
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    getAuth,
    GoogleAuthProvider,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import Loading from "./pages/Loading.svelte";
  import Mypage from "./pages/Mypage.svelte";
  // import { GoogleAuthProvider } from "firebase/auth";

  // const provider = new GoogleAuthProvider();
  // provider.addScope("https://www.googleapis.com/auth/contacts.readonly");

  // let login = false;

  let isLoading = true; // 토큰 값을 받을 때 로그인 화면이 아닌 로딩창을 띄우기 위함.

  // token으로 로그인하기
  // 고급 : 수동으로 로그인 과정 처리
  const auth = getAuth();

  const checkLogin = async () => {
    // console.log("렌더링!");
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);

    // google auth login token 보내고 로그인 정보 받기
    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);

    // 로그인 user 정보 가져오기
    const user = result.user;
    // user store에 user 정보 저장하기
    user$.set(user);
    isLoading = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": Mypage,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

<!--로그인을 하지 않았을 경우, 로그인 화면으로 가기-->
<!--user는 writable 스토어이기 때문에 값을 가져올려면 $를 넣어야한다.-->
{#if isLoading}
  <Loading />
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
