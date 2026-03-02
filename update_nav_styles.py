#!/usr/bin/env python3
import os
import glob
import re

# 定义新的样式(针对nav目录的简化版本)
NEW_STYLE = '''        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #2563eb; --primary-hover: #1d4ed8; --primary-bg: #dbeafe;
            --accent: #0891b2; --accent-bg: #cffafe;
            --secondary: #8b5cf6; --secondary-bg: #ede9fe;
            --success: #16a34a; --success-bg: #dcfce7;
            --warning: #d97706; --warning-bg: #fef3c7;
            --danger: #dc2626; --danger-bg: #fee2e2;
            --bg: #f8fafc; --bg-white: #ffffff;
            --text: #1e293b; --text-secondary: #475569; --text-muted: #64748b;
            --border: #e2e8f0;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.8; }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
        .page-header { text-align: center; padding: 60px 40px; background: var(--gradient-primary); margin: -40px -20px 48px; border-radius: 24px; box-shadow: var(--shadow-xl), var(--shadow-glow); position: relative; overflow: hidden; }
        .page-header::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: rotate 20s linear infinite; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .page-header h1 { font-size: 3rem; font-weight: 800; color: white; margin-bottom: 16px; text-shadow: 0 2px 10px rgba(0,0,0,0.2); position: relative; animation: fadeInUp 0.8s ease; }
        .page-header p { font-size: 1.2rem; color: rgba(255,255,255,0.9); max-width: 700px; margin: 0 auto; position: relative; animation: fadeInUp 0.8s ease 0.2s both; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 28px; }
        .card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 32px; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; box-shadow: var(--shadow-md); position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--gradient-primary); transform: scaleX(0); transition: transform 0.4s ease; }
        .card:hover { border-color: var(--primary); box-shadow: var(--shadow-xl), var(--shadow-glow); transform: translateY(-8px) scale(1.02); }
        .card:hover::before { transform: scaleX(1); }
        .card-icon { font-size: 2.5rem; margin-bottom: 16px; }
        .card h3 { font-size: 1.3rem; font-weight: 700; color: var(--text); margin-bottom: 12px; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card p { color: var(--text-secondary); font-size: 0.95rem; line-height: 1.7; margin-bottom: 16px; }
        .card-meta { display: flex; gap: 12px; flex-wrap: wrap; }
        .badge { display: inline-block; padding: 4px 12px; background: var(--primary-bg); color: var(--primary); border-radius: 16px; font-size: 0.8rem; font-weight: 600; box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2); }
        
        .back-link { display: inline-flex; align-items: center; gap: 8px; color: var(--text-secondary); text-decoration: none; font-weight: 500; transition: all 0.3s ease; padding: 12px 20px; background: rgba(255,255,255,0.8); border-radius: 12px; box-shadow: var(--shadow-sm); }
        .back-link:hover { color: var(--primary); transform: translateX(-4px); box-shadow: var(--shadow-md); }

        @media (max-width: 768px) {
            .container { padding: 24px 16px; }
            .page-header { margin: -24px -16px 32px; padding: 40px 24px; }
            .page-header h1 { font-size: 2rem; }
            .page-header p { font-size: 1rem; }
            .grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
            .card { padding: 24px; }
        }

        @media (max-width: 480px) {
            .page-header h1 { font-size: 1.6rem; }
            .grid { grid-template-columns: 1fr; }
        }'''

def update_html_file(file_path):
    """更新单个HTML文件的样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找<style>标签内的内容
        style_pattern = r'(<style>)(.*?)(</style>)'
        match = re.search(style_pattern, content, re.DOTALL)
        
        if match:
            # 替换style标签内的内容
            new_content = re.sub(style_pattern, f'<style>\n        {NEW_STYLE}\n    </style>', content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f'✓ 已更新: {file_path}')
            return True
        else:
            print(f'✗ 未找到style标签: {file_path}')
            return False
    except Exception as e:
        print(f'✗ 错误处理 {file_path}: {str(e)}')
        return False

def main():
    # 获取当前目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 更新nav目录下的所有HTML文件
    nav_dir = os.path.join(base_dir, 'nav')
    html_files = glob.glob(os.path.join(nav_dir, '*.html'))
    
    print(f'找到 {len(html_files)} 个HTML文件在 nav 目录\n')
    
    updated_count = 0
    for html_file in html_files:
        if update_html_file(html_file):
            updated_count += 1
    
    print(f'\n完成! 共更新 {updated_count}/{len(html_files)} 个文件')

if __name__ == '__main__':
    main()