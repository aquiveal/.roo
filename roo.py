#!/usr/bin/env python3
import os
import sys
import platform
import configparser
import ctypes
import logging
import re
import subprocess
import shutil
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

ROOMODULES_FILE = ".roomodules"

def is_admin():
    if platform.system() != "Windows":
        return True
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_and_run(args):
    logger.info("Requesting Administrator privileges...")
    script_path = os.path.abspath(sys.argv[0])
    
    # Reconstruct arguments but add --elevated
    params = f'"{script_path}" ' + " ".join([f'"{arg}"' for arg in args]) + ' --elevated'
    
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    
    if int(ret) > 32:
        logger.info("Elevation requested successfully. Please check the new Administrator window.")
        sys.exit(0)
    else:
        logger.error(f"Failed to elevate privileges. Error code: {ret}")
        sys.exit(1)

def load_modules():
    config = configparser.ConfigParser()
    if not os.path.exists(ROOMODULES_FILE):
        return config
    try:
        config.read(ROOMODULES_FILE)
        return config
    except Exception as e:
        logger.error(f"Error reading {ROOMODULES_FILE}: {e}")
        return config

def save_modules(config):
    with open(ROOMODULES_FILE, 'w') as f:
        # Use tabs for indentation to match git config style
        for section in config.sections():
            f.write(f'[{section}]\n')
            for key, value in config.items(section):
                f.write(f'\t{key} = {value}\n')
    logger.info(f"Updated {ROOMODULES_FILE}")

def ensure_ignored(path_rel):
    """Ensure a given relative path is in .gitignore under '# Roo Code Modules'."""
    gitignore_path = Path(".gitignore")
    path_to_ignore = path_rel.replace('\\', '/')
    header = "# Roo Code Modules"
    
    lines = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            lines = f.readlines()
            
    # Check if already ignored anywhere
    for line in lines:
        if line.strip() == path_to_ignore:
            return # Already ignored
            
    logger.info(f"Adding '{path_to_ignore}' to .gitignore")
    
    header_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == header:
            header_idx = i
            break
            
    if header_idx != -1:
        # Header exists, insert right after it
        lines.insert(header_idx + 1, f"{path_to_ignore}\n")
    else:
        # Header doesn't exist, append it and the path to the end
        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        if lines:
            lines.append('\n')
        lines.append(f"{header}\n")
        lines.append(f"{path_to_ignore}\n")
        
    with open(gitignore_path, 'w') as f:
        f.writelines(lines)

def create_symlink(src_str, dst_str, is_elevated=False):
    source_path = Path(src_str).resolve()
    dest_path = Path(dst_str).absolute()

    if not source_path.exists():
        logger.error(f"Error: Source path '{src_str}' does not exist.")
        sys.exit(1)

    # Ensure destination parent directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists() or dest_path.is_symlink():
        logger.warning(f"Destination '{dst_str}' already exists. Overwriting...")
        dest_path.unlink()

    # Calculate exact relative path from DEST to SRC
    relative_target = os.path.relpath(source_path, dest_path.parent)

    # Use OS-specific path separators for local symlink
    if platform.system() == "Windows":
        local_target = relative_target.replace('/', '\\')
    else:
        local_target = relative_target.replace('\\', '/')

    is_dir = source_path.is_dir()

    try:
        os.symlink(local_target, dest_path, target_is_directory=is_dir)
        logger.info(f"Created local OS-specific symlink: {dst_str} -> {local_target}")
        
        # Save to .roomodules using forward slashes (git style)
        git_target = relative_target.replace('\\', '/')
        config = load_modules()
        
        # Store metadata
        # Key is destination path (relative to repo root if possible)
        # We'll normalize to forward slash relative paths
        try:
            repo_root = Path.cwd()
            dst_rel = dest_path.relative_to(repo_root).as_posix()
            src_rel = source_path.relative_to(repo_root).as_posix()
        except ValueError:
            # Fallback if paths are outside cwd
            dst_rel = dest_path.as_posix()
            src_rel = source_path.as_posix()
            
        # Ensure the destination symlink is ignored by Git
        ensure_ignored(dst_rel)
            
        section_name = f'submodule "{dst_rel}"'
        if not config.has_section(section_name):
            config.add_section(section_name)
            
        config.set(section_name, 'path', dst_rel)
        config.set(section_name, 'source', src_rel)
        config.set(section_name, 'relative_target', git_target)
        config.set(section_name, 'type', "directory" if is_dir else "file")
        
        save_modules(config)
        
    except OSError as e:
        if platform.system() == "Windows" and getattr(e, "winerror", None) == 1314:
            if is_elevated or is_admin():
                logger.error(f"Failed to create symlink even with elevated privileges: {e}")
            else:
                logger.warning(f"Privilege error detected: {e}")
                # Pass sys.argv[1:] excluding --elevated if it was there
                original_args = [arg for arg in sys.argv[1:] if arg != "--elevated"]
                elevate_and_run(original_args)
                return
        else:
            logger.error(f"Failed to create symlink: {e}")

def is_github_url(url):
    return url.startswith("https://github.com/") or url.startswith("http://github.com/")

