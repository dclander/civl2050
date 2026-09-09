import re,sys,asyncio
from playwright.async_api import async_playwright
def to_plain(p):
    s=open(p).read()
    s=s.replace('<script src="./support.js"></script>','')
    s=s.replace('<x-dc>','').replace('</x-dc>','')
    s=re.sub(r'<helmet>(.*?)</helmet>', r'\1', s, flags=re.S)
    return s
async def main():
    src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    open('/tmp/p.html','w').write(to_plain(src))
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':w,'height':h}, device_scale_factor=2)
        await pg.goto('file:///tmp/p.html'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=out, full_page=True); await b.close()
asyncio.run(main())
