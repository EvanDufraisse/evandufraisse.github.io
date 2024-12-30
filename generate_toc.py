import re
import sys


def extract_markdown_headers(markdown_text):
    """
    Extracts markdown headers from the given text.

    Args:
        markdown_text (str): The markdown content.

    Returns:
        list of tuple: Each tuple contains the header text and its level (number of '#').
    """
    pattern = r'^(#{1,6})\s*(.+)$'
    matches = re.findall(pattern, markdown_text, re.MULTILINE)
    return [(header.strip(), len(hashes)) for hashes, header in matches]

def remove_toc(content):
    open_tag = re.escape('<span id="toc" style="display: none;"></span>')
    close_tag = re.escape('<span id="endtoc" style="display: none;"></span>')

    return re.sub(f"{open_tag}.*{close_tag}\n", "", content, flags=re.DOTALL)

def get_anchor_from_title(title):
    title = title.lower().strip()
    title = title.replace(";","")
    anchor = re.sub(r'[^\w\s-]', '-', title)
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-')
    return f"#{anchor}"

def remove_code_blocks(text):
    """
    Removes all code blocks enclosed by triple backticks (```).

    Args:
        text (str): The input text containing code blocks.

    Returns:
        str: The text with code blocks removed.
    """
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)

def generate_toc(headers, base_depth, max_depth):
    toc_html = (
        '<span id="toc" style="display: none;"></span>\n'
        '<div id="toc">'
        '<div class="py-6"></div>'
        '<div class="bg-black/5 dark:bg-white/10 rounded-lg px-6 py-1 shadow-lg transition-none">\n'
        '  <nav>\n'
        '    <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">Table of Contents</h2>\n'
        '    <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-4">\n'
    )

    current_level = 0
    numbering = []

    for header, level in headers:
        if level < base_depth:
            continue
        if level > max_depth:
            continue

        while current_level < level:
            toc_html += '    <ul class="list-disc list-inside pl-5 space-y-2">\n'
            numbering.append(0)
            current_level += 1

        while current_level > level:
            toc_html += '    </ul>\n'
            numbering.pop()
            current_level -= 1

        numbering[-1] += 1
        section_number = ".".join(map(str, numbering))
        anchor = get_anchor_from_title(header)
        toc_html += f'        <li class="text-gray-600 dark:text-gray-400"><a href="{anchor}" class="text-blue-600 hover:underline dark:text-blue-400">{section_number} {header}</a></li>\n'

    while current_level >= base_depth:
        toc_html += '    </ul>\n'
        current_level -= 1

    toc_html += (
        '    </ul>\n'
        '  </nav>\n'
        '</div>\n'
        '<div class="py-6"></div>\n'
        '</div>\n'
        '<span id="endtoc" style="display: none;"></span>'
    )
    return toc_html


def insert_toc(content, toc_html):
    if '<div id="toc"' in content:
        content = remove_toc(content)

    parts = content.split('---\n')
    if len(parts) > 2:
        return '---\n'.join(parts[:2]) + '---\n' + toc_html + '\n' + '---\n'.join(parts[2:])
    else:
        return content + '\n' + toc_html


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <base_depth>")
        sys.exit(1)

    input_file = sys.argv[1]
    base_depth = int(sys.argv[2])
    max_depth = int(sys.argv[3])

    with open(input_file, 'r') as file:
        content = file.read()

    content = remove_code_blocks(content)
    headers = extract_markdown_headers(content)

    toc_html = generate_toc(headers, base_depth, max_depth)
    with open(input_file, 'r') as file:
        content = file.read()
    updated_content = insert_toc(content, toc_html)

    with open(input_file, 'w') as file:
        file.write(updated_content)


if __name__ == "__main__":
    main()
