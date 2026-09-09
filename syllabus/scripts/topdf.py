import re,sys,asyncio
from playwright.async_api import async_playwright
def to_plain(p):
    s=open(p).read()
    s=s.replace('<script src="./support.js"></script>','')
    s=s.replace('<x-dc>','').replace('</x-dc>','')
    s=re.sub(r'<helmet>(.*?)</helmet>', r'\1', s, flags=re.S)
    return s
async def main():
    src,out=sys.argv[1],sys.argv[2]
    open('/tmp/pp.html','w').write(to_plain(src))
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page()
        await pg.goto('file:///tmp/pp.html'); await pg.wait_for_timeout(3000)
        await pg.pdf(path=out, width="8.5in", height="11in", print_background=True,
                     margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()
asyncio.run(main())
