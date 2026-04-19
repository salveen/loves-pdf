"""Callback definitions for the Priva PDF application."""

import base64
import tempfile
import zipfile
from pathlib import Path

from dash import callback, dcc, html, Input, Output, State, ALL, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from src.pdf_tool import PdfTool
from .config import COMPRESSION_DESCRIPTIONS, get_compression_level
from .components import (
    create_upload_component,
    create_file_list,
    create_compression_selector,
    create_output_input,
    create_metrics,
    create_success_alert,
    create_error_alert,
    create_download_button,
)

# Initialize the PDF tool
pdf_tool = PdfTool()


# =============================================================================
# Tab Content Rendering
# =============================================================================

@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """Render the content for each tab."""
    if active_tab == "tab-merge":
        return _create_merge_tab()
    elif active_tab == "tab-split":
        return _create_split_tab()
    elif active_tab == "tab-compress":
        return _create_compress_tab()
    return html.Div()


def _create_merge_tab() -> html.Div:
    return html.Div([
        html.H3("Merge Multiple PDFs", className="section-header"),
        html.P("Combine multiple PDF files into a single document. Use arrows to reorder files.", className="section-desc"),
        create_upload_component("merge-upload", multiple=True),
        html.Div(id="merge-file-list"),
        html.Div(id="merge-options", style={"display": "none"}, children=[
            create_output_input("merge-output-name", "merged.pdf"),
            html.Button("Merge PDFs", id="merge-btn", className="btn-primary-custom"),
        ]),
        dcc.Loading(html.Div(id="merge-result"), type="circle", color="#f59e0b"),
    ])


def _create_split_tab() -> html.Div:
    return html.Div([
        html.H3("Split PDF", className="section-header"),
        html.P("Split a PDF into multiple files by page ranges or extract specific pages.", className="section-desc"),
        create_upload_component("split-upload", multiple=False),
        html.Div(id="split-file-info"),
        html.Div(id="split-options", style={"display": "none"}, children=[
            html.Div([
                html.Label("Split Mode", className="form-label"),
                dcc.Dropdown(
                    id="split-mode",
                    options=[
                        {"label": "Extract page range", "value": "range"},
                        {"label": "Extract specific pages", "value": "pages"},
                        {"label": "Split every N pages", "value": "every_n"},
                    ],
                    value="range",
                    clearable=False,
                    searchable=False,
                    className="retro-dropdown",
                ),
            ], style={"marginBottom": "1rem"}),
            html.Div(id="split-mode-options"),
            html.Button("Split PDF", id="split-btn", className="btn-primary-custom", style={"marginTop": "1rem"}),
        ]),
        dcc.Loading(html.Div(id="split-result"), type="circle", color="#f59e0b"),
    ])


def _create_compress_tab() -> html.Div:
    return html.Div([
        html.H3("Compress a PDF", className="section-header"),
        html.P("Reduce PDF file size by compressing embedded images.", className="section-desc"),
        create_upload_component("compress-upload", multiple=False),
        html.Div(id="compress-file-info"),
        html.Div(id="compress-options", style={"display": "none"}, children=[
            create_compression_selector("compress-level"),
            create_output_input("compress-output-name", "compressed.pdf"),
            html.Button("Compress PDF", id="compress-btn", className="btn-primary-custom"),
        ]),
        dcc.Loading(html.Div(id="compress-result"), type="circle", color="#f59e0b"),
    ])


# =============================================================================
# Merge Callbacks
# =============================================================================

@callback(
    Output("merge-files-store", "data"),
    Input("merge-upload", "contents"),
    State("merge-upload", "filename"),
    State("merge-files-store", "data"),
    prevent_initial_call=True,
)
def handle_merge_upload(contents, filenames, existing_files):
    """Handle file uploads for merge."""
    if contents is None:
        raise PreventUpdate
    
    if not isinstance(contents, list):
        contents = [contents]
        filenames = [filenames]
    
    new_files = []
    for content, filename in zip(contents, filenames):
        _, content_string = content.split(",")
        decoded = base64.b64decode(content_string)
        new_files.append({
            "name": filename,
            "content": content_string,
            "size": len(decoded),
        })
    
    return (existing_files or []) + new_files


