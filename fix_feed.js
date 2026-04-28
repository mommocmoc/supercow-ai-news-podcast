const fs = require('fs');

let xml = fs.readFileSync('feed.xml', 'utf8');

// 1. Remove the 4-22 episode if it's there
const ep422Regex = /<item><title\s*>마우스를 뺏은 AI와 900조 원의 거품 \(2026-04-22\)<\/title>.*?<\/item>/s;
xml = xml.replace(ep422Regex, '');

// 2. Add channel info
const channelInfo = `<itunes:author>SuperCow 소재환</itunes:author><itunes:explicit>false</itunes:explicit><itunes:category text="Technology" /><itunes:owner><itunes:name>소재환</itunes:name><itunes:email>hey@cowcowwow.kr</itunes:email></itunes:owner>`;
xml = xml.replace('</language><itunes:image', '</language>' + channelInfo + '<itunes:image');

// 3. Add guid and explicit to each item
const items = [];
const itemRegex = /<item\b[^>]*>(.*?)<\/item>/gs;

let match;
let newXml = xml;
let urlCounts = {};

xml.replace(itemRegex, (fullMatch, innerContent) => {
    const urlMatch = innerContent.match(/<enclosure[^>]*url="([^"]+)"/);
    if (urlMatch) {
        let url = urlMatch[1];
        if (!urlCounts[url]) {
            urlCounts[url] = 1;
        } else {
            urlCounts[url]++;
            url = url + '#' + urlCounts[url];
        }
        
        let newInner = innerContent + `<guid isPermaLink="false">${url}</guid><itunes:explicit>false</itunes:explicit>`;
        
        // Handle weird spacing by just replacing the innerContent before </item>
        let newMatch = fullMatch.replace(/(<\/item>)/, `<guid isPermaLink="false">${url}</guid><itunes:explicit>false</itunes:explicit>$1`);
        newXml = newXml.replace(fullMatch, newMatch);
    }
});

fs.writeFileSync('feed.xml', newXml);
console.log('Fixed feed.xml');
