"""Fix hardcoded C:/AfricaRCT paths in all student code files."""
import os, re

ROOT = "C:/Users/user/africa-e156-students"

# Patterns to replace
REPLACEMENTS = [
    # DATA_DIR = Path("C:/AfricaRCT/data") → Path(__file__).parent / "data"
    (r'DATA_DIR\s*=\s*Path\("C:/AfricaRCT/data"\)', 'DATA_DIR = Path(__file__).parent / "data"'),
    # AFRICA_CACHE / COMP_CACHE pointing to C:/AfricaRCT/data/
    (r'(AFRICA_CACHE|COMP_CACHE)\s*=\s*DATA_DIR\s*/\s*"([^"]+)"', r'\1 = DATA_DIR / "\2"'),
    # OUTPUT_HTML = Path("C:/AfricaRCT/...")
    (r'OUTPUT_HTML\s*=\s*Path\("C:/AfricaRCT/[^"]*"', 'OUTPUT_HTML = Path(__file__).parent / "output.html"'),
    # open("C:/AfricaRCT/data/X.json", "w")
    (r'open\("C:/AfricaRCT/data/([^"]+)"', r'open(str(Path(__file__).parent / "data" / "\1")'),
    # open("C:/AfricaRCT/data/X.json", 'r')
    # (already covered by above)
    # open(DATA_DIR / "X.json", "w") -- these are fine if DATA_DIR is fixed
    # Remaining C:/AfricaRCT references in strings (HTML content etc)
    (r'"C:/AfricaRCT/data/', '"data/'),
    (r"'C:/AfricaRCT/data/", "'data/"),
    # References in HTML strings
    (r'C:\\\\AfricaRCT\\\\', ''),
    (r'C:/AfricaRCT/', ''),
]

fixed_count = 0
file_count = 0

for dirpath, dirs, files in os.walk(ROOT):
    for fname in sorted(files):
        if not fname.endswith('.py'):
            continue
        if fname in ('build.py', 'generate_dashboards.py', 'fix_paths.py', 'fetch_africa_rcts_by_country.py'):
            continue

        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()

        modified = original
        changes = 0
        for pattern, replacement in REPLACEMENTS:
            new_text = re.sub(pattern, replacement, modified)
            if new_text != modified:
                changes += re.subn(pattern, replacement, modified)[1]
                modified = new_text

        if changes > 0:
            # Ensure "from pathlib import Path" exists if we use Path(__file__)
            if 'Path(__file__)' in modified and 'from pathlib import Path' not in modified:
                modified = 'from pathlib import Path\n' + modified

            # Ensure data dir creation
            if 'Path(__file__).parent / "data"' in modified and 'makedirs' not in modified and 'mkdir' not in modified:
                # Add data dir creation after imports
                lines = modified.split('\n')
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        insert_idx = i + 1
                    elif insert_idx > 0 and line.strip() and not line.startswith('import ') and not line.startswith('from ') and not line.startswith('#'):
                        break
                lines.insert(insert_idx, '\nos.makedirs(Path(__file__).parent / "data", exist_ok=True)')
                modified = '\n'.join(lines)
                if 'import os' not in modified:
                    modified = 'import os\n' + modified

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(modified)
            fixed_count += changes
            file_count += 1
            print(f"  Fixed {changes:2d} paths in {os.path.relpath(fpath, ROOT)}")

print(f"\nTotal: {fixed_count} path fixes across {file_count} files")
