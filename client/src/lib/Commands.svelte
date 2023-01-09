<script>
  import CodeEditor from 'svelte-code-editor';
  import UtilModal from './UtilModal.svelte';
  import Modal from './Modal.svelte';
  import RemoveModal from './RemoveModal.svelte';

  import { createEventDispatcher } from 'svelte';

  export let title, description, response;

  const dispatch = createEventDispatcher();

  function changed() {
    dispatch('changed');
  }

  let style = '';
  let now = 0;
  let showAll = false;
  let boxHeight = '50px';

  $: boxStyle = `\
display: flex;
flex: 1 0 15%;
align-items: flex-start;
flex-direction: column;
width: 300px;
height: ${boxHeight};
border-radius: 50px;
padding: 25px 0 0 25px;
box-shadow: -2px -2px 4px rgba(255, 255, 255, 0.05), 1px 2px 4px rgba(0, 0, 0, 0.25);
margin-right: 20px;
transition: all ease 0.85s;
margin-bottom: 15px;`;

  let showUtilModal = false;

  function spin() {
    style = `transform: rotate(${now == 0 ? 90 : 0}deg);`;
    now == 0 ? now = 1 : now = 0;
    showAll = !showAll;
    boxHeight == '170px' ? boxHeight = '50px' : boxHeight = '170px';
  }

  function testFunc(event) {
    event.preventDefault();
    
    showUtilModal = true;
    
    return false;
  }

  let nowEvent = 'remove';

  let showEditModal = false;
  let showRemoveModal = false;
  let advanced = false;
  let code = `\
description = '${description}'
response = '${response}'

async def ${title}(ctx):
    await ctx.respond(response)`;

  let commandName = title, des = description, res = response;

  async function submit() {
    await fetch("/command", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          commandName: commandName,
          description: des,
          response: res,
      }),
    });

    showEditModal = false;
    showRemoveModal = true;
    nowEvent = 'edit';
  }

  async function remove() {
    await fetch(`/command/${title}`, {
      method: "REMOVE",
      headers: {
          "Content-Type": "application/json",
      },
    });

    changed();
  }

  function handleCloseEvent(event) {
    let ev = event.detail.message;

    if (ev != 'defaultClose') {
      if (ev == 'edit') {
        showEditModal = true;
      } else {
        showRemoveModal = true;
        nowEvent = 'remove';
      }
    }

    showUtilModal = false;
  }

  function handleRemoveModal(event) {
    let ev = event.detail.message;

    if (ev != 'defaultClose') {
      if (ev == 'yes') {
        remove();
      }
    }
    
    showRemoveModal = false;
  }
</script>

{#if showEditModal}
  <Modal on:close="{() => showEditModal = false}">
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
      <input type="text" class="txt-input" id="description" placeholder="커맨드의 설명을 입력해주세요." bind:value={des}>
    </div>

    <div class="dust-class">
      <label for="response"><span>* </span>응답</label>
      <input type="text" class="txt-input" id="response" placeholder="커맨드의 응답을 입력해주세요." bind:value={res}>
    </div>

    <button class='submit' on:click={submit}>제출</button>
    {/if}
  </Modal>
{/if}

{#if showRemoveModal}
  <RemoveModal event={nowEvent} on:close="{handleRemoveModal}">
    <p style='color: red; cursor:pointer'>예</p>
    <p style='cursor:pointer'>아니오</p>
  </RemoveModal>
{/if}

{#if showUtilModal}
  <UtilModal on:close="{handleCloseEvent}" />
{/if}

<div on:contextmenu={testFunc} style={boxStyle}>
  <div class="start">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <svg id='arrow' on:click={spin} style={style} viewBox="0 0 8 11" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M1.711 0.657C1.57 0.549 1.411 0.5 1.255 0.5C0.866 0.5 0.5 0.806001 0.5 1.249L0.5 9.75C0.5 10.195 0.867 10.5 1.255 10.5C1.412 10.5 1.571 10.45 1.712 10.341C3.266 9.138 5.911 7.089 7.21 6.083C7.394 5.941 7.5 5.723 7.5 5.491C7.5 5.261 7.393 5.042 7.209 4.9C5.91 3.898 3.264 1.856 1.711 0.657V0.657Z" />
    </svg>

    <span class='title'>
      /{title}
    </span>
  </div>
  {#if showAll}
    <span class='description'>
      description: {description}
      <br>
      response: {response}
    </span>
    <span class='isAdvanced'>
      isAdvanced: false
    </span>
  {/if}
</div>

<style>
  svg {
    margin-top: 2px;
    margin-right: 8px;
    float: left;
    fill: white;
    width: 12px;
    transition: all ease 0.85s;
  }

  @font-face {
    font-family: 'LINESeedKR-Bd';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_11-01@1.0/LINESeedKR-Bd.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
  }

  @font-face {
    font-family: 'LINESeedKR-Rg';
    src: url('https://cdn.jsdelivr.net/gh/wizfile/font/LINESeedKR-Rg.eot');
    src:url('https://cdn.jsdelivr.net/gh/wizfile/font/LINESeedKR-Rg.woff') format('woff');
    font-style: normal;
  }

  .title {
    font-family: 'LINESeedKR-Bd';
    font-size: 1.3em;
    font-weight: bold;
  }

  .description {
    float: left;
    margin-top: 5px;

    text-align: left;
    font-family: 'LINESeedKR-Rg';
    font-weight: 400;
  }

  .isAdvanced {
    float: left;

    text-align: left;
    font-family: 'LINESeedKR-Rg';
    font-weight: 400;
  }

  .start {
    display: flex;
    align-items: flex-start;
    flex-direction: row;
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
