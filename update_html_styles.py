#!/usr/bin/env python3
import os
import glob
import re

# 定义新的样式
NEW_STYLE = '''        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #2563eb; --primary-hover: #1d4ed8; --primary-bg: #dbeafe;
            --accent: #0891b2; --accent-bg: #cffafe;
            --secondary: #8b5cf6; --secondary-bg: #ede9fe;
            --secondary-tag: #db2777; --secondary-tag-bg: #fce7f3;
            --success: #16a34a; --success-bg: #dcfce7;
            --warning: #d97706; --warning-bg: #fef3c7;
            --danger: #dc2626; --danger-bg: #fee2e2;
            --bg: #f8fafc; --bg-white: #ffffff;
            --text: #1e293b; --text-secondary: #475569; --text-muted: #64748b;
            --border: #e2e8f0; --code-bg: #1e293b; --code-text: #e2e8f0;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --gradient-warm: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.8; }
        .layout { display: flex; }
        aside { width: 280px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-right: 1px solid var(--border); padding: 24px 0; position: fixed; top: 0; left: 0; height: 100vh; overflow-y: auto; box-shadow: var(--shadow-xl); z-index: 100; transition: all 0.3s ease; }
        aside:hover { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
        aside h2 { font-size: 0.9rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; padding: 0 24px; margin-bottom: 16px; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav-tree { list-style: none; padding: 0 8px; }
        .nav-tree li { margin-bottom: 4px; }
        .nav-tree a { display: block; color: var(--text-secondary); text-decoration: none; padding: 12px 20px; font-size: 0.95rem; border-left: 3px solid transparent; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border-radius: 0 10px 10px 0; margin-right: 12px; font-weight: 500; }
        .nav-tree a:hover { background: linear-gradient(90deg, var(--primary-bg) 0%, rgba(219, 234, 254, 0.5) 100%); color: var(--primary); border-left-color: var(--primary); transform: translateX(6px); box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15); }
        .nav-tree .nav-category { font-size: 0.8rem; font-weight: 700; color: var(--text-muted); padding: 18px 20px 10px; text-transform: uppercase; letter-spacing: 0.1em; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; position: relative; }
        .nav-tree .nav-category::after { content: ''; position: absolute; bottom: 0; left: 20px; width: 40px; height: 2px; background: var(--gradient-primary); border-radius: 2px; }
        .nav-tree .nav-item { padding-left: 36px; font-size: 0.9rem; }
        .collapsible { cursor: pointer; position: relative; transition: all 0.3s ease; }
        .collapsible:hover { color: var(--primary); }
        .collapsible::after { content: '▼'; position: absolute; right: 20px; font-size: 0.65rem; color: var(--text-muted); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .collapsible.active::after { transform: rotate(180deg); color: var(--primary); }
        .collapsible-content { max-height: 0; overflow: hidden; transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
        .collapsible-content.show { max-height: 600px; }
        main { margin-left: 280px; padding: 32px 48px; min-height: 100vh; flex: 1; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }
        
        .page-header { text-align: center; padding: 48px 32px; background: var(--gradient-primary); margin: -32px -48px 40px; border-radius: 20px; box-shadow: var(--shadow-xl), var(--shadow-glow); position: relative; overflow: hidden; }
        .page-header::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: rotate 20s linear infinite; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .page-header h1 { font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 12px; text-shadow: 0 2px 10px rgba(0,0,0,0.2); position: relative; animation: fadeInUp 0.8s ease; }
        .page-header p { font-size: 1.1rem; color: rgba(255,255,255,0.9); max-width: 600px; margin: 0 auto; position: relative; animation: fadeInUp 0.8s ease 0.2s both; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

        .table-subsection { margin-bottom: 40px; padding: 28px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; box-shadow: var(--shadow-lg); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; }
        .table-subsection::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--gradient-primary); }
        .table-subsection:hover { box-shadow: var(--shadow-xl), var(--shadow-glow); transform: translateY(-4px); }
        .table-subsection h3 { font-size: 1.4rem; margin-bottom: 20px; color: var(--text); font-weight: 700; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .table-subsection h4 { font-size: 1.15rem; margin-bottom: 16px; color: var(--text-secondary); font-weight: 600; }
        
        table { width: 100%; border-collapse: collapse; margin-bottom: 24px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-md); }
        th, td { padding: 16px 20px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
        th { background: var(--gradient-primary); color: white; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }
        tbody tr { transition: all 0.3s ease; }
        tbody tr:hover { background: var(--primary-bg); transform: scale(1.01); }
        tbody tr:last-child td { border-bottom: none; }
        
        code { background: var(--code-bg); color: #fbbf24; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
        .code-block { background: var(--code-bg); color: var(--code-text); padding: 24px; border-radius: 16px; overflow-x: auto; margin-bottom: 24px; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; font-size: 0.9rem; line-height: 1.7; white-space: pre-wrap; word-break: break-all; box-shadow: var(--shadow-xl); border: 1px solid rgba(255,255,255,0.1); position: relative; }
        .code-block::before { content: 'CODE'; position: absolute; top: 0; right: 0; background: var(--gradient-primary); color: white; font-size: 0.7rem; font-weight: 700; padding: 6px 16px; border-radius: 0 16px 0 16px; letter-spacing: 0.05em; }
        .keyword { color: #c084fc; font-weight: 600; }
        .function { color: #60a5fa; font-weight: 600; }
        .string { color: #4ade80; }
        .comment { color: #6b7280; font-style: italic; }
        .number { color: #f97316; font-weight: 600; }
        .property { color: #f472b6; font-weight: 600; }
        .operator { color: #fb923c; }
        
        .main-content { max-width: 960px; margin: 0 auto; }
        .content-section { margin-bottom: 56px; padding-bottom: 40px; border-bottom: 2px solid var(--border); animation: fadeInUp 0.6s ease; }
        .content-section:last-child { border-bottom: none; }
        .content-section h2 { font-size: 1.9rem; margin-bottom: 28px; color: var(--text); font-weight: 700; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .content-section h3 { font-size: 1.5rem; margin-bottom: 20px; color: var(--text); font-weight: 600; }
        .content-section p { margin-bottom: 24px; color: var(--text-secondary); font-size: 1.05rem; line-height: 1.9; }
        .content-section ul, .content-section ol { margin-bottom: 24px; padding-left: 32px; }
        .content-section li { margin-bottom: 14px; color: var(--text-secondary); }
        .content-section ul li::marker { color: var(--primary); }
        
        .example-box { background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(37, 99, 235, 0.1) 100%); border-left: 5px solid var(--primary); padding: 24px 28px; margin: 28px 0; border-radius: 16px; box-shadow: var(--shadow-md); transition: all 0.3s ease; }
        .example-box:hover { box-shadow: var(--shadow-lg); transform: translateX(6px); }
        .example-box h4 { color: var(--primary); margin-bottom: 14px; font-weight: 700; }
        .note-box { background: linear-gradient(135deg, rgba(217, 119, 6, 0.05) 0%, rgba(217, 119, 6, 0.1) 100%); border-left: 5px solid var(--warning); padding: 24px 28px; margin: 28px 0; border-radius: 16px; box-shadow: var(--shadow-md); transition: all 0.3s ease; }
        .note-box:hover { box-shadow: var(--shadow-lg); transform: translateX(6px); }
        .note-box h4 { color: var(--warning); margin-bottom: 14px; font-weight: 700; }
        .tip-box { background: linear-gradient(135deg, rgba(22, 163, 74, 0.05) 0%, rgba(22, 163, 74, 0.1) 100%); border-left: 5px solid var(--success); padding: 24px 28px; margin: 28px 0; border-radius: 16px; box-shadow: var(--shadow-md); transition: all 0.3s ease; }
        .tip-box:hover { box-shadow: var(--shadow-lg); transform: translateX(6px); }
        .tip-box h4 { color: var(--success); margin-bottom: 14px; font-weight: 700; }
        .warning-box { background: linear-gradient(135deg, rgba(220, 38, 38, 0.05) 0%, rgba(220, 38, 38, 0.1) 100%); border-left: 5px solid var(--danger); padding: 24px 28px; margin: 28px 0; border-radius: 16px; box-shadow: var(--shadow-md); transition: all 0.3s ease; }
        .warning-box:hover { box-shadow: var(--shadow-lg); transform: translateX(6px); }
        .warning-box h4 { color: var(--danger); margin-bottom: 14px; font-weight: 700; }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 900px) {
            aside { width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border); padding: 16px 0; box-shadow: var(--shadow-md); }
            main { margin-left: 0; padding: 24px 20px; }
            .page-header { margin: -24px -20px 40px; padding: 40px 20px; }
            .page-header h1 { font-size: 2rem; }
            .table-subsection { padding: 24px; }
            .code-block { padding: 20px; }
            .nav-tree { padding: 0; }
            .nav-tree a { margin-right: 0; border-radius: 8px; }
        }

        @media (max-width: 600px) {
            main { padding: 20px 16px; }
            .page-header h1 { font-size: 1.6rem; }
            .page-header p { font-size: 0.95rem; }
            .content-section h2 { font-size: 1.5rem; }
            .content-section h3 { font-size: 1.25rem; }
            .content-section p { font-size: 1rem; }
            th, td { padding: 12px 14px; font-size: 0.85rem; }
            .table-subsection { padding: 20px; margin-bottom: 28px; }
            .example-box, .note-box, .tip-box, .warning-box { padding: 20px; margin: 20px 0; }
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
    
    # 更新sections目录下的所有HTML文件
    sections_dir = os.path.join(base_dir, 'sections')
    html_files = glob.glob(os.path.join(sections_dir, '*.html'))
    
    print(f'找到 {len(html_files)} 个HTML文件在 sections 目录\n')
    
    updated_count = 0
    for html_file in html_files:
        if update_html_file(html_file):
            updated_count += 1
    
    print(f'\n完成! 共更新 {updated_count}/{len(html_files)} 个文件')

if __name__ == '__main__':
    main()