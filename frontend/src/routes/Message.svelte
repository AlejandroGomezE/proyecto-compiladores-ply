<script>
  import { fade } from 'svelte/transition';
  export let message;
</script>

<p class="text-sm text-gray-500 px-2 py-1" in:fade={{ y: 200, duration: 1000 }}>>> {message}</p>
