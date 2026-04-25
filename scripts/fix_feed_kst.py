import xml.etree.ElementTree as ET
import os
from datetime import datetime, timezone, timedelta

def fix():
    feed_file = '/Users/deute1615/supercow-ai-news-podcast/feed.xml'
    ITUNES_NS = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
    ET.register_namespace('itunes', ITUNES_NS)
    tree = ET.parse(feed_file)
    root = tree.getroot()
    channel = root.find('channel')
    items = channel.findall('item')
    for item in items:
        encl = item.find('enclosure')
        if encl is not None and 'AI_Daily_News_2026-04-25.mp3' in encl.get('url'):
            channel.remove(item)
    
    item = ET.SubElement(channel, 'item')
    title = '코딩은 맡겨도 전등은 내가 끈다'
    ET.SubElement(item, 'title').text = title
    
    mp3_path = '/Users/deute1615/supercow-ai-news-podcast/audio/AI_Daily_News_2026-04-25.mp3'
    file_size = os.path.getsize(mp3_path)
    ET.SubElement(item, 'enclosure', 
                   url='https://mommocmoc.github.io/supercow-ai-news-podcast/audio/AI_Daily_News_2026-04-25.mp3', 
                   type='audio/mpeg', 
                   length=str(file_size))
    
    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst)
    ET.SubElement(item, 'pubDate').text = now_kst.strftime('%a, %d %b %Y %H:%M:%S +0900')
    
    desc = '2026년 04월 25일 자 AI 데일리 뉴스 - 코딩은 맡겨도 전등은 내가 끈다 등 주요 AI 뉴스를 정리해 드립니다.'
    ET.SubElement(item, 'description').text = desc
    ET.SubElement(item, '{%s}summary' % ITUNES_NS).text = desc
    
    tree.write(feed_file, encoding='UTF-8', xml_declaration=True)

if __name__ == '__main__':
    fix()
