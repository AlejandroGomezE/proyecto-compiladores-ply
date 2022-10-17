<script>
  export let code;
  export let loading;
  export let compilerHandler;
  import Loading from './Loading.svelte';

  function handleTab(e) {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = e.target.selectionStart;
      const end = e.target.selectionEnd;
      e.target.value = e.target.value.substring(0, start) + '\t' + e.target.value.substring(end);
      e.target.selectionStart = e.target.selectionEnd = start + 1;
    }
  }
</script>

<div class="flex flex-col">
  <label for="input" class="block text-sm font-medium"> Input code </label>
  <div class="relative">
    <textarea class="bg-white h-[70vh] mt-1 rounded-md w-full border-none resize-none" name="input" bind:value={code} on:keydown={handleTab} />
    {#if loading}
      <Loading />
    {/if}
  </div>
  <button
    type="button"
    on:click={compilerHandler}
    disabled={loading}
    class="mt-2 rounded-md border border-transparent bg-green-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50"
  >
    Compilar
  </button>
</div>
