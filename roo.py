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

# Save original working directory before any chdir
ORIGINAL_CWD = os.getcwd()

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
    
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, ORIGINAL_CWD, 1)
    
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
    """Ensure a given relative path is in .gitignore under '# Roo Modules'."""
    gitignore_path = Path(".gitignore")
    path_to_ignore = path_rel.replace('\\', '/')
    header = "# Roo Modules"
    
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

def create_symlink(src_str, dst_str, is_elevated=False, is_update=False):
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
        
        # If we are just updating existing submodules, skip config generation entirely
        if is_update:
            return
            
        # Save to .roomodules using forward slashes (git style)
        config = load_modules()
        
        # Store metadata
        # Key is destination path (relative to repo root if possible)
        # We'll normalize to forward slash relative paths
        try:
            repo_root = get_git_root()
            dst_rel = dest_path.relative_to(repo_root).as_posix()
        except ValueError:
            dst_rel = dest_path.as_posix()
            
        # Determine if source should be absolute or relative in the URL
        original_src_path = Path(src_str)
        if original_src_path.is_absolute():
            # If they provided an absolute path, store it absolute
            src_url_path = source_path.as_posix()
            # Absolute file URI format varies slightly, we'll prefix it if it doesn't start with / (like on windows C:/)
            if not src_url_path.startswith('/'):
                src_url_path = '/' + src_url_path
        else:
            # If they provided a relative path, calculate it relative to repo root
            try:
                src_url_path = source_path.relative_to(repo_root).as_posix()
            except ValueError:
                # If it's a relative path that escapes the repo (like ../../outside_repo)
                # Calculate relative path from repo root manually
                src_url_path = os.path.relpath(source_path, repo_root).replace('\\', '/')
            
        # Ensure the destination symlink is ignored by Git
        ensure_ignored(dst_rel)
            
        section_name = f'submodule "{dst_rel}"'
        if not config.has_section(section_name):
            config.add_section(section_name)
            
        config.set(section_name, 'path', dst_rel)
        
        # Use file:/// format. If src_url_path is relative (e.g. docs/api), it becomes file:///docs/api
        # If absolute on windows (e.g. /C:/docs), it becomes file:///C:/docs
        # If relative outside repo (e.g. ../docs), it becomes file:///../docs
        # Ensure directories end with / to make inference robust
        if is_dir and not src_url_path.endswith('/'):
            src_url_path += '/'
            
        if src_url_path.startswith('/'):
            config.set(section_name, 'url', f"file://{src_url_path}")
        else:
            config.set(section_name, 'url', f"file:///{src_url_path}")
        
        # Explicitly omit type and let update command dynamically resolve it based on extension
        
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
        if re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)", src):
            download_github_folder(src, dst)
            
            # Save remote metadata
            config = load_modules()
            try:
                repo_root = get_git_root()
                dst_rel = Path(dst).resolve().relative_to(repo_root).as_posix()
            except ValueError:
                dst_rel = Path(dst).resolve().as_posix()
                
            # Ensure the destination folder is ignored by Git
            ensure_ignored(dst_rel)
                
            section_name = f'submodule "{dst_rel}"'
            if not config.has_section(section_name):
                config.add_section(section_name)
                
            config.set(section_name, 'path', dst_rel)
            config.set(section_name, 'url', src)
            
            save_modules(config)
        else:
            logger.info(f"Adding full repository as git submodule: {src} -> {dst}")
            try:
                subprocess.run(["git", "submodule", "add", "--force", src, dst], check=True)
                logger.info(f"Successfully added git submodule: {dst}")
                
                # Save remote metadata to .roomodules as well
                config = load_modules()
                try:
                    repo_root = get_git_root()
                    dst_rel = Path(dst).resolve().relative_to(repo_root).as_posix()
                except ValueError:
                    dst_rel = Path(dst).resolve().as_posix()
                    
                section_name = f'submodule "{dst_rel}"'
                if not config.has_section(section_name):
                    config.add_section(section_name)
                    
                config.set(section_name, 'path', dst_rel)
                config.set(section_name, 'url', src)
                
                save_modules(config)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to add git submodule: {e}")
                sys.exit(1)
    else:
        create_symlink(src, dst, is_elevated)