@callback(
    Output("merge-file-list", "children"),
    Output("merge-options", "style"),
    Input("merge-files-store", "data"),
)
def update_merge_file_list(files):
    """Update the file list display for merge."""
    if not files:
        return html.Div(), {"display": "none"}
    return create_file_list(files, show_reorder=True, id_prefix="merge"), {"display": "block", "marginTop": "1rem"}


@callback(
    Output("merge-files-store", "data", allow_duplicate=True),
    Input({"type": "merge-remove", "index": ALL}, "n_clicks"),
    State("merge-files-store", "data"),
    prevent_initial_call=True,
)
def remove_merge_file(remove_clicks, files):
    """Handle file removal for merge."""
    if not files or not ctx.triggered_id:
        raise PreventUpdate
    
    # Check if any actual click happened
    if not any(remove_clicks):
        raise PreventUpdate
    
    triggered = ctx.triggered_id
    if not isinstance(triggered, dict):
        raise PreventUpdate
    
    idx = triggered["index"]
    if idx >= len(files):
        raise PreventUpdate
        
    files = files.copy()
    files.pop(idx)
    
    return files


@callback(
    Output("merge-files-store", "data", allow_duplicate=True),
    Input({"type": "merge-move-up", "index": ALL}, "n_clicks"),
    Input({"type": "merge-move-down", "index": ALL}, "n_clicks"),
    State("merge-files-store", "data"),
    prevent_initial_call=True,
)
def reorder_merge_files(up_clicks, down_clicks, files):
    """Handle file reordering via buttons for merge."""
    if not files or not ctx.triggered_id:
        raise PreventUpdate
    
    # Check if any actual click happened
    all_clicks = (up_clicks or []) + (down_clicks or [])
    if not any(all_clicks):
        raise PreventUpdate
    
    triggered = ctx.triggered_id
    if not isinstance(triggered, dict):
        raise PreventUpdate
    
    idx = triggered["index"]
    action = triggered["type"]
    files = files.copy()
    
    if action == "merge-move-up" and idx > 0:
        files[idx], files[idx - 1] = files[idx - 1], files[idx]
    elif action == "merge-move-down" and idx < len(files) - 1:
        files[idx], files[idx + 1] = files[idx + 1], files[idx]
    
    return files


@callback(
    Output("merge-result", "children"),
    Input("merge-btn", "n_clicks"),
    State("merge-files-store", "data"),
    State("merge-output-name", "value"),
    prevent_initial_call=True,
)
def merge_pdfs(n_clicks, files, output_name):
    """Execute PDF merge."""
    if not n_clicks or not files:
        raise PreventUpdate
    
    if len(files) < 2:
        return create_error_alert("Please upload at least 2 PDF files to merge.")
    
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            input_paths = []
            for f in files:
                file_path = tmp_path / f["name"]
                file_path.write_bytes(base64.b64decode(f["content"]))
                input_paths.append(file_path)
            
            output_path = tmp_path / output_name
            result_path = pdf_tool.merge(input_paths, output_path)
            
            result_bytes = result_path.read_bytes()
            result_b64 = base64.b64encode(result_bytes).decode()
            
            return html.Div([
                create_success_alert(f"✓ Successfully merged {len(files)} PDFs!"),
                create_download_button(
                    f"data:application/pdf;base64,{result_b64}",
                    output_name,
                    "Download Merged PDF"
                ),
            ])
    except Exception as e:
        return create_error_alert(f"Error merging PDFs: {str(e)}")


# =============================================================================
# Compress Callbacks
# =============================================================================

@callback(
    Output("compress-file-store", "data"),
    Input("compress-upload", "contents"),
    State("compress-upload", "filename"),
    prevent_initial_call=True,
)
def handle_compress_upload(content, filename):
    """Handle file upload for compression."""
    if content is None:
        raise PreventUpdate
    
    _, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    
    return {
        "name": filename,
        "content": content_string,
        "size": len(decoded),
    }


@callback(
    Output("compress-file-info", "children"),
    Output("compress-options", "style"),
    Output("compress-output-name", "value"),
    Input("compress-file-store", "data"),
)
def update_compress_file_info(file_data):
    """Update the file info display for compression."""
    if not file_data:
        return html.Div(), {"display": "none"}, "compressed.pdf"
    
    default_name = f"{Path(file_data['name']).stem}_compressed.pdf"
    
    info = html.Div([
        html.Strong(file_data["name"]),
        html.Span(" — Original size: ", style={"color": "#a8a29e"}),
        html.Strong(f"{file_data['size'] / 1024:.1f} KB"),
    ], className="file-list-container", style={"borderLeftColor": "#d97706"})
    
    return info, {"display": "block", "marginTop": "1rem"}, default_name


