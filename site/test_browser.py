"""Local real-Chromium checks. Run after serving dist on localhost:8766."""
from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:8766/');page.wait_for_selector('.card');assert page.locator('.card').count()==13
 page.screenshot(path='/tmp/fieldnotes-desktop.png',full_page=True)
 page.locator('#query').fill('路网');page.wait_for_timeout(300);assert page.locator('.card').count()>0;assert page.locator('mark').count()>0
 page.locator('.card h3 a').first.click();page.wait_for_selector('#reader:not([hidden])');assert page.locator('#body').inner_text();assert page.locator('#toc a').count()>0
 page.locator('#toc a').last.click();assert page.evaluate('window.scrollY')>0
 page.reload();page.wait_for_selector('#reader:not([hidden])');assert page.locator('#article-title').inner_text()
 page.locator('#back').click();assert page.locator('#query').input_value()=='路网'
 page.go_back();page.wait_for_selector('#reader:not([hidden])');page.go_forward();page.wait_for_selector('#library:not([hidden])')
 page.locator('#query').fill('<script>alert(1)</script>');page.wait_for_timeout(300);assert page.locator('#empty').is_visible();assert page.locator('script').count()==1
 page.locator('#clear').click();assert page.locator('.card').count()==13
 page.locator('#categories button').filter(has_text='小说创作').click();assert page.locator('.card').count()==1
 page.locator('#theme').click();assert page.locator('html').get_attribute('data-theme')=='dark';page.reload();page.wait_for_selector('.card');assert page.locator('html').get_attribute('data-theme')=='dark'
 page.locator('#theme').click();page.goto('http://localhost:8766/');page.wait_for_selector('.card');page.keyboard.press('/');assert page.locator('#query').evaluate('(e)=>e===document.activeElement')
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path='/tmp/fieldnotes-mobile.png',full_page=True);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.locator('.card h3 a').filter(has_text='平面设计').click();page.wait_for_selector('#reader:not([hidden])');assert page.locator('#body img').count()==6;page.screenshot(path='/tmp/fieldnotes-reader-mobile.png',full_page=True);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 with page.expect_download() as info:page.locator('#downloads a').first.click()
 assert info.value.suggested_filename.endswith('.docx')
 assert not errors,errors
 browser.close();print('Chromium: 13 cards, search/highlight, reading/TOC, reload, back-forward, XSS query, clear, category, theme persistence, keyboard, mobile overflow, six images, Word download passed.')
