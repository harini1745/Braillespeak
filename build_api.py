import os

os.makedirs('app/api/ocr', exist_ok=True)
os.makedirs('app/api/translate', exist_ok=True)
os.makedirs('app/api/tts', exist_ok=True)

# ── app/api/ocr/route.ts ─────────────────────────────────────
ocr = r"""import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;

    if (!file) return NextResponse.json({ error: 'No file provided' }, { status: 400 });

    const bytes = await file.arrayBuffer();
    const base64 = Buffer.from(bytes).toString('base64');
    const mimeType = file.type || 'image/png';

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [
              {
                inline_data: { mime_type: mimeType, data: base64 }
              },
              {
                text: `This image contains Braille text. Please:
1. Identify all Braille characters/cells visible in the image
2. Convert them to their Unicode Braille equivalents (⠀-⣿)
3. Return ONLY the Unicode Braille characters, nothing else
If no Braille is found, return "NO_BRAILLE_FOUND"`
              }
            ]
          }]
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json({ error: data.error?.message || 'Gemini API error' }, { status: 500 });
    }

    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    if (text === 'NO_BRAILLE_FOUND') {
      return NextResponse.json({ error: 'No Braille found in image' }, { status: 400 });
    }

    return NextResponse.json({ braille: text.trim() });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
"""

# ── app/api/translate/route.ts ───────────────────────────────
translate = r"""import { NextRequest, NextResponse } from 'next/server';

// Hardcoded Braille Unicode decoder
function decodeBraille(text: string): string {
  const map: Record<string, string> = {
    '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
    '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
    '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
    '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
    '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y',
    '⠵': 'z', '⠀': ' ', '⠂': ',', '⠲': '.', '⠖': '!',
    '⠦': '?', '⠄': "'", '⠤': '-',
  };
  return text.split('').map(c => map[c] || c).join('');
}

export async function POST(req: NextRequest) {
  try {
    const { braille, targetLanguage } = await req.json();

    if (!braille) return NextResponse.json({ error: 'No Braille text provided' }, { status: 400 });

    // First decode with hardcoded map
    const decoded = decodeBraille(braille);

    // Then use Gemini to clean up and translate
    const prompt = targetLanguage && targetLanguage !== 'English'
      ? `The following text was decoded from Braille: "${decoded}". Please clean it up (fix spacing, capitalization) and translate it to ${targetLanguage}. Return ONLY the final translated text, nothing else.`
      : `The following text was decoded from Braille: "${decoded}". Please clean it up (fix spacing, capitalization). Return ONLY the cleaned text, nothing else.`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }]
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      // Fallback to just decoded text
      return NextResponse.json({ text: decoded, confidence: 70 });
    }

    const text = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || decoded;
    return NextResponse.json({ text, confidence: 94 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
"""

# ── app/api/tts/route.ts ─────────────────────────────────────
tts = r"""import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { text, language } = await req.json();
    if (!text) return NextResponse.json({ error: 'No text provided' }, { status: 400 });
    // Web Speech API is used client-side, this route just confirms the text
    return NextResponse.json({ text, language: language || 'English', ready: true });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
"""

with open('app/api/ocr/route.ts', 'w', encoding='utf-8') as f:
    f.write(ocr)

with open('app/api/translate/route.ts', 'w', encoding='utf-8') as f:
    f.write(translate)

with open('app/api/tts/route.ts', 'w', encoding='utf-8') as f:
    f.write(tts)

print('API routes written!')