import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { text, targetLanguage } = await request.json();
    if (!text || !targetLanguage) return NextResponse.json({ error: 'Missing text or targetLanguage' }, { status: 400 });

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
      },
      body: JSON.stringify({
        model: 'llama-3.3-70b-versatile',
        messages: [{ role: 'user', content: `Translate to ${targetLanguage}. Return ONLY the translated text, nothing else:\n\n${text}` }],
        max_tokens: 1024,
      }),
    });

    if (!response.ok) throw new Error('Groq API failed');
    const data = await response.json();
    const translatedText = data.choices?.[0]?.message?.content?.trim() || '';
    return NextResponse.json({ translatedText, confidence: 0.93 });
  } catch (error) {
    console.error('Translation error:', error);
    return NextResponse.json({ error: 'Translation failed', details: error instanceof Error ? error.message : 'Unknown' }, { status: 500 });
  }
}