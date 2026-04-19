<script lang="ts">
	import { compressPdf, downloadBlob, formatSize } from '$lib/pdf';

	let file = $state<File | null>(null);
	let level = $state('MEDIUM');
	let outputName = $state('compressed.pdf');
	let processing = $state(false);
	let result = $state<{ success: boolean; message: string } | null>(null);
	let resultData = $state<Uint8Array | null>(null);
	let metrics = $state<{ original: number; compressed: number; reduction: number } | null>(null);
	let dragover = $state(false);

	const descriptions: Record<string, string> = {
		LOW: 'Minimal compression — structure cleanup only',
		MEDIUM: 'Balanced — metadata stripped, structure optimized',
		HIGH: 'Aggressive — maximum structural compression',
		EXTREME: 'Maximum — all non-essential data removed'
	};

	async function handleFile(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files?.[0]) {
			file = input.files[0];
			outputName = `${file.name.replace(/\.pdf$/i, '')}_compressed.pdf`;
			result = null;
			resultData = null;
			metrics = null;
			input.value = '';
		}
	}

	async function handleDrop(event: DragEvent) {
		event.preventDefault();
		dragover = false;
		const f = event.dataTransfer?.files?.[0];
		if (f && f.name.toLowerCase().endsWith('.pdf')) {
			file = f;
			outputName = `${file.name.replace(/\.pdf$/i, '')}_compressed.pdf`;
			result = null;
			resultData = null;
			metrics = null;
		}
	}

	async function doCompress() {
		if (!file) return;
		processing = true;
		result = null;
		resultData = null;
		metrics = null;
		try {
			const data = await compressPdf(file, level);
			resultData = data;
			const originalKb = file.size / 1024;
			const compressedKb = data.length / 1024;
			const reduction = ((originalKb - compressedKb) / originalKb) * 100;
			metrics = { original: originalKb, compressed: compressedKb, reduction };
			result = { success: true, message: '✓ Compression complete!' };
		} catch (e: unknown) {
			result = {
				success: false,
				message: `Error compressing PDF: ${e instanceof Error ? e.message : e}`
			};
		} finally {
			processing = false;
		}
	}

	function download() {
		if (resultData) {
			const name = outputName.endsWith('.pdf') ? outputName : outputName + '.pdf';
			downloadBlob(resultData, name);
		}
	}
</script>

<h3 class="section-header">Compress a PDF</h3>
<p class="section-desc">
	Reduce PDF file size by stripping metadata and optimizing structure.
</p>

{#if !file}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		class="upload-area"
		class:dragover
		ondragover={(e) => { e.preventDefault(); dragover = true; }}
		ondragleave={() => (dragover = false)}
		ondrop={handleDrop}
	>
		<div class="upload-icon">📄</div>
		<div class="upload-text">Drop a PDF file here or <span>click to browse</span></div>
		<input type="file" accept=".pdf" onchange={handleFile} />
	</div>
{:else}
	<div class="file-info-box">
		<strong>{file.name}</strong>
		<span class="muted"> — Original size: </span>
		<strong>{formatSize(file.size)}</strong>
		<button
			class="remove-btn"
			style="float: right;"
			onclick={() => {
				file = null;
				result = null;
				resultData = null;
				metrics = null;
			}}
			title="Remove"
		>
			✕
		</button>
	</div>

	<div class="form-group">
		<label class="form-label" for="compress-level">Compression Level</label>
		<select id="compress-level" class="form-select" bind:value={level}>
			<option value="LOW">Low</option>
			<option value="MEDIUM">Medium</option>
			<option value="HIGH">High</option>
			<option value="EXTREME">Extreme</option>
		</select>
		<div class="form-hint">{descriptions[level]}</div>
	</div>

	<div class="form-group">
		<label class="form-label" for="compress-output">Output filename</label>
		<input id="compress-output" class="form-input" type="text" bind:value={outputName} />
	</div>

	<button class="btn-primary" onclick={doCompress} disabled={processing}>
		{#if processing}<span class="spinner"></span>{/if}
		Compress PDF
	</button>
{/if}

{#if result}
	<div style="margin-top: 1rem;">
		{#if result.success}
			<div class="alert-success">{result.message}</div>
			{#if metrics}
				<div class="metrics-row">
					<div class="metric-card">
						<div class="metric-label">Original Size</div>
						<div class="metric-value">{metrics.original.toFixed(1)} KB</div>
					</div>
					<div class="metric-card">
						<div class="metric-label">Compressed Size</div>
						<div class="metric-value">{metrics.compressed.toFixed(1)} KB</div>
					</div>
					<div class="metric-card">
						<div class="metric-label">Reduction</div>
						<div class="metric-value">{metrics.reduction.toFixed(1)}%</div>
					</div>
				</div>
			{/if}
			<button class="btn-download" onclick={download}>Download Compressed PDF</button>
		{:else}
			<div class="alert-error">{result.message}</div>
		{/if}
	</div>
{/if}