def download_github_folder(url, dest_str):
    dest_path = Path(dest_str).resolve()
    
    # Parse the GitHub URL: https://github.com/owner/repo/tree/branch/path/to/folder
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)", url)
    if not match:
        logger.error(f"Invalid GitHub folder URL format: {url}")
        logger.error("Expected format: https://github.com/owner/repo/tree/branch/path/to/folder")
        sys.exit(1)
        
    owner, repo, branch, folder_path = match.groups()
    repo_url = f"https://github.com/{owner}/{repo}.git"
    
    logger.info(f"Downloading from {repo_url} (branch: {branch}, folder: {folder_path})")
    
    # We will use git sparse-checkout to download just the specific folder
    # Create a temporary directory in the current working directory
    tmp_dir = Path.cwd() / f".tmp_{repo}_{branch}"
    
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
        
    try:
        # Initialize a new git repo
        subprocess.run(["git", "clone", "--no-checkout", "--depth", "1", "--branch", branch, repo_url, str(tmp_dir)], check=True, capture_output=True)
        
        # Configure sparse-checkout
        subprocess.run(["git", "sparse-checkout", "init", "--cone"], cwd=str(tmp_dir), check=True, capture_output=True)
        subprocess.run(["git", "sparse-checkout", "set", folder_path], cwd=str(tmp_dir), check=True, capture_output=True)
        
        # Checkout the files
        subprocess.run(["git", "checkout"], cwd=str(tmp_dir), check=True, capture_output=True)
        
        # Move the downloaded folder to the final destination
        source_folder = tmp_dir / folder_path
        
        if not source_folder.exists():
            logger.error(f"Folder '{folder_path}' not found in repository.")
            shutil.rmtree(tmp_dir)
            sys.exit(1)
            
        # Ensure parent of destination exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove destination if it exists
        if dest_path.exists():
            if dest_path.is_dir() and not dest_path.is_symlink():
                shutil.rmtree(dest_path)
            else:
                dest_path.unlink()
                
        # Move it
        shutil.move(str(source_folder), str(dest_path))
        logger.info(f"Successfully downloaded to {dest_str}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        if e.stderr:
            logger.error(e.stderr.decode('utf-8'))
        sys.exit(1)
    finally:
        # Cleanup temp dir
        if tmp_dir.exists():
            # on windows sometimes git processes hold onto pack files briefly
            try:
                # we need to remove .git dir carefully on windows
                def handle_remove_readonly(func, path, exc_info):
                    import stat
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                shutil.rmtree(tmp_dir, onerror=handle_remove_readonly)
            except Exception as e:
                logger.warning(f"Could not fully clean up temporary directory {tmp_dir}: {e}")

def handle_add(src, dst, is_elevated):
    if not src or not dst:
        logger.error("Both source and destination paths are required for 'submodule add'")
        sys.exit(1)
        
    if is_github_url(src):
        download_github_folder(src, dst)
        
        # Save remote metadata
        config = load_modules()
        try:
            repo_root = Path.cwd()
            dst_rel = Path(dst).resolve().relative_to(repo_root).as_posix()
        except ValueError:
            dst_rel = Path(dst).resolve().as_posix()
            
        # Ensure the destination folder is ignored by Git
        ensure_ignored(dst_rel)
            
        # extract submodule name, default to the last part of destination
        submodule_name = dst_rel.split('/')[-1] if '/' in dst_rel else dst_rel
            
        section_name = f'submodule "{submodule_name}"'
        if not config.has_section(section_name):
            config.add_section(section_name)
            
        config.set(section_name, 'path', dst_rel)
        config.set(section_name, 'url', src)
        config.set(section_name, 'type', 'remote_folder')
        
        save_modules(config)
    else:
        create_symlink(src, dst, is_elevated)

def handle_submodule_update(is_elevated):
    config = load_modules()
    if not config.sections():
        logger.info("No .roomodules found or file is empty.")
        return
        
    logger.info(f"Updating submodules from {ROOMODULES_FILE}...")
    repo_root = Path.cwd()
    
    for section in config.sections():
        if not section.startswith('submodule "'):
            continue
            
        dst_rel = config.get(section, 'path', fallback=None)
        if not dst_rel:
            logger.warning(f"Skipping {section}: No path specified")
            continue
            
        module_type = config.get(section, 'type', fallback=None)
        
        if module_type == "remote_folder" or config.has_option(section, 'url'):
            source_url = config.get(section, 'url', fallback=None)
            if not source_url:
                logger.warning(f"Skipping {section}: No url specified")
                continue
            
            logger.info(f"Processing remote folder: {dst_rel}")
            download_github_folder(source_url, dst_rel)
            continue
            
        src_rel = config.get(section, 'source', fallback=None)
        if not src_rel:
            logger.warning(f"Skipping {section}: No source specified for local symlink")
            continue
            
        src_path = repo_root / src_rel
        dst_path = repo_root / dst_rel
        
        logger.info(f"Processing local symlink: {dst_rel}")
        create_symlink(str(src_path), str(dst_path), is_elevated)
    
    logger.info("Submodule update complete.")

def main():
    is_elevated = "--elevated" in sys.argv
    if is_elevated:
        sys.argv.remove("--elevated")
        
    parser = argparse.ArgumentParser(description="roo module manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'submodule' command
    submodule_parser = subparsers.add_parser("submodule")
    submodule_subparsers = submodule_parser.add_subparsers(dest="action", required=True)
    
    # 'submodule update'
    update_parser = submodule_subparsers.add_parser("update", help="Update all submodules from .roomodules")
    
    # 'submodule add'
    add_parser = submodule_subparsers.add_parser("add", help="Add a new submodule")
    add_parser.add_argument("src", help="Source path or GitHub URL")
    add_parser.add_argument("dst", help="Destination path")

    args = parser.parse_args()

    if args.command == "submodule":
        if args.action == "add":
            handle_add(args.src, args.dst, is_elevated)
        elif args.action == "update":
            handle_submodule_update(is_elevated)
        
    if is_elevated:
        logger.info("(Window will close automatically)")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
