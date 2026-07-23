#!/usr/bin/env python3
"""
TROS PRO — Inject scraped stats into KOL_DATA in index.html.
Preserves last-known stats when a scrape fails, and preserves the two
Actual-Use constants across auto-updates.
Usage: python3 scripts/update_dashboard.py scrape_results.json index.html
"""
import json, sys, re

KOL_METADATA = {
    "bass__inmeesub": {
        "displayName": "บอสเบลไนติงเจล",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 506700,
        "budget": 20000,
        "profile": "https://www.tiktok.com/@bass__inmeesub",
        "caption": "TROS Pro ทำถึง #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "kuanpuantiew": {
        "displayName": "กวนป่วนเที่ยว",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 1100000,
        "budget": 20000,
        "profile": " https://www.tiktok.com/@kuanpuantiew",
        "caption": "เอาชีวิตรอด ในป่า\nด้วยไอเท็มลับสำหรับชายไทย \n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "juno55555": {
        "displayName": "บักจูโน่",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 2600000,
        "budget": 25000,
        "profile": "https://www.tiktok.com/@juno55555",
        "caption": "สิ่งศักดิ์สิทธิ์ช่วยลูกช้างด้วยเถิด #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "pluemwattanathon": {
        "displayName": "ผมชื่อปลื้ม",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 161100,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@pluemwattanathon",
        "caption": "ผู้ชายดูดี ไม่มีคำว่าสายเกินไป #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "bee112711": {
        "displayName": "bee112711",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 458700,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@bee112711",
        "caption": "เที่ยวใกล้บ้านหนึ่งวัน ตลอดทั้งวันหน้ายังกริบอยู่ได้ตลอด โคตรเจ๋ง #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "kunofficial29": {
        "displayName": "kunofficial29",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 245600,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@kunofficial29",
        "caption": "เสริมหล่อเพิ่มความมั่นใจด้วย TROS Pro ก่อนไปทำงานค่าบ\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "pakkaput17": {
        "displayName": "pakkaput17",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 369700,
        "budget": 14000,
        "profile": "https://www.tiktok.com/@pakkaput17",
        "caption": "ผมลองแล้วเด็ดขนาดนี้ ต้องไปจัดกันแล้วคับ \n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "benmar_98": {
        "displayName": "เบนมาร์",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 1400000,
        "budget": 10000,
        "profile": "https://www.tiktok.com/@benmar_98",
        "caption": "“ สูตรความหล่อ “ \n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "sapol_mu_": {
        "displayName": "sapol_mu_",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 470400,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@sapol_mu_",
        "caption": "เช้าทำงาน เย็นเข้ายิม\nเหนื่อยได้…แต่หน้าต้องไม่เยิ้ม\nพร้อมทุกบทบาทในวันเดียว 👊🏻💪🏻\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "folk.rt": {
        "displayName": "โฟล์คสบายดี",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 89700,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@folk.rt",
        "caption": "จะออกงานไหนก็มั่นใจ \n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน\n#โฟล์คสบายดี #บักหล่าโฟล์ค",
        "postDate": "2026-07-22"
    },
    "homchuy": {
        "displayName": "homchuy",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 3000000,
        "budget": 11000,
        "profile": "https://www.tiktok.com/@homchuy",
        "caption": "สอนทั้งวันแทบไม่รอด แต่หน้ายังรอดอยู่😂 ตัวช่วยของครูสายลุย TROS Pro เลยยย\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "pangpon.thatpong": {
        "displayName": "pangpon.thatpong",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 101100,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@pangpon.thatpong",
        "caption": "หนุ่มโรงงานอย่างผม ยังไงก็ต้องมี TROS Pro ไว้ติดตัวอยู่แล้วค่าบ\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "pattarapon_mike": {
        "displayName": "pattarapon_mike",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 99400,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@pattarapon_mike",
        "caption": "เลิกแอบได้แล้วนะทุกคน #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "mac5869": {
        "displayName": "mac5869",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 266500,
        "budget": 13000,
        "profile": "https://www.tiktok.com/@mac5869",
        "caption": "แป้งที่คู่ควรกับผู้ชาย\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "ig_earthalert24": {
        "displayName": "ig_earthalert24",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 372800,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@ig_earthalert24",
        "caption": "เปิดใจรอบเดียวติดใจเลย แฟนชอบแป้งตัวนี้มาก #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "i.thinnajohn": {
        "displayName": "i.thinnajohn",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 195100,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@i.thinnajohn",
        "caption": "ไอเทมเด็ดสำหรับผู้ชาย 😎 #แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "artchanathip.ppppp": {
        "displayName": "artchanathip.ppppp",
        "platform": "TikTok",
        "category": "TikTok",
        "followers": 178700,
        "budget": 9000,
        "profile": "https://www.tiktok.com/@artchanathip.ppppp",
        "caption": "\"ในที่สุดผู้ชายก็มีแป้งเป็นของตัวเอง 🖤🤍 \"\n#แป้งผู้ชายTROSProFacialBB #เลิกยืมแป้งแฟน\n#หน้าไม่วอกคุมมันตลอดวัน",
        "postDate": "2026-07-22"
    },
    "wecanchoose": {
        "displayName": "ผู้บริโภค",
        "platform": "Facebook",
        "category": "Facebook",
        "followers": 3000000,
        "budget": 47000,
        "profile": "https://www.facebook.com/wecanchoose?locale=th_TH",
        "caption": "",
        "postDate": "2026-08-10"
    }
}

