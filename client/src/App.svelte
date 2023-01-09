<script>
  import CodeEditor from 'svelte-code-editor';
  import Commands from './lib/Commands.svelte';
  
  import Modal from './lib/Modal.svelte';

	let showModal = false;
  let showTokenModal = false;
  let commandName = '';
  let description = '';
  let response = '';
  let token = '';

  function caseModal() {
    switch (showModal) {
      case true:
        showModal = false;
      case false:
        showModal = true;
    }
  }

  function caseTokenModal() {
    switch (showTokenModal) {
      case true:
        showTokenModal = false;
      case false:
        showTokenModal = true;
    }
  }

  async function submit() {
    await fetch("/command", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          commandName: commandName,
          description: description,
          response: response,
      }),
    });

    showModal = false;

    commandName = '', description = '', response = '';

    reload();
  }

  async function tokenSubmit() {
    await fetch("/token", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          TOKEN: token
      }),
    });

    showModal = false;

    reload();
  }

  async function getCommands() {
    const res = await fetch('/command');
    const data = JSON.stringify(await res.json());

    return data;
  }

  let commands = getCommands();

  function reload() {
    commands = getCommands();
  }

  let code = `\
description = 'hello, world!'
response = 'pong!'

async def ping(ctx):
    await ctx.respond(response)`;

  let advanced = false;
</script>

<main>
  <h1>Dashboard</h1>

  {#if showModal}
    <Modal on:close="{() => showModal = false}">
      <h2 slot="header">
        AddCommands
      </h2>

      <label for="advanced">고급 기능</label>
      <input type="checkbox" id="advanced" bind:checked={advanced}>

      {#if advanced}
        <p>
        코드를 입력해주세요. (async - await, 인자: ctx, decorator 불필요)
        <br>
        함수 이름이 커맨드 이름이 됩니다. (필요 변수: description, response)
        </p>
        <CodeEditor lang='python' bind:code tab='    ' autofocus={true} />
      {:else}
      <div class="dust-class">
        <label for="commandName"><span>* </span>커맨드 이름 (띄어쓰기 사용 불가)</label>
        <input type="text" class="txt-input" id="commandName" placeholder="커맨드 이름을 입력해주세요." bind:value={commandName}>
      </div>

      <div class="dust-class">
        <label for="description"><span>* </span>설명</label>
        <input type="text" class="txt-input" id="description" placeholder="커맨드의 설명을 입력해주세요." bind:value={description}>
      </div>

      <div class="dust-class">  
        <label for="response"><span>* </span>응답</label>
        <input type="text" class="txt-input" id="response" placeholder="커맨드의 응답을 입력해주세요." bind:value={response}>
      </div>

      <button class='submit' on:click={submit}>제출</button>
      {/if}
    </Modal>
  {/if}

  {#if showTokenModal}
    <Modal on:close="{() => showTokenModal = false}">
    <h2 slot="header">
      ChangeToken
    </h2>
    
    <div class="dust-class">
      <label for="token"><span>* </span>토큰</label>
      <input type="text" class="txt-input" id="token" placeholder="토큰을 입력해주세요." bind:value={token}>
    </div>

    <button class='submit' on:click={tokenSubmit}>제출</button>
    </Modal>
  {/if}

  <div id='commands'>
    {#await commands}
      <p>waiting</p>
    {:then data}
      {#each JSON.parse(data) as command}
        <Commands on:changed={reload} title={command.commandName} description={command.description} response={command.response} />
      {/each}
    {/await}
  </div>

  <br>
  <button on:click={caseModal}>AddCommand</button>
  <button on:click={caseTokenModal}>changeToken</button>
</main>

<style>
  #commands {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  .submit {
    margin-left: 55%;
  }

  input[type="text"] {
    font-family: 'Noto Sans KR','Noto Sans Korean', "Nanum Gothic", sans-serif !important;
    appearance: none;
    border-radius: 0;
    border: 0;
    outline: none;
    font-size: 10px;
  }

  input[type="text"]::placeholder {
    color: #d9d9d9
  }

  .dust-class {
    width: 50%; 
    box-sizing: border-box;
    margin: 20px auto;
    position: relative;
  }

  .dust-class label {
    display: inline-block;
    position: absolute;
    top: -12px;
    left: 8px;
    font-size: 14px;
    color: #282c34;
    font-weight: bold;
  }

  .dust-class label span {
    color: #da4841;
    vertical-align: -1px;
  }

  .dust-class input[type="text"] {
    width: 100%;
    border: 1px solid #dddddd !important;
    font-size: 1rem;
    line-height: 1.45;
    letter-spacing: -0.04rem;
    border-radius: 8px;
    padding: 16px;
    margin-top: 12px;
  }
</style>
