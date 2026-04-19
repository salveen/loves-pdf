<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>Priva PDF</title>
</svelte:head>

{@render children()}
