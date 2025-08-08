#!/usr/bin/env python3
"""
Log cleanup script for Simulate to Survive
"""

import os
import shutil
from pathlib import Path
import argparse

def clean_logs(keep_recent=0):
    """Clean log files"""
    logs_dir = Path("logs")
    
    if not logs_dir.exists():
        print("📁 日志文件夹不存在")
        return
    
    log_files = list(logs_dir.glob("*.log"))
    
    if not log_files:
        print("📁 日志文件夹为空")
        return
    
    print(f"📁 找到 {len(log_files)} 个日志文件")
    
    # Sort by modification time (newest first)
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    if keep_recent > 0:
        # Keep the most recent files
        files_to_delete = log_files[keep_recent:]
        files_to_keep = log_files[:keep_recent]
        
        print(f"🗑️ 将删除 {len(files_to_delete)} 个旧日志文件")
        print(f"💾 保留 {len(files_to_keep)} 个最新日志文件")
        
        for log_file in files_to_delete:
            try:
                log_file.unlink()
                print(f"   ✓ 删除: {log_file.name}")
            except Exception as e:
                print(f"   ❌ 删除失败 {log_file.name}: {e}")
    else:
        # Delete all log files
        print(f"🗑️ 删除所有 {len(log_files)} 个日志文件")
        
        for log_file in log_files:
            try:
                log_file.unlink()
                print(f"   ✓ 删除: {log_file.name}")
            except Exception as e:
                print(f"   ❌ 删除失败 {log_file.name}: {e}")
    
    print("✅ 日志清理完成")

def list_logs():
    """List all log files"""
    logs_dir = Path("logs")
    
    if not logs_dir.exists():
        print("📁 日志文件夹不存在")
        return
    
    log_files = list(logs_dir.glob("*.log"))
    
    if not log_files:
        print("📁 日志文件夹为空")
        return
    
    print(f"📁 日志文件夹中有 {len(log_files)} 个文件:")
    
    # Sort by modification time (newest first)
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, log_file in enumerate(log_files, 1):
        size = log_file.stat().st_size
        mtime = log_file.stat().st_mtime
        from datetime import datetime
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"   {i}. {log_file.name} ({size} bytes, {mtime_str})")

def main():
    parser = argparse.ArgumentParser(description="日志管理工具")
    parser.add_argument("action", choices=["clean", "list"], help="操作类型")
    parser.add_argument("--keep", type=int, default=0, help="保留最新的N个日志文件")
    
    args = parser.parse_args()
    
    if args.action == "clean":
        clean_logs(args.keep)
    elif args.action == "list":
        list_logs()

if __name__ == "__main__":
    main()
