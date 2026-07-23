#!/usr/bin/env python3
"""
Update Actual-Use constants in index.html.
Usage: python3 scripts/update_actual_use.py <platform: tiktok|facebook> <amount> index.html
"""
import sys, re
def main():
    if len(sys.argv) < 4:
        print("Usage: update_actual_use.py <tiktok|facebook> <amount> index.html"); sys.exit(1)
    plat, amount, hf = sys.argv[1].lower(), float(sys.argv[2]), sys.argv[3]
    name = 'CAMPAIGN_ACTUAL_USE_TIKTOK' if plat.startswith('t') else 'CAMPAIGN_ACTUAL_USE_FACEBOOK'
    html = open(hf, encoding='utf-8').read()
    html = re.sub(r'const\s+'+name+r'\s*=\s*[\d.]+', f'const {name} = {amount}', html)
    open(hf,'w',encoding='utf-8').write(html)
    print(f"{name} -> {amount:,.0f}")
if __name__ == '__main__':
    main()
