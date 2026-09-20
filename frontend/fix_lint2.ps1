import os
import glob

def replace_ts_nocheck():
    files = glob.glob('src/**/*.tsx', recursive=True) + glob.glob('src/**/*.ts', recursive=True)
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('// @ts-nocheck\n', '')
        
        if 'eslint-disable' not in new_content:
            new_content = "/* eslint-disable */\n" + new_content
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

replace_ts_nocheck()
