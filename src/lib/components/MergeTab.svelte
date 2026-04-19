<script lang="ts">
	import { mergePdfs, downloadBlob, formatSize } from '$lib/pdf';

	let files = $state<File[]>([]);
	let outputName = $state('merged.pdf');
	let processing = $state(false);
	let result = $state<{ success: boolean; message: string } | null>(null);
	let resultData = $state<Uint8Array | null>(null);
	let dragover = $state(false);

	function handleFiles(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files) {
			files = [...files, ...Array.from(input.files)];
			input.value = '';
		}
		result = null;
		resultData = null;
	}

	function handleDrop(event: DragEvent) {
		event.preventDefault();
		dragover = false;
		if (event.dataTransfer?.files) {
			const pdfs = Array.from(event.dataTransfer.files).filter((f) =>
				f.name.toLowerCase().endsWith('.pdf')
			);
			files = [...files, ...pdfs];
		}
		result = null;
		resultData = null;
	}

	function removeFile(index: number) {
		files = files.filter((_, i) => i !== index);
		result = null;
		resultData = null;
	}

	function moveUp(index: number) {
		if (index === 0) return;
		const arr = [...files];
		[arr[index - 1], arr[index]] = [arr[index], arr[index - 1]];
		files = arr;
	}

	function moveDown(index: number) {
		if (index === files.length - 1) return;
		const arr = [...files];
		[arr[index], arr[index + 1]] = [arr[index + 1], arr[index]];
		files = arr;
	}

	async function doMerge() {
		if (files.length < 2) {
			result = { success: false, message: 'Please upload at least 2 PDF files to merge.' };
			return;
		}
		processing = true;
		result = null;
		resultData = null;
		try {
			const name = outputName.endsWith('.pdf') ? outputName : outputName + '.pdf';
			const data = await mergePdfs(files);
			resultData = data;
			result = { success: true, message: `✓ Successfully merged ${files.length} PDFs!` };
		} catch (e: unknown) {
			result = { success: false, message: `Error merging PDFs: ${e instanceof Error ? e.message : e}` };
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

<h3 class="section-header">Merge Multiple PDFs</h3>
<p class="section-desc">Combine multiple PDF files into a single document. Use arrows to reorder files.</p>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	class="upload-area"
	class:dragover
	ondragover={(e) => { e.preventDefault(); dragover = true; }}
	ondragleave={() => (dragover = false)}
	ondrop={handleDrop}
>
	<div class="upload-icon">📄</div>
	<div class="upload-text">Drop PDF file(s) here or <span>click to browse</span></div>
	<input type="file" accept=".pdf" multiple onchange={handleFiles} />
</div>

{#if files.length > 0}
	<div class="file-list-container">
		<div class="file-list-header">
			<strong>{files.length} file(s) ready</strong>
			<span class="reorder-hint"> — use arrows to reorder</span>
		</div>
		{#each files as file, i (file.name + i)}
			<div class="file-item">
				<span class="file-number">{i + 1}</span>
				<span class="file-name">{file.name}</span>
				<span class="file-size">{formatSize(file.size)}</span>
				<div class="file-actions">
					<button class="move-btn" disabled={i === 0} onclick={() => moveUp(i)} title="Move up">↑</button>
					<button class="move-btn" disabled={i === files.length - 1} onclick={() => moveDown(i)} title="Move down">↓</button>
					<button class="remove-btn" onclick={() => removeFile(i)} title="Remove">✕</button>
				</div>
			</div>
		{/each}
	</div>

	<div class="form-group">
		<label class="form-label" for="merge-output">Output filename</label>
		<input id="merge-output" class="form-input" type="text" bind:value={outputName} />
	</div>

	<button class="btn-primary" onclick={doMerge} disabled={processing}>
		{#if processing}<span class="spinner"></span>{/if}
		Merge PDFs
	</button>
{/if}

{#if result}
	<div style="margin-top: 1rem;">
		{#if result.success}
			<div class="alert-success">{result.message}</div>
			<button class="btn-download" onclick={download}>Download Merged PDF</button>
		{:else}
			<div class="alert-error">{result.message}</div>
		{/if}
	</div>
{/if}
