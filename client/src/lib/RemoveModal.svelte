<script>
	import { createEventDispatcher, onDestroy } from 'svelte';

	const dispatch = createEventDispatcher();
	
    function close(ev = 'defaultClose') {
        dispatch('close', {
			message: ev
		});
    }

	let modal;

	export let event;

	function handle_keydown(e) {
		if (e.key === 'Escape') {
			close();
			return;
		}

		if (e.key === 'Tab') {
			// trap focus
			const nodes = modal.querySelectorAll('*');
			const tabbable = Array.from(nodes).filter(n => n.tabIndex >= 0);

			let index = tabbable.indexOf(document.activeElement);
			if (index === -1 && e.shiftKey) index = 0;

			index += tabbable.length + (e.shiftKey ? -1 : 1);
			index %= tabbable.length;

			tabbable[index].focus();
			e.preventDefault();
		}
	}

	const previously_focused = typeof document !== 'undefined' && document.activeElement;

	if (previously_focused) {
		onDestroy(() => {
			previously_focused.focus();
		});
	}

    function clYes() {
        close('yes');
    }

    function clNo() {
        close('no');
    }
</script>

<svelte:window on:keydown={handle_keydown}/>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="modal-background" on:click={close}></div>

<div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
  <h4>{event == 'edit' ? '속성 변경' : `삭제`}</h4>
  <hr>
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <p on:click={clYes} style='color: red; cursor: pointer;'>예</p>
  <hr>
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <p on:click={clNo} style='cursor: pointer;'>아니오</p>
</div>

<style>
	.modal-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0,0,0,0.3);
	}

	.modal {
		position: absolute;
		left: 50%;
		top: 50%;
		width: 11em;
		max-height: calc(100vh - 4em);
		overflow: auto;
		transform: translate(-50%,-50%);
		padding: 0.3em;
		border-radius: 30px;
		background: white;
        color: black;
	}
</style>
