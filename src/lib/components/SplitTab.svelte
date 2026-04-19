<script lang="ts">
	import {
		getPageCount,
		splitByRange,
		extractPages,
		splitEveryN,
		parsePageInput,
		downloadBlob,
		formatSize
	} from '$lib/pdf';

	let file = $state<File | null>(null);
	let pageCount = $state(0);
	let mode = $state<'range' | 'pages' | 'every_n'>('range');
	let startPage = $state(1);
	let endPage = $state(1);
	let pagesInput = $state('');
	let everyN = $state(1);
	let processing = $state(false);
	let result = $state<{ success: boolean; message: string } | null>(null);
	let resultFiles = $state<{ name: string; data: Uint8Array }[]>([]);
	let dragover = $state(false);

	async function handleFile(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files?.[0]) {
			file = input.files[0];
			pageCount = await getPageCount(file);
			startPage = 1;
			endPage = pageCount;
			everyN = 1;
			result = null;
			resultFiles = [];
			input.value = '';
		}
	}

	async function handleDrop(event: DragEvent) {
		event.preventDefault();
		dragover = false;
		const f = event.dataTransfer?.files?.[0];
		if (f && f.name.toLowerCase().endsWith('.pdf')) {
			file = f;
			pageCount = await getPageCount(file);
			startPage = 1;
			endPage = pageCount;
			everyN = 1;
			result = null;
			resultFiles = [];
		}
	}

	async function doSplit() {
		if (!file) return;
		processing = true;
		result = null;
		resultFiles = [];
		try {
			if (mode === 'range') {
				const data = await splitByRange(file, startPage, endPage);
				const name = `${file.name.replace(/\.pdf$/i, '')}_pages${startPage}-${endPage}.pdf`;
				resultFiles = [{ name, data }];
				result = { success: true, message: '✓ PDF split successfully!' };
			} else if (mode === 'pages') {
				const pages = parsePageInput(pagesInput, pageCount);
				const data = await extractPages(file, pages);
				const name = `${file.name.replace(/\.pdf$/i, '')}_extracted.pdf`;
				resultFiles = [{ name, data }];
				result = { success: true, message: '✓ PDF split successfully!' };
			} else {
				const parts = await splitEveryN(file, everyN);
				resultFiles = parts;
				result = { success: true, message: `✓ Created ${parts.length} files!` };
			}
		} catch (e: unknown) {
			result = {
				success: false,
				message: `Error splitting PDF: ${e instanceof Error ? e.message : e}`
			};
		} finally {
			processing = false;
		}
	}

	function downloadFile(f: { name: string; data: Uint8Array }) {
		downloadBlob(f.data, f.name);
	}

	function downloadAll() {
		for (const f of resultFiles) {
			downloadBlob(f.data, f.name);
		}
	}
</script>

<h3 class="section-header">Split PDF</h3>
<p class="section-desc">
	Split a PDF into multiple files by page ranges or extract specific pages.
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
		<span class="muted"> — </span>
		<strong>{pageCount} pages</strong>
		<span class="subtle"> ({formatSize(file.size)})</span>
		<button
			class="remove-btn"
			style="float: right;"
			onclick={() => {
				file = null;
				pageCount = 0;
				result = null;
				resultFiles = [];
			}}
			title="Remove"
		>
			✕
		</button>
	</div>

	<div class="form-group">
		<label class="form-label" for="split-mode">Split Mode</label>
		<select id="split-mode" class="form-select" bind:value={mode}>
			<option value="range">Extract page range</option>
			<option value="pages">Extract specific pages</option>
			<option value="every_n">Split every N pages</option>
		</select>
	</div>

	{#if mode === 'range'}
		<div class="form-row">
			<div class="form-group">
				<label class="form-label" for="start-page">Start Page</label>
				<input
					id="start-page"
					class="form-input"
					type="number"
					min="1"
					max={pageCount}
					bind:value={startPage}
				/>
			</div>
			<div class="form-group">
				<label class="form-label" for="end-page">End Page</label>
				<input
					id="end-page"
					class="form-input"
					type="number"
					min="1"
					max={pageCount}
					bind:value={endPage}
				/>
			</div>
		</div>
	{:else if mode === 'pages'}
		<div class="form-group">
			<label class="form-label" for="pages-input">Pages to Extract</label>
			<input
				id="pages-input"
				class="form-input"
				type="text"
				placeholder="e.g., 1, 3, 5-7 (max: {pageCount})"
				bind:value={pagesInput}
			/>
			<div class="form-hint">
				Enter page numbers separated by commas. Use hyphens for ranges (e.g., 1-3).
			</div>
		</div>
	{:else}
		<div class="form-group">
			<label class="form-label" for="every-n">Pages per File</label>
			<input
				id="every-n"
				class="form-input"
				type="number"
				min="1"
				max={pageCount}
				bind:value={everyN}
			/>
			<div class="form-hint">
				The PDF will be split into multiple files, each containing this many pages.
			</div>
		</div>
	{/if}

	<button class="btn-primary" onclick={doSplit} disabled={processing} style="margin-top: 0.5rem;">
		{#if processing}<span class="spinner"></span>{/if}
		Split PDF
	</button>
{/if}

{#if result}
	<div style="margin-top: 1rem;">
		{#if result.success}
			<div class="alert-success">{result.message}</div>
			{#if resultFiles.length === 1}
				<button class="btn-download" onclick={() => downloadFile(resultFiles[0])}>
					Download {resultFiles[0].name}
				</button>
			{:else}
				<ul class="result-list">
					{#each resultFiles as f}
						<li>
							{f.name}
							<button
								class="btn-download"
								style="padding: 0.3rem 0.8rem; font-size: 0.85rem; margin-left: 0.5rem; margin-top: 0;"
								onclick={() => downloadFile(f)}
							>
								Download
							</button>
						</li>
					{/each}
				</ul>
				<button class="btn-download" onclick={downloadAll}>Download All</button>
			{/if}
		{:else}
			<div class="alert-error">{result.message}</div>
		{/if}
	</div>
{/if}
