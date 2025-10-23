#!/usr/bin/env python3
"""
Convert remaining Flyberry markdown documents (31-34) to HTML
"""

import re
from pathlib import Path

def markdown_to_html(md_content):
    """Convert markdown to HTML (simple implementation)"""
    html = md_content

    # Headers
    html = re.sub(r'^### (.+)$', r'<h3 id="\1">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 id="\1">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1 id="\1">\1</h1>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Lists
    lines = html.split('\n')
    in_list = False
    in_ordered_list = False
    result = []

    for line in lines:
        # Unordered lists
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            result.append(f'<li>{content}</li>')
        # Ordered lists
        elif re.match(r'^\d+\. ', line.strip()):
            if not in_ordered_list:
                result.append('<ol>')
                in_ordered_list = True
            content = re.sub(r'^\d+\. ', '', line.strip())
            result.append(f'<li>{content}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if in_ordered_list:
                result.append('</ol>')
                in_ordered_list = False

            # Horizontal rules
            if line.strip() == '---':
                result.append('<hr />')
            # Code blocks
            elif line.strip().startswith('```'):
                continue
            # Paragraphs
            elif line.strip() and not line.startswith('<'):
                result.append(f'<p>{line.strip()}</p>')
            else:
                result.append(line)

    if in_list:
        result.append('</ul>')
    if in_ordered_list:
        result.append('</ol>')

    return '\n'.join(result)

def create_html_doc(doc_number, title, md_file):
    """Create HTML document from markdown"""

    # Read markdown
    md_content = Path(md_file).read_text()

    # Extract metadata
    lines = md_content.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---' and i > 0:
            content_start = i + 1
            break

    content = '\n'.join(lines[content_start:]) if content_start > 0 else md_content

    # Convert markdown to HTML
    html_content = markdown_to_html(content)

    # Determine navigation (all link back to Act 6 since others not converted yet)
    prev_link = 'act-6-operating-plan.html#doc-' + str(doc_number - 1) if doc_number > 30 else 'act-6-operating-plan.html'
    prev_label = f'Act 6: Doc {doc_number-1}' if doc_number > 30 else 'Act 6'

    next_link = 'act-6-operating-plan.html#doc-' + str(doc_number + 1) if doc_number < 35 else 'act-6-operating-plan.html'
    next_label = f'Act 6: Doc {doc_number+1}' if doc_number < 35 else 'Back to Act 6'

    # Map filenames
    filename_map = {
        31: 'doc-31-brand-designer-brief',
        32: 'doc-32-packaging-requirements',
        33: 'doc-33-retail-experience',
        34: 'doc-34-digital-strategy'
    }

    # Create HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doc {doc_number}: {title} - Flyberry Brand Package</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <a href="index.html" class="header-title">Flyberry Brand Package</a>
                <nav class="header-nav">
                    <a href="index.html" class="nav-link">Home</a>
                    <a href="act-1-who-we-are.html" class="nav-link">Act 1</a>
                    <a href="act-2-where-we-are.html" class="nav-link">Act 2</a>
                    <a href="act-3-where-we-go.html" class="nav-link">Act 3</a>
                    <a href="act-4-where-we-should-go.html" class="nav-link">Act 4</a>
                    <a href="act-6-operating-plan.html" class="nav-link active">Act 6</a>
                </nav>
            </div>
        </div>
    </header>

    <div class="breadcrumb">
        <div class="container">
            <ul class="breadcrumb-list">
                <li class="breadcrumb-item"><a href="index.html">Home</a></li>
                <li class="breadcrumb-item"><a href="act-6-operating-plan.html">ACT 6: OPERATING PLAN</a></li>
                <li class="breadcrumb-item">Doc {doc_number}: {title}</li>
            </ul>
        </div>
    </div>

    <div class="container">
        <div class="layout-grid">
            <aside class="sidebar">
                <div class="toc">
                    <h3 class="toc-title">Document Navigation</h3>
                    <ul class="toc-list">
                        <li class="toc-item">
                            <a href="act-6-operating-plan.html" class="toc-link">
                                ← Back to Act 6
                            </a>
                        </li>
                    </ul>
                    <div style="margin-top: 20px; padding: 12px; background: #f8fafc; border-radius: 6px; font-size: 14px;">
                        <div style="font-weight: 600; margin-bottom: 6px;">Also available:</div>
                        <a href="{filename_map[doc_number]}.md" style="color: #2563eb; text-decoration: none;">📄 Download Markdown</a>
                    </div>
                </div>
            </aside>

            <main class="main-content">
                <div class="document-section">
                    <div class="document-header">
                        <div class="document-meta">
                            <span class="document-number">Document {doc_number}</span>
                            <span class="document-category">ACT 6: OPERATING PLAN</span>
                        </div>
                    </div>
                    <div class="document-content">
{html_content}
                    </div>
                </div>

                <!-- Navigation Footer -->
                <nav class="nav-footer">
                    <a href="{prev_link}" class="nav-prev">
                        <span>←</span>
                        <div>
                            <div class="nav-label">Previous</div>
                            <div>{prev_label}</div>
                        </div>
                    </a>
                    <a href="{next_link}" class="nav-next">
                        <div>
                            <div class="nav-label">Next</div>
                            <div>{next_label}</div>
                        </div>
                        <span>→</span>
                    </a>
                </nav>
            </main>
        </div>
    </div>

    <!-- Footer -->
    <footer class="mt-5 pt-4 border-top">
        <div class="container text-center text-muted">
            <p>Created by Growth Darji | October 2025</p>
        </div>
    </footer>

    <script src="assets/scripts.js"></script>
</body>
</html>"""

    return html_template

if __name__ == '__main__':
    # Convert doc-31
    html_31 = create_html_doc(31, 'Brand Designer Brief', 'docs/doc-31-brand-designer-brief.md')
    Path('docs/doc-31-brand-designer-brief.html').write_text(html_31)
    print('✅ Created docs/doc-31-brand-designer-brief.html')

    # Convert doc-32
    html_32 = create_html_doc(32, 'Packaging Requirements', 'docs/doc-32-packaging-requirements.md')
    Path('docs/doc-32-packaging-requirements.html').write_text(html_32)
    print('✅ Created docs/doc-32-packaging-requirements.html')

    # Convert doc-33
    html_33 = create_html_doc(33, 'Retail Experience Blueprint', 'docs/doc-33-retail-experience.md')
    Path('docs/doc-33-retail-experience.html').write_text(html_33)
    print('✅ Created docs/doc-33-retail-experience.html')

    # Convert doc-34
    html_34 = create_html_doc(34, 'Digital Strategy', 'docs/doc-34-digital-strategy.md')
    Path('docs/doc-34-digital-strategy.html').write_text(html_34)
    print('✅ Created docs/doc-34-digital-strategy.html')
