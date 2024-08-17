<script>
  import Nav from "../components/Nav.svelte";
  import { user$ } from "../store";

  // user storage 정보를 지우고, local storage에 token이 있는지 확인해서 가져오는데 이것도 비워줘야함.
  const logout = () => {
    user$.set(null);
    localStorage.removeItem("token");
  };
</script>

<div>나의 당근</div>
<button on:click={logout}>로그아웃</button>
<Nav location="my" />

<style>
  button {
    cursor: pointer;
    border: 1px solid rgba(0, 0, 0, 0.3);
  }
</style>