def handle_submodule_update(is_elevated):
    config = load_modules()
    if not config.sections():
        logger.info("No .roomodules found or file is empty.")
        return
        
    logger.info(f"Updating submodules from {ROOMODULES_FILE}...")
    repo_root = get_git_root()
    
    for section in config.sections():
        if not section.startswith('submodule "'):
            continue
            
        dst_rel = config.get(section, 'path', fallback=None)
        if not dst_rel:
            logger.warning(f"Skipping {section}: No path specified")
            continue
            
        source_url = config.get(section, 'url', fallback=None)
        if not source_url:
            logger.warning(f"Skipping {section}: No url specified")
            continue
            
        if is_github_url(source_url):
            if re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)", source_url):
                logger.info(f"Processing remote folder: {dst_rel}")
                download_github_folder(source_url, dst_rel)
            else:
                logger.info(f"Processing full git submodule: {dst_rel}")
                try:
                    subprocess.run(["git", "submodule", "update", "--init", "--recursive", dst_rel], check=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to update git submodule {dst_rel}: {e}")
        elif source_url.startswith("file://"):
            # Local symlink using the file:// prefix
            # Parse whether it is an absolute URI (file:///C:/... or file:////home/...) 
            # or relative URI (file:///docs/... or file:///../docs/...)
            
            # Remove file:// prefix
            src_uri_path = source_url[len("file://"):]
            
            # If it starts with a slash, it might be an absolute path (on Mac/Linux /home/... or Windows /C:/...)
            # or it might be a relative path attached to file:/// like file:///../docs
            # Let's cleanly separate the 3rd slash
            if src_uri_path.startswith('/'):
                src_uri_path = src_uri_path[1:]
                
            # Check if it's an absolute path on Windows (e.g., C:/...) or absolute on Unix (starts with / after the first 3 slashes)
            if re.match(r"^[A-Za-z]:/", src_uri_path) or src_uri_path.startswith('/'):
                src_path = Path(src_uri_path)
            else:
                # It's a relative path, so resolve it relative to repo_root
                src_path = repo_root / src_uri_path
                
            dst_path = repo_root / dst_rel
            
            # Try to infer it based on file extension
            is_dir = not dst_rel.split('/')[-1].count('.') > 0
            
            logger.info(f"Processing local symlink: {dst_rel} -> {src_path}")
            create_symlink(str(src_path), str(dst_path), is_elevated, is_update=True)
        else:
            logger.warning(f"Skipping {section}: Unrecognized url format '{source_url}'")
            
    logger.info("Submodule update complete.")

def get_git_root():
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError:
        logger.error("Error: Not inside a git repository.")
        sys.exit(1)
    except FileNotFoundError:
        logger.error("Error: git command not found.")
        sys.exit(1)

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
        original_cwd = Path.cwd()
        git_root = get_git_root()
        os.chdir(git_root)
        logger.info(f"Operating from git repository root: {git_root}")

        if args.action == "add":
            src = args.src
            dst = args.dst
            
            if not is_github_url(src):
                src_path = Path(src)
                if not src_path.is_absolute():
                    src_abs = (original_cwd / src).resolve()
                    try:
                        src = os.path.relpath(src_abs, git_root).replace('\\', '/')
                    except ValueError:
                        src = str(src_abs).replace('\\', '/')
                        
            dst_path = Path(dst)
            if not dst_path.is_absolute():
                dst_abs = (original_cwd / dst).resolve()
                try:
                    dst = os.path.relpath(dst_abs, git_root).replace('\\', '/')
                except ValueError:
                    dst = str(dst_abs).replace('\\', '/')

            handle_add(src, dst, is_elevated)
        elif args.action == "update":
            handle_submodule_update(is_elevated)
        
    if is_elevated:
        logger.info("(Window will close automatically)")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

