<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>pdf util</title>
</svelte:head>

{@render children()}
