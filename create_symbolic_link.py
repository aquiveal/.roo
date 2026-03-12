#!/usr/bin/env python3
import os
import sys
import platform
import ctypes
import subprocess
from pathlib import Path

def is_admin():
    if platform.system() != "Windows":
        return True
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def configure_git_symlinks(directory_path, enable=False):
    action_str = "true" if enable else "false"
    status_msg = "track" if enable else "ignore"
    print(f"⚙️ Configuring Git to {status_msg} local symlink changes (core.symlinks={action_str})...")
    try:
        # Run git config inside the specified directory to apply it to the repo
        subprocess.run(
            ["git", "config", "core.symlinks", action_str],
            cwd=directory_path,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"   ✅ Git configured successfully. Symlink updates will now be {status_msg}ed.\n")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Could not configure Git (is this a git repository?): {e}\n")
    except FileNotFoundError:
        print("   ⚠️ Git executable not found. Skipping Git configuration.\n")

def elevate_and_run(src, dst):
    print("🛡️  Requesting Administrator privileges to create symlink...")
    # sys.executable is the python interpreter, sys.argv[0] is the script path
    script_path = os.path.abspath(sys.argv[0])
    
    # We pass the src and dst as arguments, and a special flag '--elevated' to pause at the end
    params = f'"{script_path}" "{src}" "{dst}" --elevated'
    
    # ShellExecuteW(hwnd, verb, file, parameters, directory, showcmd)
    # showcmd=1 is SW_SHOWNORMAL
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    
    if int(ret) > 32:
        print("✅ Elevation requested successfully. Please check the new Administrator window.")
        sys.exit(0)
    else:
        print(f"❌ Failed to elevate privileges. Error code: {ret}")
        sys.exit(1)

