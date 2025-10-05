#!/usr/bin/python

# -*- coding: utf-8 -*-
# Copyright: (c) 2025
# License: MIT

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: github_download
short_description: Download assets from a GitHub release
description:
  - Downloads assets from a GitHub release.
  - Supports filtering assets by name, specific version, or downloading all assets.
  - Supports check mode to preview what would be downloaded.
options:
  repo:
    description:
      - GitHub repository in the format 'owner/repo'.
    required: true
    type: str
  version:
    description:
      - The release version tag (e.g. v0.1.0). Defaults to latest release.
    required: false
    type: str
    default: latest
  match:
    description:
      - A list of substrings to match in asset names.
      - If unspecified, all assets from the release are downloaded.
    required: false
    type: list
    elements: str
  download_dir:
    description:
      - Directory to download the assets to.
    required: false
    type: str
    default: /tmp
author:
  - Eyerogade
'''

EXAMPLES = r'''
- name: Download latest release of bat
  github_download:
    repo: sharkdp/bat
    match:
      - x86_64
      - musl
    download_dir: /tmp

- name: Download specific version of fd
  github_download:
    repo: sharkdp/fd
    version: v9.0.0
    match:
      - amd64
    download_dir: /opt/releases
'''

RETURN = r'''
changed:
  description: Whether any assets were downloaded or would be downloaded
  type: bool
  returned: always
downloaded_files:
  description: List of downloaded asset file paths (or would-be files in check mode)
  type: list
  returned: always
message:
  description: Status message
  type: str
  returned: always
'''

import os
import requests
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            repo=dict(type='str', required=True),
            version=dict(type='str', default='latest'),
            match=dict(type='list', elements='str', required=False, default=[]),
            download_dir=dict(type='str', default='/tmp'),
        ),
        supports_check_mode=True
    )

    repo = module.params['repo']
    version = module.params['version']
    match = module.params['match']
    download_dir = os.path.expanduser(module.params['download_dir'])

    if '/' not in repo:
        module.fail_json(msg="Invalid repo format. Expected 'owner/repo'")

    try:
        # Fetch release metadata
        if version == 'latest':
            url = f"https://api.github.com/repos/{repo}/releases/latest"
        else:
            url = f"https://api.github.com/repos/{repo}/releases/tags/{version}"

        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            module.fail_json(msg=f"Failed to fetch release info: {response.status_code} {response.text}")

        release_data = response.json()
        assets = release_data.get('assets', [])
        if not assets:
            module.exit_json(changed=False, message="No assets found in release", downloaded_files=[])

        os.makedirs(download_dir, exist_ok=True)
        to_download = []

        for asset in assets:
            asset_name = asset['name']
            download_url = asset['browser_download_url']

            # If match list given, only download matching assets
            if match and not any(m in asset_name for m in match):
                continue

            dest_path = os.path.join(download_dir, asset_name)
            if not os.path.exists(dest_path):
                to_download.append({
                    'name': asset_name,
                    'url': download_url,
                    'dest': dest_path
                })

        # --- Check Mode Behavior ---
        if module.check_mode:
            if not to_download:
                module.exit_json(
                    changed=False,
                    message="No new assets would be downloaded (all already exist or no matches found)",
                    downloaded_files=[]
                )
            else:
                would_download = [f"{a['name']} -> {a['dest']}" for a in to_download]
                module.exit_json(
                    changed=True,
                    message="Would download the following assets:\n" + "\n".join(would_download),
                    downloaded_files=would_download
                )

        # --- Normal Mode (actual download) ---
        downloaded = []
        for asset in to_download:
            try:
                r = requests.get(asset['url'], stream=True, timeout=30)
                r.raise_for_status()

                with open(asset['dest'], 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

                downloaded.append(asset['dest'])
            except Exception as e:
                module.fail_json(msg=f"Failed downloading {asset['name']}: {str(e)}")

        changed = len(downloaded) > 0
        msg = f"Downloaded {len(downloaded)} asset(s)" if changed else "No new assets downloaded"
        module.exit_json(changed=changed, message=msg, downloaded_files=downloaded)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Network error: {str(e)}")
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()
