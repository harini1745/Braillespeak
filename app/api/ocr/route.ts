import { NextRequest, NextResponse } from 'next/server';
import { Jimp } from 'jimp';

export async function POST(request: NextRequest) {
  try {
    const { imageBase64, mimeType } = await request.json();
    if (!imageBase64) return NextResponse.json({ error: 'Missing image data' }, { status: 400 });

    const buffer = Buffer.from(imageBase64, 'base64');
    const image = await Jimp.fromBuffer(buffer);
    const width = image.width;
    const height = image.height;

    const dots: { x: number; y: number }[] = [];
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const hex = image.getPixelColor(x, y);
        const r = (hex >>> 24) & 0xff;
        const g = (hex >>> 16) & 0xff;
        const b = (hex >>> 8) & 0xff;
        if ((r + g + b) / 3 < 100) dots.push({ x, y });
      }
    }

    if (dots.length === 0) return NextResponse.json({ text: '' });

    const clusters: { x: number; y: number }[] = [];
    const visited = new Set<string>();
    for (const dot of dots) {
      const key = `${Math.round(dot.x / 10)},${Math.round(dot.y / 10)}`;
      if (!visited.has(key)) { visited.add(key); clusters.push(dot); }
    }

    const yLevels: number[] = [];
    for (const c of clusters) {
      if (!yLevels.some(l => Math.abs(l - c.y) < height * 0.06)) yLevels.push(c.y);
    }
    yLevels.sort((a, b) => a - b);

    const xLevels: number[] = [];
    for (const c of clusters) {
      if (!xLevels.some(l => Math.abs(l - c.x) < width * 0.04)) xLevels.push(c.x);
    }
    xLevels.sort((a, b) => a - b);

    const cellXGroups: [number, number][] = [];
    let i = 0;
    while (i < xLevels.length) {
      if (i + 1 < xLevels.length && xLevels[i + 1] - xLevels[i] < width * 0.12) {
        cellXGroups.push([xLevels[i], xLevels[i + 1]]);
        i += 2;
      } else {
        cellXGroups.push([xLevels[i], xLevels[i] + width * 0.04]);
        i++;
      }
    }

    // Pick best 3 consecutive y-levels (smallest total span)
    let rowYs = yLevels.slice(0, 3);
    if (yLevels.length >= 4) {
      const span1 = yLevels[2] - yLevels[0];
      const span2 = yLevels[3] - yLevels[1];
      rowYs = span1 <= span2 ? yLevels.slice(0, 3) : yLevels.slice(1, 4);
    }

    console.log('rowYs:', rowYs);

    const brailleMap: Record<string, string> = {
      '1': 'a', '12': 'b', '14': 'c', '145': 'd', '15': 'e',
      '124': 'f', '1245': 'g', '125': 'h', '24': 'i', '245': 'j',
      '13': 'k', '123': 'l', '134': 'm', '1345': 'n', '135': 'o',
      '1234': 'p', '12345': 'q', '1235': 'r', '234': 's', '2345': 't',
      '136': 'u', '1236': 'v', '2456': 'w', '1346': 'x', '13456': 'y', '1356': 'z',
    };

    const xThresh = width * 0.05;
    const rowSpacing = rowYs.length > 1 ? (rowYs[rowYs.length - 1] - rowYs[0]) / (rowYs.length - 1) : 30;
    const yThresh = rowSpacing * 0.4;
    let text = '';

    for (const [leftX, rightX] of cellXGroups) {
      const dotNums: number[] = [];
      for (const cluster of clusters) {
        const isLeft = Math.abs(cluster.x - leftX) < xThresh;
        const isRight = Math.abs(cluster.x - rightX) < xThresh;
        if (!isLeft && !isRight) continue;
        for (let row = 0; row < rowYs.length; row++) {
          if (Math.abs(cluster.y - rowYs[row]) < yThresh) {
            const dotNum = isLeft ? row + 1 : row + 4;
            if (!dotNums.includes(dotNum)) dotNums.push(dotNum);
          }
        }
      }
      dotNums.sort((a, b) => a - b);
      const key = dotNums.join('');
      console.log(`Cell [${leftX},${rightX}] dots: ${key}`);
      text += brailleMap[key] ?? '?';
    }

    console.log('OCR decoded text:', text);
    return NextResponse.json({ text });
  } catch (error) {
    console.error('OCR error:', error);
    return NextResponse.json({ error: 'OCR failed', details: error instanceof Error ? error.message : 'Unknown' }, { status: 500 });
  }
}