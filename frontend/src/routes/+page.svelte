<script>
  import Input from './Input.svelte';
  import Output from './Output.svelte';

  let code = '';
  let loading = false;
  let error = '';
  let compiled_data = null;

  async function compilerHandler(e) {
    loading = true;
    const res = await fetch('http://localhost:5000/api/code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
      }),
    });
    const data = await res.json();
    if (res.status === 200) {
      compiled_data = data;
      error = '';
    } else {
      compiled_data = null;
      error = data.message;
    }
    loading = false;
  }
</script>

<svelte:head>
  <title>Compilador</title>
</svelte:head>

<section class="grid grid-cols-2 gap-8">
  <Input bind:code {loading} {compilerHandler} />
  <Output {loading} {error} {compiled_data} />
</section>