@callback(
    Output("compress-level-desc", "children"),
    Input("compress-level", "value"),
)
def update_compress_level_desc(level):
    """Update compression level description."""
    if level:
        return COMPRESSION_DESCRIPTIONS.get(level, "")
    return ""


@callback(
    Output("compress-result", "children"),
    Input("compress-btn", "n_clicks"),
    State("compress-file-store", "data"),
    State("compress-level", "value"),
    State("compress-output-name", "value"),
    prevent_initial_call=True,
)
def compress_pdf(n_clicks, file_data, level, output_name):
    """Execute PDF compression."""
    if not n_clicks or not file_data:
        raise PreventUpdate
    
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    
    compression_level = get_compression_level(level)
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            input_path = tmp_path / file_data["name"]
            input_path.write_bytes(base64.b64decode(file_data["content"]))
            
            output_path = tmp_path / output_name
            result_path = pdf_tool.compress(input_path, output_path, compression_level)
            
            result_bytes = result_path.read_bytes()
            result_b64 = base64.b64encode(result_bytes).decode()
            
            original_size_kb = file_data["size"] / 1024
            new_size_kb = len(result_bytes) / 1024
            reduction = ((original_size_kb - new_size_kb) / original_size_kb) * 100
            
            return html.Div([
                create_success_alert("✓ Compression complete!"),
                create_metrics(original_size_kb, new_size_kb, reduction),
                create_download_button(
                    f"data:application/pdf;base64,{result_b64}",
                    output_name,
                    "Download Compressed PDF"
                ),
            ])
    except Exception as e:
        return create_error_alert(f"Error compressing PDF: {str(e)}")


# =============================================================================
# Split Callbacks
# =============================================================================

@callback(
    Output("split-file-store", "data"),
    Input("split-upload", "contents"),
    State("split-upload", "filename"),
    prevent_initial_call=True,
)
def handle_split_upload(content, filename):
    """Handle file upload for splitting."""
    if content is None:
        raise PreventUpdate
    
    _, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(decoded)
        tmp.flush()
        page_count = pdf_tool.get_page_count(Path(tmp.name))
    
    return {
        "name": filename,
        "content": content_string,
        "size": len(decoded),
        "page_count": page_count,
    }


@callback(
    Output("split-file-info", "children"),
    Output("split-options", "style"),
    Input("split-file-store", "data"),
)
def update_split_file_info(file_data):
    """Update the file info display for splitting."""
    if not file_data:
        return html.Div(), {"display": "none"}
    
    info = html.Div([
        html.Strong(file_data["name"]),
        html.Span(" — ", style={"color": "#a8a29e"}),
        html.Strong(f"{file_data['page_count']} pages"),
        html.Span(f" ({file_data['size'] / 1024:.1f} KB)", style={"color": "#78716c"}),
    ], className="file-list-container", style={"borderLeftColor": "#d97706"})
    
    return info, {"display": "block", "marginTop": "1rem"}


@callback(
    Output("split-mode-options", "children"),
    Input("split-mode", "value"),
    State("split-file-store", "data"),
)
def update_split_mode_options(mode, file_data):
    """Update split mode options based on selected mode."""
    page_count = file_data["page_count"] if file_data else 1
    
    if mode == "range":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("Start Page", className="form-label"),
                    dbc.Input(id="split-start-page", type="number", min=1, max=page_count, value=1, className="form-control"),
                ]),
                dbc.Col([
                    html.Label("End Page", className="form-label"),
                    dbc.Input(id="split-end-page", type="number", min=1, max=page_count, value=page_count, className="form-control"),
                ]),
            ], className="g-3"),
            dcc.Store(id="split-pages-input", data=""),
            dcc.Store(id="split-every-n", data=1),
        ])
    
    elif mode == "pages":
        return html.Div([
            html.Label("Pages to Extract", className="form-label"),
            dbc.Input(
                id="split-pages-input", 
                type="text", 
                placeholder=f"e.g., 1, 3, 5-7 (max: {page_count})",
                className="form-control"
            ),
            html.Div("Enter page numbers separated by commas. Use hyphens for ranges (e.g., 1-3).", 
                    className="compression-desc"),
            dcc.Store(id="split-start-page", data=1),
            dcc.Store(id="split-end-page", data=page_count),
            dcc.Store(id="split-every-n", data=1),
        ])
    
    elif mode == "every_n":
        return html.Div([
            html.Label("Pages per File", className="form-label"),
            dbc.Input(id="split-every-n", type="number", min=1, max=page_count, value=1, className="form-control"),
            html.Div("The PDF will be split into multiple files, each containing this many pages.", 
                    className="compression-desc"),
            dcc.Store(id="split-start-page", data=1),
            dcc.Store(id="split-end-page", data=page_count),
            dcc.Store(id="split-pages-input", data=""),
        ])
    
    return html.Div()


