import re,sys,asyncio
from playwright.async_api import async_playwright
def to_plain(p):
    s=open(p).read()
    s=s.replace('<script src="./support.js"></script>','').replace('<x-dc>','').replace('</x-dc>','')
    return re.sub(r'<helmet>(.*?)</helmet>', r'\1', s, flags=re.S)
async def main():
    src,out,w,h=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
    open('/tmp/t2.html','w').write(to_plain(src))
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page()
        await pg.goto('file:///tmp/t2.html'); await pg.wait_for_timeout(3000)
        await pg.pdf(path=out, width=w, height=h, print_background=True,
                     margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()
asyncio.run(main())
