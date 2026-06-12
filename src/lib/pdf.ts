import { PDFDocument, PDFName, PDFRawStream, PDFArray, type PDFDict } from 'pdf-lib';

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

// Per-level JPEG re-encoding settings. LOW is lossless (no image changes).
const COMPRESSION_LEVELS: Record<string, { quality: number; maxDim: number } | null> = {
	LOW: null,
	MEDIUM: { quality: 0.75, maxDim: 2000 },
	HIGH: { quality: 0.55, maxDim: 1500 },
	EXTREME: { quality: 0.35, maxDim: 1000 }
};

function isDctEncoded(dict: PDFDict): boolean {
	const filter = dict.get(PDFName.of('Filter'));
	if (filter === PDFName.of('DCTDecode')) return true;
	return (
		filter instanceof PDFArray &&
		filter.size() === 1 &&
		filter.get(0) === PDFName.of('DCTDecode')
	);
}

async function reencodeJpeg(
	data: Uint8Array,
	quality: number,
	maxDim: number
): Promise<{ data: Uint8Array; width: number; height: number } | null> {
	let bitmap: ImageBitmap;
	try {
		bitmap = await createImageBitmap(new Blob([data as BlobPart], { type: 'image/jpeg' }));
	} catch {
		return null; // browser couldn't decode this JPEG variant
	}
	try {
		const scale = Math.min(1, maxDim / Math.max(bitmap.width, bitmap.height));
		const width = Math.max(1, Math.round(bitmap.width * scale));
		const height = Math.max(1, Math.round(bitmap.height * scale));
		let blob: Blob;
		if (typeof OffscreenCanvas !== 'undefined') {
			const canvas = new OffscreenCanvas(width, height);
			const ctx = canvas.getContext('2d');
			if (!ctx) return null;
			ctx.drawImage(bitmap, 0, 0, width, height);
			blob = await canvas.convertToBlob({ type: 'image/jpeg', quality });
		} else {
			const canvas = document.createElement('canvas');
			canvas.width = width;
			canvas.height = height;
			const ctx = canvas.getContext('2d');
			if (!ctx) return null;
			ctx.drawImage(bitmap, 0, 0, width, height);
			blob = await new Promise<Blob>((resolve, reject) =>
				canvas.toBlob(
					(b) => (b ? resolve(b) : reject(new Error('JPEG encoding failed'))),
					'image/jpeg',
					quality
				)
			);
		}
		return { data: new Uint8Array(await blob.arrayBuffer()), width, height };
	} finally {
		bitmap.close();
	}
}

async function recompressImages(doc: PDFDocument, quality: number, maxDim: number) {
	const context = doc.context;
	for (const [ref, obj] of context.enumerateIndirectObjects()) {
		if (!(obj instanceof PDFRawStream)) continue;
		const dict = obj.dict;
		if (dict.get(PDFName.of('Subtype')) !== PDFName.of('Image')) continue;
		if (dict.get(PDFName.of('ImageMask'))) continue;
		if (!isDctEncoded(dict)) continue;
		try {
			const reencoded = await reencodeJpeg(obj.contents, quality, maxDim);
			// only swap in the re-encoded image if it's actually smaller
			if (!reencoded || reencoded.data.length >= obj.contents.length) continue;
			const newDict = dict.clone(context);
			newDict.set(PDFName.of('Width'), context.obj(reencoded.width));
			newDict.set(PDFName.of('Height'), context.obj(reencoded.height));
			newDict.set(PDFName.of('Filter'), PDFName.of('DCTDecode'));
			// canvas always outputs 8-bit RGB JPEGs regardless of the source colorspace
			newDict.set(PDFName.of('ColorSpace'), PDFName.of('DeviceRGB'));
			newDict.set(PDFName.of('BitsPerComponent'), context.obj(8));
			newDict.set(PDFName.of('Length'), context.obj(reencoded.data.length));
			newDict.delete(PDFName.of('DecodeParms'));
			newDict.delete(PDFName.of('Decode'));
			context.assign(ref, PDFRawStream.of(newDict, reencoded.data));
		} catch {
			// leave this image untouched rather than failing the whole document
		}
	}
}

export async function compressPdf(file: File, level: string): Promise<Uint8Array> {
	const bytes = new Uint8Array(await file.arrayBuffer());
	// updateMetadata: false stops pdf-lib from stamping its own Producer/ModDate
	const doc = await PDFDocument.load(bytes, { updateMetadata: false });

	const imageOpts = COMPRESSION_LEVELS[level] ?? null;
	if (imageOpts) {
		await recompressImages(doc, imageOpts.quality, imageOpts.maxDim);
	}

	// Strip metadata, including the XMP metadata stream
	doc.setTitle('');
	doc.setAuthor('');
	doc.setSubject('');
	doc.setKeywords([]);
	doc.setProducer('');
	doc.setCreator('');
	doc.catalog.delete(PDFName.of('Metadata'));

	const out = await doc.save({ useObjectStreams: true });

	// Never hand back something bigger than the input
	return out.length < bytes.length ? out : bytes;
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
