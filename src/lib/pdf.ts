import { PDFDocument } from 'pdf-lib';

export async function mergePdfs(files: File[]): Promise<Uint8Array> {
	const merged = await PDFDocument.create();
	for (const file of files) {
		const bytes = new Uint8Array(await file.arrayBuffer());
		const doc = await PDFDocument.load(bytes);
		const pages = await merged.copyPages(doc, doc.getPageIndices());
		for (const page of pages) {
			merged.addPage(page);
		}
	}
	return merged.save();
}

export async function getPageCount(file: File): Promise<number> {
	const bytes = new Uint8Array(await file.arrayBuffer());
	const doc = await PDFDocument.load(bytes);
	return doc.getPageCount();
}

export async function splitByRange(
	file: File,
	start: number,
	end: number
): Promise<Uint8Array> {
	const bytes = new Uint8Array(await file.arrayBuffer());
	const src = await PDFDocument.load(bytes);
	const out = await PDFDocument.create();
	// pages are 0-indexed in pdf-lib, user provides 1-indexed
	const indices = [];
	for (let i = start - 1; i < end && i < src.getPageCount(); i++) {
		indices.push(i);
	}
	const pages = await out.copyPages(src, indices);
	for (const p of pages) out.addPage(p);
	return out.save();
}

export async function extractPages(
	file: File,
	pageNumbers: number[]
): Promise<Uint8Array> {
	const bytes = new Uint8Array(await file.arrayBuffer());
	const src = await PDFDocument.load(bytes);
	const out = await PDFDocument.create();
	const indices = pageNumbers.map((p) => p - 1).filter((i) => i >= 0 && i < src.getPageCount());
	const pages = await out.copyPages(src, indices);
	for (const p of pages) out.addPage(p);
	return out.save();
}

export async function splitEveryN(
	file: File,
	n: number
): Promise<{ name: string; data: Uint8Array }[]> {
	const bytes = new Uint8Array(await file.arrayBuffer());
	const src = await PDFDocument.load(bytes);
	const total = src.getPageCount();
	const results: { name: string; data: Uint8Array }[] = [];
	const baseName = file.name.replace(/\.pdf$/i, '');

	for (let start = 0; start < total; start += n) {
		const end = Math.min(start + n, total);
		const out = await PDFDocument.create();
		const indices = [];
		for (let i = start; i < end; i++) indices.push(i);
		const pages = await out.copyPages(src, indices);
		for (const p of pages) out.addPage(p);
		const part = Math.floor(start / n) + 1;
		results.push({
			name: `${baseName}_part${part}.pdf`,
			data: await out.save()
		});
	}
	return results;
}

export async function compressPdf(
	file: File,
	_level: string
): Promise<Uint8Array> {
	// pdf-lib doesn't do image recompression, but we can strip metadata,
	// rebuild the structure, and use object-stream compression.
	// For real Ghostscript-level compression, a WASM build would be needed.
	// This still reduces size for many PDFs by cleaning up structure.
	const bytes = new Uint8Array(await file.arrayBuffer());
	const doc = await PDFDocument.load(bytes);

	// Strip metadata
	doc.setTitle('');
	doc.setAuthor('');
	doc.setSubject('');
	doc.setKeywords([]);
	doc.setProducer('');
	doc.setCreator('');

	return doc.save();
}

export function parsePageInput(input: string, maxPage: number): number[] {
	const pages: number[] = [];
	const parts = input.replace(/\s/g, '').split(',');
	for (const part of parts) {
		if (!part) continue;
		if (part.includes('-')) {
			const [a, b] = part.split('-').map(Number);
			const start = Math.min(a, b);
			const end = Math.max(a, b);
			for (let i = start; i <= end; i++) pages.push(i);
		} else {
			pages.push(Number(part));
		}
	}
	const unique = [...new Set(pages)].sort((a, b) => a - b);
	const invalid = unique.filter((p) => p < 1 || p > maxPage);
	if (invalid.length) throw new Error(`Invalid pages: ${invalid.join(', ')}. Document has ${maxPage} pages.`);
	return unique;
}

export function downloadBlob(data: Uint8Array, filename: string) {
	const blob = new Blob([data as BlobPart], { type: 'application/pdf' });
	const url = URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = filename;
	a.click();
	URL.revokeObjectURL(url);
}

export function downloadZip(
	_files: { name: string; data: Uint8Array }[],
	_zipName: string
) {
	// Minimal ZIP implementation — we avoid a dep for this.
	// Each file as a separate download instead.
	for (const f of _files) {
		downloadBlob(f.data, f.name);
	}
}

export function formatSize(bytes: number): string {
	if (bytes < 1024) return `${bytes} B`;
	return `${(bytes / 1024).toFixed(1)} KB`;
}
