from converter import convert_html_to_text

LIMIT = 750

def generate_chunks(doc: str) -> list[str]:
    text = convert_html_to_text(doc)
    if len(text) <= LIMIT:
        return [text]
    chunks = text.split("\n\n")
    chunks = split_big_chunks(chunks)
    chunks = merge_small_chunks(chunks)
    return chunks

def split_big_chunks(chunks: list[str]):
    split_chunks = []
    for c in chunks:
        if len(c) <= LIMIT:
            split_chunks.append(c)
        else:
            split_chunks += split_big_chunk(c)
    return split_chunks

def split_big_chunk(chunk: str):
    lines = chunk.split("\n")
    chunks = []
    current = ""
    while lines:
        line = lines.pop(0)
        if is_bullet(line):
            # Don’t break up bulleted lists mid-list
            text = get_bullets(line, lines)
        elif is_header(line):
            # Keep headers together with paragraphs
            text = get_header(line, lines)
        else:
            text = line + "\n"
        if len(current) + len(text) > LIMIT:
            if current:
                chunks.append(current)
            current = text
        else:
            current += text
    if current:
        chunks.append(current)
    return chunks

def is_bullet(line):
    return line.startswith("* ")

def is_header(line):
    return line.startswith("# ") or line.startswith("## ") or line.startswith("### ") or line.startswith("#### ") or line.startswith("##### ") or line.startswith("###### ")

def get_bullets(bullet: str, lines: list[str]):
    bullets = bullet + "\n"
    while lines:
        if is_bullet(lines[0]):
            bullet_line = lines.pop(0)
            bullets += bullet_line + "\n"
        else:
            break
    return bullets

def get_header(header: str, lines: list[str]):
    header = header + "\n"
    while lines:
        is_paragraph = not (is_bullet(lines[0]) or is_header(lines[0]))
        with_paragraph = len(header) + len(lines[0])
        if is_paragraph and with_paragraph < LIMIT:
            paragraph = lines.pop(0)
            header += paragraph + "\n"
        else:
            break
    return header

def merge_small_chunks(chunks: list[str]):
    merged_chunks = []
    current_chunk = ""
    while chunks:
        chunk = chunks.pop(0)
        if len(current_chunk) + len(chunk) > LIMIT:
            if current_chunk:
                merged_chunks.append(current_chunk)
            current_chunk = chunk
        else:
            current_chunk += "\n" + chunk
    if current_chunk:
        merged_chunks.append(current_chunk)
    return merged_chunks