def create_symlink(source_str, dest_str, is_elevated=False):
    # Convert inputs to Path objects
    source_path = Path(source_str).resolve()
    dest_path = Path(dest_str).absolute()

    if not source_path.exists():
        print(f"❌ Error: Source path '{source_str}' does not exist.")
        sys.exit(1)

    # Automatically create the destination folders if they don't exist
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure Git to ALLOW tracking so you can commit the new symlink
    configure_git_symlinks(dest_path.parent, enable=True)

    # Remove existing file/symlink if it's already there
    if dest_path.exists() or dest_path.is_symlink():
        print(f"⚠️  Destination '{dest_str}' already exists. Overwriting...")
        dest_path.unlink()

    # Calculate the exact relative path from the DESTINATION back to the SOURCE
    # This prevents you from having to guess how many "../../" to use!
    relative_target = os.path.relpath(source_path, dest_path.parent)

    # FORCE forward slashes (/) for the initial creation to make it Git-compatible
    # This ensures Mac/Linux users get the right path when they clone
    git_relative_target = relative_target.replace('\\', '/')

    is_dir = source_path.is_dir()

    try:
        # Create the symlink (with forward slashes for Git)
        os.symlink(git_relative_target, dest_path, target_is_directory=is_dir)
        print(f"✅ Success! Git-compatible symlink created:")
        print(f"   {dest_str}  ->  {git_relative_target}")
        
        # If on Windows, we immediately need to fix it locally so it works for the developer right now,
        # but we do NOT track the fix in Git, so we tell Git to ignore changes to this specific file.
        if platform.system() == "Windows":
            print("🔄 Fixing Windows local symlink and telling Git to ignore local path separator changes...")
            # Unlink and recreate with backslashes
            dest_path.unlink()
            windows_target = relative_target.replace('/', '\\')
            os.symlink(windows_target, dest_path, target_is_directory=is_dir)
            
            # Tell Git to ignore future changes to this specific symlink file
            # This allows the forward-slash version to stay in the repository index
            try:
                subprocess.run(
                    ["git", "update-index", "--skip-worktree", dest_path.name],
                    cwd=dest_path.parent,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError:
                pass
            print(f"   ✅ Local Windows symlink active: {dest_path.name} -> {windows_target}")
            
    except OSError as e:
        # WinError 1314 is ERROR_PRIVILEGE_NOT_HELD
        if platform.system() == "Windows" and getattr(e, "winerror", None) == 1314:
            if is_elevated or is_admin():
                # We are already elevated or admin, but still failed
                print(f"❌ Failed to create symlink even with elevated privileges: {e}")
            else:
                print(f"⚠️  Privilege error detected: {e}")
                elevate_and_run(source_str, dest_str)
                return
        else:
            print(f"❌ Failed to create symlink: {e}")
            
        if platform.system() == "Windows":
            print("\n🔧 WINDOWS FIX REQUIRED:")
            print("   You must enable 'Developer Mode' in Windows Settings")
            print("   OR run your terminal as Administrator to create symlinks.")

def scan_symlinks(directory):
    directory_path = Path(directory).resolve()
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"❌ Error: Directory '{directory}' does not exist or is not a directory.")
        sys.exit(1)
        
    print(f"🔍 Scanning for symbolic links in: {directory_path}\n")
    
    # Configure git so our path separator fixes aren't tracked
    configure_git_symlinks(directory_path)
    
    found_links = False
    
    for path in directory_path.rglob('*'):
        if path.is_symlink():
            found_links = True
            target = os.readlink(path)
            
            # Recreate the symlink to fix path separators for the current OS
            is_dir = path.is_dir()
            
            # Use OS-specific path separators for the target
            if platform.system() == "Windows":
                fixed_target = target.replace('/', '\\')
            else:
                fixed_target = target.replace('\\', '/')
                
            if target != fixed_target:
                print(f"🔄 Fixing symlink for current OS:")
                print(f"   Link:   {path}")
                print(f"   Old:    {target}")
                print(f"   New:    {fixed_target}")
                
                try:
                    path.unlink()
                    os.symlink(fixed_target, path, target_is_directory=is_dir)
                    print(f"   ✅ Fixed successfully.\n")
                except OSError as e:
                    print(f"   ❌ Failed to fix: {e}\n")
            else:
                print(f"✅ Found symlink (OS format matches):")
                print(f"   Link:   {path}")
                print(f"   Target: {target}\n")
                
    if not found_links:
        print("ℹ️ No symbolic links found in this directory.")

if __name__ == "__main__":
    print("🔗 Cross-Platform Git Symlink Creator & Scanner\n")
    
    # Check if arguments were passed via command line
    # --elevated is used internally when relaunching
    is_elevated = "--elevated" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--elevated"]
    
    if len(args) == 1:
        # One argument: Scan directory
        scan_symlinks(args[0])
    elif len(args) == 2:
        # Two arguments: Create symlink
        src = args[0]
        dst = args[1]
        create_symlink(src, dst, is_elevated)
    else:
        # If no valid arguments, ask the user interactively what to do
        print("Choose an action:")
        print("1. Scan directory for symlinks (and fix path separators)")
        print("2. Create a new symlink")
        choice = input("> ").strip()
        
        if choice == "1":
            directory = input("📁 Enter directory to scan:\n> ").strip()
            if directory:
                scan_symlinks(directory)
            else:
                print("❌ Directory is required.")
        elif choice == "2":
            src = input("📁 Enter source path (e.g., roo-library/1-languages/typescript):\n> ").strip()
            dst = input("🎯 Enter destination (e.g., .roo/rules-code-node/10-typescript):\n> ").strip()
            if not src or not dst:
                print("❌ Both source and destination are required.")
                if is_elevated:
                    input("\nPress Enter to exit...")
                sys.exit(1)
            create_symlink(src, dst, is_elevated)
        else:
            print("❌ Invalid choice.")
            sys.exit(1)
            
    if is_elevated:
        print("\n(Window will close automatically)")
        input("Press Enter to exit...")