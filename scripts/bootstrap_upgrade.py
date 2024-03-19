import os
import re

# Patterns of breaking changes between Bootstrap 2.6 and 5
breaking_changes = {
    'col-form-legend': 'col-form-label', 
    'input-group-addon': 'input-group-prepend',
    'input-group-btn': 'input-group-append',
    'no-gutters': 'g-0',
    '.media': '',
    '.order-*': '',
    'make-col': '',
    'thead-light': '',
    'thead-dark': '',
    '.pre-scrollable': '',
    'text-justify': '',
    'custom-check': 'form-check',
    'custom-switch': 'form-switch',
    'custom-select': 'form-select',
    'custom-file': 'form-control',
    'form-file': 'form-control',
    'form-control-file': '',
    'form-control-range': '',
    'input-group-append': 'input-group-text',
    'input-group-prepend': 'input-group-text',
    'label': '',
    'form-text': '',
    'badge-*': 'bg-*',
    'badge-pill': 'rounded-pill',
    'btn-block': '',
    'card-deck': '',
    'card-columns': '',
    'card': '',
    'close': 'btn-close',    
    'flip': '',
    'arrow': 'popover-arrow',
    'arrow': 'tooltip-arrow',
    'whiteList': 'allowList',
    'left-*': 'start-*',
    'right-*': 'end-*',
    '.border-left': '.border-start',
    '.border-right': '.border-end',
    '.rounded-left': '.rounded-start',
    '.rounded-right': '.rounded-end',
    '.ml-*': '.ms-*',
    '.mr-*': '.me-*',
    '.pl-*': '.ps-*',
    '.text-left': '.text-start',
    '.text-right': '.text-end',
    '.text-monospace': '.font-monospace',
    '.text-hide': '',
    '.front-weight-*': '.fw-*',
    '.front-style-*': '.fst-*',
    '.rounded-sm': '.rounded-1',
    '.rounded-lg': '.rounded-3',
    '.ratio-*': '',
    'data-toggle': 'data-bs-toggle',
}

def find_breaking_changes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('bootstrap_') or file.startswith('bootstrap-'):
                continue
            if file.endswith('.html') or file.endswith('.css') or file.endswith('.js'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.readlines()
                for line_num, line in enumerate(contents, 1):
                    for old, new in breaking_changes.items():
                        if re.search(old, line):
                            print(f"File: {file_path}, Line: {line_num}, Change: '{old}' to '{new}'")

# Point at your project directory to find breaking changes
find_breaking_changes('../wcoa/')
