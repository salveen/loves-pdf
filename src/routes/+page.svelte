<script lang="ts">
	import MergeTab from '$lib/components/MergeTab.svelte';
	import SplitTab from '$lib/components/SplitTab.svelte';
	import CompressTab from '$lib/components/CompressTab.svelte';

	let activeTab = $state<'merge' | 'split' | 'compress'>('merge');
</script>

<div class="main-container">
	<div class="main-header">
		<h1>Priva PDF</h1>
		<p>Private, local PDF tools — your files never leave your browser</p>
	</div>

	<div class="tab-bar">
		<button class="tab-btn" class:active={activeTab === 'merge'} onclick={() => (activeTab = 'merge')}>
			Merge PDFs
		</button>
		<button class="tab-btn" class:active={activeTab === 'split'} onclick={() => (activeTab = 'split')}>
			Split PDF
		</button>
		<button
			class="tab-btn"
			class:active={activeTab === 'compress'}
			onclick={() => (activeTab = 'compress')}
		>
			Compress PDF
		</button>
	</div>

	<div>
		{#if activeTab === 'merge'}
			<MergeTab />
		{:else if activeTab === 'split'}
			<SplitTab />
		{:else}
			<CompressTab />
		{/if}
	</div>

	<div class="footer">
		<div class="privacy-badge">🔒 100% Private — All processing happens in your browser</div>
		<p style="margin-top: 1rem; font-size: 0.8rem;">Your files never leave your machine</p>
	</div>
</div>
