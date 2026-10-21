#!/usr/bin/env python3
"""Build the Applify Kodi HTTP source for GitHub Pages (Python 3.9+)."""
import argparse
import ast
import copy
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
SKIN_ID = 'skin.applify'
REPOSITORY_ID = 'repository.applify'
REPOSITORY_VERSION = '1.0.0'


def write_xml(path, element):
    ET.indent(element, space='  ')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ET.tostring(element, encoding='utf-8', xml_declaration=True) + b'\n')


def md5_file(path):
    path.with_suffix(path.suffix + '.md5').write_text(
        hashlib.md5(path.read_bytes()).hexdigest() + '\n')


def newest_skin():
    candidates = []
    for path in ROOT.glob('skin.applify-*.zip'):
        match = re.fullmatch(r'skin\.applify-(\d+)\.(\d+)\.(\d+)\.zip', path.name)
        if match:
            candidates.append((tuple(map(int, match.groups())), path))
    if not candidates:
        raise ValueError('Upload skin.applify-X.Y.Z.zip beside build_repository.py')
    return max(candidates)[1]


def validate_skin(path):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('Corrupt skin ZIP')
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate ZIP paths')
        for entry in archive.infolist():
            parts = PurePosixPath(entry.filename)
            if (parts.is_absolute() or '..' in parts.parts or '\\' in entry.filename
                    or not parts.parts or parts.parts[0] != SKIN_ID
                    or (entry.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError('Unsupported ZIP path: ' + entry.filename)
            if entry.filename.endswith('.xml'):
                ET.fromstring(archive.read(entry))
            elif entry.filename.endswith('.py'):
                ast.parse(archive.read(entry).decode('utf-8'), filename=entry.filename)
        addon = ET.fromstring(archive.read(SKIN_ID + '/addon.xml'))
        version = addon.get('version')
        if (addon.get('id') != SKIN_ID or addon.get('name') != 'Applify'
                or not re.fullmatch(r'\d+\.\d+\.\d+', version or '')
                or path.name != f'{SKIN_ID}-{version}.zip'):
            raise ValueError('Skin ZIP name must match Applify addon.xml ID/version')
        fonts = ET.fromstring(archive.read(SKIN_ID + '/xml/Font.xml'))
        for name in sorted({item.text or '' for item in fonts.findall('.//filename')}):
            if not name.endswith('.ttf') or SKIN_ID + '/fonts/' + name not in names:
                raise ValueError('Missing font: ' + name)
            if archive.read(SKIN_ID + '/fonts/' + name)[:4] not in (b'OTTO', b'\x00\x01\x00\x00'):
                raise ValueError('Invalid font: ' + name)
        icon = archive.read(SKIN_ID + '/resources/icon.png')
    return addon, icon


def build(base_url, output):
    parsed = urlsplit(base_url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('--base-url must be the HTTPS GitHub Pages site URL')
    base_url = base_url.rstrip('/')
    skin_zip = newest_skin()
    skin, icon = validate_skin(skin_zip)
    version = skin.get('version')
    # Output is dedicated generated content, never the source directory.
    output = output.resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError('Choose a dedicated output subdirectory')
    output.mkdir(parents=True, exist_ok=True)
    skin_dir = output / SKIN_ID
    skin_dir.mkdir(exist_ok=True)
    shutil.copyfile(skin_zip, skin_dir / skin_zip.name)
    md5_file(skin_dir / skin_zip.name)
    write_xml(skin_dir / 'addon.xml', copy.deepcopy(skin))
    (skin_dir / 'icon.png').write_bytes(icon)

    repo = ET.Element('addon', {'id': REPOSITORY_ID, 'version': REPOSITORY_VERSION,
                              'name': 'Applify Repository', 'provider-name': 'Kamil'})
    extension = ET.SubElement(repo, 'extension', {'point': 'xbmc.addon.repository',
                                                'name': 'Applify Repository'})
    directory = ET.SubElement(extension, 'dir')
    ET.SubElement(directory, 'info', {'compressed': 'false'}).text = base_url + '/addons.xml'
    ET.SubElement(directory, 'checksum').text = base_url + '/addons.xml.md5'
    ET.SubElement(directory, 'datadir', {'zip': 'true'}).text = base_url + '/'
    metadata = ET.SubElement(repo, 'extension', {'point': 'xbmc.addon.metadata'})
    ET.SubElement(metadata, 'summary', {'lang': 'en_GB'}).text = 'Install and update the Applify Kodi skin.'
    ET.SubElement(metadata, 'description', {'lang': 'en_GB'}).text = 'Official distribution repository for Applify, maintained by its creator Kamil.'
    ET.SubElement(metadata, 'platform').text = 'all'
    ET.SubElement(metadata, 'license').text = 'MIT'
    ET.SubElement(ET.SubElement(metadata, 'assets'), 'icon').text = 'icon.png'
    repo_dir = output / REPOSITORY_ID
    repo_dir.mkdir(exist_ok=True)
    write_xml(repo_dir / 'addon.xml', copy.deepcopy(repo))
    (repo_dir / 'icon.png').write_bytes(icon)
    installer_name = f'{REPOSITORY_ID}-{REPOSITORY_VERSION}.zip'
    with tempfile.TemporaryDirectory() as temp:
        source = Path(temp) / REPOSITORY_ID
        source.mkdir()
        write_xml(source / 'addon.xml', copy.deepcopy(repo))
        (source / 'icon.png').write_bytes(icon)
        (source / 'LICENSE.txt').write_text(
            'MIT License\n\nCopyright (c) 2026 Kamil\n\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy '
            'of this software and associated documentation files (the "Software"), to deal '
            'in the Software without restriction, including without limitation the rights '
            'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '
            'copies of the Software, and to permit persons to whom the Software is '
            'furnished to do so, subject to the following conditions:\n\n'
            'The above copyright notice and this permission notice shall be included in '
            'all copies or substantial portions of the Software.\n\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
            'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
            'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL '
            'THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
            'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING '
            'FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER '
            'DEALINGS IN THE SOFTWARE.\n')
        with zipfile.ZipFile(repo_dir / installer_name, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(source.iterdir()):
                archive.write(path, REPOSITORY_ID + '/' + path.name)
    md5_file(repo_dir / installer_name)
    # The bootstrap ZIP is at the source root, so Kodi users see it immediately.
    shutil.copyfile(repo_dir / installer_name, output / installer_name)
    md5_file(output / installer_name)
    index = ET.Element('addons')
    index.extend([copy.deepcopy(skin), copy.deepcopy(repo)])
    write_xml(output / 'addons.xml', index)
    md5_file(output / 'addons.xml')
    (output / '.nojekyll').touch()
    # Keep a plain filename anchor. Kodi's HTTP directory parser reads this link.
    (output / 'index.html').write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Applify Kodi Source</title></head><body>\n'
        '<h1>Applify Kodi Source</h1>\n'
        f'<p>Applify v{html.escape(version)}</p>\n'
        f'<p><a href="{installer_name}">{installer_name}</a></p>\n'
        '<p>In Kodi: File manager → Add source → enter this page URL. '
        'Then Add-ons → Install from ZIP file → Applify → select the repository ZIP.</p>\n'
        '<p>Next: Install from repository → Applify Repository → Look and feel → Skin → Applify.</p>\n'
        f'<p>Source URL: <code>{html.escape(base_url)}/</code></p>\n'
        '</body></html>\n')
    config = {'name': 'Applify', 'skin_id': SKIN_ID, 'skin_version': version,
              'repository_id': REPOSITORY_ID, 'repository_version': REPOSITORY_VERSION,
              'source_url': base_url + '/', 'repository_zip': base_url + '/' + installer_name,
              'skin_zip': base_url + '/' + SKIN_ID + '/' + skin_zip.name}
    (output / 'repository-config.json').write_text(json.dumps(config, indent=2) + '\n')
    print(json.dumps(config, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', required=True, help='URL reported by actions/configure-pages')
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    build(args.base_url, args.output)