KOL_LINKS = {
    "bass__inmeesub": "https://vt.tiktok.com/ZSXgmUfA8/",
    "kuanpuantiew": "https://vt.tiktok.com/ZSXgqSFbs/",
    "juno55555": "https://vt.tiktok.com/ZSXgpUoF4/",
    "pluemwattanathon": "https://vt.tiktok.com/ZSXgCbosJ/",
    "bee112711": "https://vt.tiktok.com/ZSXgmXbkW/",
    "kunofficial29": "https://vt.tiktok.com/ZSXqv1ytm/",
    "pakkaput17": "https://vt.tiktok.com/ZSXb9cbeX/",
    "benmar_98": "https://vt.tiktok.com/ZSXg96w3m/",
    "sapol_mu_": "https://vt.tiktok.com/ZSXguN6Gr/",
    "folk.rt": "https://vt.tiktok.com/ZSXggLvfp/",
    "homchuy": "https://vt.tiktok.com/ZSXgp9fcv/",
    "pangpon.thatpong": "https://vt.tiktok.com/ZSXgwqy9u/",
    "pattarapon_mike": "https://vt.tiktok.com/ZSXgQGLjv/",
    "mac5869": "https://vt.tiktok.com/ZSXgqvweV/",
    "ig_earthalert24": "https://vt.tiktok.com/ZSXgm3eLV/",
    "i.thinnajohn": "https://vt.tiktok.com/ZSXbPDroy/",
    "artchanathip.ppppp": "https://vt.tiktok.com/ZSXgxGT7k/"
}

NOT_POSTED = set(["wecanchoose"])


def js(s):
    if s is None: return ''
    return str(s).replace('\\','\\\\').replace("'","\\'").replace('\n',' ').replace('\r',' ')


def preserve_use(html, name):
    m = re.search(r'const\s+'+name+r'\s*=\s*([\d.]+)', html)
    return float(m.group(1)) if m else 0


def parse_existing(html):
    ex = {}
    pat = (r"\{\s*username:\s*'([^']+)'.*?followers:\s*(\d+).*?views:\s*(\d+)"
           r".*?likes:\s*(\d+).*?shares:\s*(\d+).*?comments:\s*(\d+).*?saves:\s*(\d+)")
    for m in re.finditer(pat, html):
        ex[m.group(1)] = {'followers':int(m.group(2)),'views':int(m.group(3)),'likes':int(m.group(4)),
                          'shares':int(m.group(5)),'comments':int(m.group(6)),'saves':int(m.group(7))}
    return ex


def entry(handle, scrape, existing):
    m = KOL_METADATA.get(handle, {})
    sd = scrape.get(handle, {}); ex = existing.get(handle, {})
    link = KOL_LINKS.get(handle, '')
    followers = sd.get('followers') or m.get('followers', 0)
    if handle in scrape:
        v,l,s,c,sv = (sd.get('views',0),sd.get('likes',0),sd.get('shares',0),
                      sd.get('comments',0),sd.get('saves',0))
    else:
        v,l,s,c,sv = (ex.get('views',0),ex.get('likes',0),ex.get('shares',0),
                      ex.get('comments',0),ex.get('saves',0))
    posted = handle not in NOT_POSTED and bool(link)
    plat = m.get('platform','TikTok')
    return ("  { username: '%s', displayName: '%s', platform: '%s', category: '%s', gender: '-', "
            "followers: %d, views: %d, likes: %d, shares: %d, comments: %d, saves: %d, "
            "posts: %d, kpi_views: %d, posted: %s, link: '%s', profile: '%s', budget: %d, "
            "caption: '%s', postDate: '%s' }") % (
        js(handle), js(m.get('displayName',handle)), plat, plat, followers,
        v,l,s,c,sv, (1 if posted else 0), v, ('true' if posted else 'false'),
        js(link), js(m.get('profile','')), m.get('budget',0),
        js(m.get('caption',''))[:180], js(m.get('postDate','')))


def main():
    if len(sys.argv) < 3:
        print("Usage: update_dashboard.py scrape_results.json index.html"); sys.exit(1)
    jf, hf = sys.argv[1], sys.argv[2]
    try:
        scrape = json.load(open(jf, encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        scrape = {}
    html = open(hf, encoding='utf-8').read()
    tt_use = preserve_use(html, 'CAMPAIGN_ACTUAL_USE_TIKTOK')
    fb_use = preserve_use(html, 'CAMPAIGN_ACTUAL_USE_FACEBOOK')
    existing = parse_existing(html)
    entries = [entry(h, scrape, existing) for h in KOL_METADATA.keys()]
    new_block = "const KOL_DATA = [\n" + ",\n".join(entries) + "\n];"
    html = re.sub(r'const\s+KOL_DATA\s*=\s*\[[\s\S]*?\];', new_block, html, count=1)
    html = re.sub(r'const\s+CAMPAIGN_ACTUAL_USE_TIKTOK\s*=\s*[\d.]+',
                  f'const CAMPAIGN_ACTUAL_USE_TIKTOK = {tt_use}', html)
    html = re.sub(r'const\s+CAMPAIGN_ACTUAL_USE_FACEBOOK\s*=\s*[\d.]+',
                  f'const CAMPAIGN_ACTUAL_USE_FACEBOOK = {fb_use}', html)
    open(hf, 'w', encoding='utf-8').write(html)
    print(f"Updated {hf}: {len(entries)} KOLs, {len(scrape)} scraped, "
          f"use TT={tt_use:,.0f} FB={fb_use:,.0f}")


if __name__ == '__main__':
    main()
