import os
import html

NOTES_DIR = r"D:\Balaji\Code\Python\My_Support\latex_guide\notes"
OUTPUT_DIR = r"D:\Balaji\Code\Python\My_Support\latex_guide\core\templates\core"

NOTE_MAP = {
    'latex2docx': 'LaTeX2Docx_Note.txt',
    'uppreedit': 'UP_Preedit.txt',
    'uptypeset': 'UP_Note.txt',
    'olhtypeset': 'OLH_Note.txt',
    'latextoxml': 'LaTeXML_Note.txt',
}

def parse_txt_to_html(filepath, title, slug):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.read().split('\n')
        
    parsed_blocks = []
    current_block_type = 'text'
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_code = False
        
        if (stripped.startswith('$') or '`' in stripped or stripped.startswith('\\') 
            or stripped.startswith('Server:') or stripped.startswith('Local:')):
            is_code = True
        elif len(line) - len(line.lstrip()) >= 3 and stripped != '':
            is_code = True
        elif stripped and all(c in '-=' for c in stripped) and len(stripped) >= 3:
            if current_block_type == 'code':
                is_code = True

        is_heading = False
        if stripped and stripped.isupper() and len(stripped) > 3:
            is_heading = True
        elif len(lines) > i + 1 and lines[i+1].strip() and all(c in '-=' for c in lines[i+1].strip()) and len(lines[i+1].strip()) >= 3:
            is_heading = True
            
        if is_code:
            if current_block_type == 'text':
                if current_lines:
                    parsed_blocks.append({'type': 'text', 'content': '\n'.join(current_lines)})
                current_lines = [line]
                current_block_type = 'code'
            else:
                current_lines.append(line)
        else:
            if current_block_type == 'code':
                if current_lines:
                    parsed_blocks.append({'type': 'code', 'content': '\n'.join(current_lines)})
                current_lines = [line]
                current_block_type = 'text'
            else:
                if is_heading:
                    if current_lines:
                        parsed_blocks.append({'type': 'text', 'content': '\n'.join(current_lines)})
                        current_lines = []
                    parsed_blocks.append({'type': 'heading', 'content': stripped})
                else:
                    if stripped and all(c in '-=' for c in stripped) and len(stripped) >= 3:
                        pass
                    else:
                        current_lines.append(line)
                        
    if current_lines:
        parsed_blocks.append({'type': current_block_type, 'content': '\n'.join(current_lines)})

    html_parts = [
        "{% extends 'core/base.html' %}",
        "{% block content %}",
        f'<div class="note-viewer">',
        f'    <h2>{title} - Interactive Checklist</h2>',
        f'    <div class="note-content">',
        '        {% verbatim %}'
    ]
    
    chk_index = 1
    
    # We will group contiguous text+code blocks under a single checklist item
    # A heading breaks the group.
    
    i = 0
    while i < len(parsed_blocks):
        block = parsed_blocks[i]
        
        if block['type'] == 'heading':
            content = block['content'].strip()
            if content:
                html_parts.append(f'        <h3 class="note-heading">{html.escape(content)}</h3>')
            i += 1
            continue
            
        if block['type'] == 'text':
            content = block['content'].strip()
            if not content:
                i += 1
                continue
                
            # Start checklist item
            html_parts.append('        <div class="checklist-item">')
            html_parts.append(f'            <input type="checkbox" id="{slug}_{chk_index}" class="check-box">')
            html_parts.append('            <div class="step-content">')
            
            # Use label for the text
            escaped_text = html.escape(content).replace('\n', '<br>')
            html_parts.append(f'                <label for="{slug}_{chk_index}"><strong>{escaped_text}</strong></label>')
            
            # Check if next block(s) are code, if so append them inside this checklist item
            i += 1
            while i < len(parsed_blocks) and parsed_blocks[i]['type'] == 'code':
                code_content = parsed_blocks[i]['content'].strip()
                if code_content:
                    escaped_code = html.escape(code_content)
                    html_parts.append('                <div class="code-wrapper">')
                    html_parts.append('                    <button class="copy-btn" aria-label="Copy to clipboard">Copy</button>')
                    html_parts.append(f'                    <pre><code>{escaped_code}</code></pre>')
                    html_parts.append('                </div>')
                i += 1
                
            html_parts.append('            </div>')
            html_parts.append('        </div>')
            chk_index += 1
            
        elif block['type'] == 'code':
            # Code without preceding text
            html_parts.append('        <div class="checklist-item">')
            html_parts.append(f'            <input type="checkbox" id="{slug}_{chk_index}" class="check-box">')
            html_parts.append('            <div class="step-content">')
            html_parts.append(f'                <label for="{slug}_{chk_index}">Code action:</label>')
            
            code_content = block['content'].strip()
            escaped_code = html.escape(code_content)
            html_parts.append('                <div class="code-wrapper">')
            html_parts.append('                    <button class="copy-btn" aria-label="Copy to clipboard">Copy</button>')
            html_parts.append(f'                    <pre><code>{escaped_code}</code></pre>')
            html_parts.append('                </div>')
            html_parts.append('            </div>')
            html_parts.append('        </div>')
            
            chk_index += 1
            i += 1

    html_parts.append('        {% endverbatim %}')
    html_parts.append('    </div>')
    html_parts.append('</div>')
    html_parts.append('{% endblock %}')
    
    return '\n'.join(html_parts)

for slug, filename in NOTE_MAP.items():
    if slug != 'latextoxml': continue
    in_path = os.path.join(NOTES_DIR, filename)
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    title = filename.replace('_', ' ').replace('.txt', '')
    if os.path.exists(in_path):
        html_output = parse_txt_to_html(in_path, title, slug)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"Generated {out_path}")
