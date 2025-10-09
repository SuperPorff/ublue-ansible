#!/usr/bin/env Justfile

# Show a list of available recipes
@_default:
    just --list --unsorted

# Setup build environment for molecule testing
setup:
    rm -rf .venv
    python3 -m venv .venv
    .venv/bin/pip3 install --upgrade pip
    .venv/bin/pip3 install uv
    .venv/bin/pip3 install molecule-plugins[podman,vagrant]
    test -f pyproject.toml || .venv/bin/uv init
    .venv/bin/uv add molecule
    .venv/bin/uv add ansible
    .venv/bin/uv add ansible-lint
    .venv/bin/uv add github3.py
    git clone https://github.com/borgbase/ansible-role-borgbackup \
        roles/ansible-role-borgbackup
    rm -rf roles/ansible-role-borgbackup/.git

# Create a new ansible role
create-role role_name:
    mkdir -p "roles/{{ role_name }}/files"
    mkdir -p "roles/{{ role_name }}/tasks"
    mkdir -p "roles/{{ role_name }}/templates"
    touch "roles/{{ role_name }}/tasks/main.yml"

# Create config for a new tool
create-config config_name:
    touch "roles/user_config/tasks/{{ config_name }}.yml"
    mkdir -p "roles/user_config/files/{{ config_name }}"
    mkdir -p "roles/user_config/templates/{{ config_name }}"
