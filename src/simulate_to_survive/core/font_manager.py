#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体管理器 - 自动选择最佳的中文字体
"""

import pygame
from typing import Optional, Tuple

class FontManager:
    """字体管理器"""
    
    def __init__(self):
        self._cached_fonts = {}
        self._best_chinese_font = None
        # 延迟初始化，等待pygame初始化完成
    
    def initialize(self):
        """初始化字体系统（在pygame初始化后调用）"""
        if not self._best_chinese_font:
            self._initialize_fonts()
    
    def _initialize_fonts(self):
        """初始化字体系统"""
        # 中文字体优先级列表
        chinese_fonts = [
            'hiraginosansgb',      # macOS 最佳中文字体
            'pingfangsc',          # macOS 苹方字体
            'stheitimedium',       # macOS 华文黑体
            'arialunicode',        # Arial Unicode MS
            'notosanscjksc',       # Google Noto Sans CJK 简体中文
            'notosanscjk',         # Google Noto Sans CJK
            'sourcehansanscn',     # Source Han Sans 简体中文
            'simsun',              # Windows 宋体
            'simhei',              # Windows 黑体
            'microsoftyahei'       # Windows 微软雅黑
        ]
        
        # 测试并选择最佳中文字体
        for font_name in chinese_fonts:
            try:
                test_font = pygame.font.SysFont(font_name, 24)
                # 测试中文字符渲染
                test_surface = test_font.render("测试", True, (255, 255, 255))
                # 检查渲染结果
                width, height = test_surface.get_size()
                if width > 10 and height > 10:  # 确保字体正常渲染
                    self._best_chinese_font = font_name
                    print(f"✅ 选择中文字体: {font_name}")
                    break
                else:
                    print(f"⚠️  字体 {font_name} 渲染尺寸异常: {width}x{height}")
            except Exception as e:
                print(f"❌ 字体 {font_name} 测试失败: {e}")
                continue
        
        if not self._best_chinese_font:
            print("⚠️  未找到合适的中文字体，使用默认字体")
            self._best_chinese_font = None
    
    def get_font(self, size: int) -> pygame.font.Font:
        """获取指定大小的字体"""
        cache_key = f"{self._best_chinese_font}_{size}"
        
        if cache_key in self._cached_fonts:
            return self._cached_fonts[cache_key]
        
        try:
            if self._best_chinese_font:
                font = pygame.font.SysFont(self._best_chinese_font, size)
            else:
                font = pygame.font.Font(None, size)
            
            self._cached_fonts[cache_key] = font
            return font
        except:
            # 回退到默认字体
            font = pygame.font.Font(None, size)
            self._cached_fonts[cache_key] = font
            return font
    
    def get_small_font(self) -> pygame.font.Font:
        """获取小字体"""
        return self.get_font(24)
    
    def get_normal_font(self) -> pygame.font.Font:
        """获取正常字体"""
        return self.get_font(32)
    
    def get_large_font(self) -> pygame.font.Font:
        """获取大字体"""
        return self.get_font(48)
    
    def test_chinese_rendering(self, text: str, size: int = 32) -> Tuple[bool, Optional[pygame.Surface]]:
        """测试中文字符渲染"""
        try:
            font = self.get_font(size)
            surface = font.render(text, True, (255, 255, 255))
            return True, surface
        except Exception as e:
            print(f"❌ 中文字符渲染失败: {e}")
            return False, None

# 全局字体管理器实例
font_manager = FontManager()
