<script>
    let doLoginCheck = checkIfLoggedIn()
  
    function tryAgain() {
      doLoginCheck = checkIfLoggedIn()
    }
  
    function checkIfLoggedIn() {
      return fetch('/api/v1/me')
        .then(res => {
          if (!res.ok) {
            throw new Error('Cannot connect to server!');
          }
          return res.json();
        });
    }
  </script>
  
  {#await doLoginCheck}
    <h1>hello</h1>
  {:then loggedIn}
    {#if loggedIn}
      <p>Profile</p>
      <p class="mb-0 h3">Logout</p>
    {:else}
      <p class="mb-0 h3">Login</p>
      <p class="mb-0 h3">Register</p>
    {/if}
  {:catch error}
    <p>{error.message}</p>
    <button on:click={tryAgain}>Refresh</button>
  {/await}