def _parse_page_input(page_string: str, max_page: int) -> list[int]:
    """Parse page input like '1, 3, 5-7' into a list of page numbers."""
    pages = []
    parts = page_string.replace(" ", "").split(",")
    
    for part in parts:
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
            if start > end:
                start, end = end, start
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(part))
    
    pages = sorted(set(pages))
    invalid = [p for p in pages if p < 1 or p > max_page]
    if invalid:
        raise ValueError(f"Invalid page numbers: {invalid}. Document has {max_page} pages.")
    
    return pages


@callback(
    Output("split-result", "children"),
    Input("split-btn", "n_clicks"),
    State("split-file-store", "data"),
    State("split-mode", "value"),
    State("split-start-page", "value"),
    State("split-end-page", "value"),
    State("split-pages-input", "value"),
    State("split-every-n", "value"),
    prevent_initial_call=True,
)
def split_pdf(n_clicks, file_data, mode, start_page, end_page, pages_input, every_n):
    """Execute PDF split."""
    if not n_clicks or not file_data:
        raise PreventUpdate
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            input_path = tmp_path / file_data["name"]
            input_path.write_bytes(base64.b64decode(file_data["content"]))
            
            page_count = file_data["page_count"]
            output_files = []
            
            if mode == "range":
                start = int(start_page) if start_page else 1
                end = int(end_page) if end_page else page_count
                output_files = pdf_tool.split_by_ranges(input_path, tmp_path, [(start, end)])
            
            elif mode == "pages":
                if not pages_input:
                    return create_error_alert("Please enter page numbers to extract.")
                pages = _parse_page_input(pages_input, page_count)
                output_name = f"{input_path.stem}_extracted.pdf"
                output_files = [pdf_tool.extract_pages(input_path, tmp_path / output_name, pages)]
            
            elif mode == "every_n":
                n = int(every_n) if every_n else 1
                output_files = pdf_tool.split_every_n_pages(input_path, tmp_path, n)
            
            # Single file - direct download
            if len(output_files) == 1:
                result_bytes = output_files[0].read_bytes()
                result_b64 = base64.b64encode(result_bytes).decode()
                output_name = output_files[0].name
                
                return html.Div([
                    create_success_alert("✓ PDF split successfully!"),
                    create_download_button(
                        f"data:application/pdf;base64,{result_b64}",
                        output_name,
                        f"Download {output_name}"
                    ),
                ])
            
            # Multiple files - create ZIP
            zip_path = tmp_path / f"{input_path.stem}_split.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                for output_file in output_files:
                    zf.write(output_file, output_file.name)
            
            zip_bytes = zip_path.read_bytes()
            zip_b64 = base64.b64encode(zip_bytes).decode()
            
            file_list = html.Ul([
                html.Li(f.name, style={"color": "#d6d3d1"}) for f in output_files
            ], style={"marginTop": "0.5rem", "marginBottom": "1rem"})
            
            return html.Div([
                create_success_alert(f"✓ Created {len(output_files)} files!"),
                file_list,
                create_download_button(
                    f"data:application/zip;base64,{zip_b64}",
                    f"{input_path.stem}_split.zip",
                    "Download All (ZIP)"
                ),
            ])
    
    except ValueError as e:
        return create_error_alert(f"Error: {str(e)}")
    except Exception as e:
        return create_error_alert(f"Error splitting PDF: {str(e)}")
