<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>salveen-loves-pdf</title>
</svelte:head>

{@render children()}
