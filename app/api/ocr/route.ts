import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { imageBase64, mimeType } = await request.json();
    if (!imageBase64) return NextResponse.json({ error: 'Missing image data' }, { status: 400 });

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  inline_data: {
                    mime_type: mimeType || 'image/jpeg',
                    data: imageBase64,
                  },
                },
                {
                  text: 'This image contains Braille text. Read the Braille carefully and return ONLY the decoded plain English text. No explanations, no descriptions, just the words.',
                },
              ],
            },
          ],
        }),
      }
    );

    if (!response.ok) {
      const err = await response.text();
      console.error('Gemini OCR error:', err);
      throw new Error('Gemini vision API failed');
    }

    const data = await response.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || '';
    console.log('OCR raw response:', text);
    return NextResponse.json({ text });
  } catch (error) {
    console.error('OCR error:', error);
    return NextResponse.json({ error: 'OCR failed', details: error instanceof Error ? error.message : 'Unknown' }, { status: 500 });
  }
}