'use client';

import { useState, useRef } from 'react';
import { supabase } from '@/lib/supabase';

const decodeBraille = {'⠀':' ','⠁':'a','⠃':'b','⠉':'c','⠙':'d','⠑':'e','⠋':'f','⠛':'g','⠓':'h','⠊':'i','⠚':'j','⠅':'k','⠇':'l','⠍':'m','⠝':'n','⠕':'o','⠏':'p','⠟':'q','⠗':'r','⠎':'s','⠞':'t','⠥':'u','⠧':'v','⠺':'w','⠭':'x','⠽':'y','⠵':'z'};

const LANGUAGES = ['English','Tamil','Hindi','French','Spanish','German','Japanese','Arabic','Portuguese','Italian'];
const TABS = ['unicode','image','camera','batch'];

export default function Converter() {
  const [activeTab, setActiveTab] = useState('unicode');
  const [unicodeBraille, setUnicodeBraille] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [audioPlaying, setAudioPlaying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [step, setStep] = useState(0);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const STEPS = ['Detecting Braille dots...', 'Decoding characters...', 'Translating text...', 'Ready!'];

  const decodeBrailleText = (text: string) =>
    text.split('').map((char) => decodeBraille[char] ?? char).join('');

  const toBase64 = (file: File): Promise<string> =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result.split(',')[1]);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

  const handleImageSelect = (file: File) => {
    if (!file.type.startsWith('image/')) { setError('Please upload an image file.'); return; }
    setImageFile(file);
    setError('');
    setResult(null);
    setImagePreview(URL.createObjectURL(file));
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleImageSelect(file);
  };

  const handleConvertUnicode = async () => {
    if (!unicodeBraille.trim()) { setError('Please paste some Braille Unicode first.'); return; }
    setLoading(true); setError(''); setResult(null); setStep(0);
    try {
      setStep(1);
      const decodedText = decodeBrailleText(unicodeBraille);
      if (!decodedText.trim()) { setError('No valid Braille found.'); setLoading(false); return; }
      setStep(2);
      const res = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: decodedText, targetLanguage: selectedLanguage }),
      });
      if (!res.ok) throw new Error('Translation failed');
      const { translatedText, confidence } = await res.json();
      setStep(3);
      const finalResult = { decodedText, translatedText, confidence: confidence || 0.93, lang: selectedLanguage };
      setResult(finalResult);
      try {
        await supabase.from('conversions').insert({
          user_id: 'anonymous',
          original_braille: unicodeBraille,
          decoded_text: decodedText,
          translated_text: translatedText,
          language: selectedLanguage,
          confidence: confidence || 0.93,
        });
      } catch (e) { console.error('Save failed:', e); }
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleConvertImage = async () => {
    if (!imageFile) { setError('Please upload an image first.'); return; }
    setLoading(true); setError(''); setResult(null); setStep(0);
    try {
      setStep(1);
      const base64 = await toBase64(imageFile);
      const mimeType = imageFile.type;

      const ocrRes = await fetch('/api/ocr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ imageBase64: base64, mimeType }),
      });
      if (!ocrRes.ok) throw new Error('OCR failed');
      const { text: ocrText } = await ocrRes.json();
      if (!ocrText || !ocrText.trim()) { setError('Could not extract text from image.'); setLoading(false); return; }

      // Extract just the decoded letters from OCR response
      const raw = ocrText.trim();
      const match = raw.match(/(?:decoded\s+(?:word|letters?|text)\s+(?:is|are):?\s*)([a-zA-Z\s]+)$/im);
      const decodedText = match
        ? match[1].trim()
        : raw.split('\n').filter((l: string) => l.trim()).pop()?.replace(/[^a-zA-Z\s]/g, '').trim() || raw;

      setStep(2);
      setStep(3);
      const transRes = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: decodedText, targetLanguage: selectedLanguage }),
      });
      if (!transRes.ok) throw new Error('Translation failed');
      const { translatedText, confidence } = await transRes.json();

      const finalResult = { decodedText, translatedText, confidence: confidence || 0.91, lang: selectedLanguage };
      setResult(finalResult);

      try {
        await supabase.from('conversions').insert({
          user_id: 'anonymous',
          original_braille: '[image upload]',
          decoded_text: decodedText,
          translated_text: translatedText,
          language: selectedLanguage,
          confidence: confidence || 0.91,
        });
      } catch (e) { console.error('Save failed:', e); }
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleConvert = () => {
    if (activeTab === 'unicode') handleConvertUnicode();
    else if (activeTab === 'image') handleConvertImage();
  };

  const canConvert = activeTab === 'unicode' ? !!unicodeBraille.trim() : activeTab === 'image' ? !!imageFile : false;

  const handleSpeak = () => {
    if (!result?.translatedText) return;
    if (audioPlaying) { window.speechSynthesis.cancel(); setAudioPlaying(false); return; }
    const utterance = new SpeechSynthesisUtterance(result.translatedText);
    const langMap: Record<string, string> = { Tamil: 'ta-IN', Hindi: 'hi-IN', French: 'fr-FR', Spanish: 'es-ES', German: 'de-DE', Japanese: 'ja-JP', Arabic: 'ar-SA', Portuguese: 'pt-PT', Italian: 'it-IT' };
    utterance.lang = langMap[result.lang] || 'en-US';
    utterance.rate = 0.9;
    utterance.onend = () => setAudioPlaying(false);
    utterance.onerror = () => setAudioPlaying(false);
    window.speechSynthesis.speak(utterance);
    setAudioPlaying(true);
  };

  const handleCopy = () => {
    if (!result?.translatedText) return;
    navigator.clipboard.writeText(result.translatedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)', color: 'var(--text)' }}>
      <nav className="nav-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" style={{ textDecoration: 'none', color: 'inherit' }} className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>B</div>
            <span className="font-bold text-lg">Braille<span style={{ color: 'var(--accent)' }}>Speak</span></span>
          </a>
          <div className="flex items-center gap-3">
            <select value={selectedLanguage} onChange={e => setSelectedLanguage(e.target.value)} className="text-xs px-3 py-1.5 rounded-lg font-medium" style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', cursor: 'pointer' }}>
              {LANGUAGES.map(l => <option key={l}>{l}</option>)}
            </select>
            <a href="/sign-in" className="btn-ghost px-4 py-2 text-xs font-medium" style={{ textDecoration: 'none', display: 'inline-block' }}>Sign in</a>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-1">Braille Converter</h1>
          <p className="text-sm" style={{ color: 'var(--muted)' }}>Upload, capture, or paste Braille to get instant speech output</p>
        </div>

        {error && (
          <div className="mb-4 px-4 py-3 rounded-xl text-sm font-medium" style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#ef4444' }}>{error}</div>
        )}

        <div className="grid lg:grid-cols-2 gap-5">
          <div className="flex flex-col gap-4">
            <div className="card p-1.5 flex gap-1">
              {TABS.map(t => (
                <button key={t} onClick={() => { setActiveTab(t); setError(''); setResult(null); }} className={'tab-pill flex-1 ' + (activeTab === t ? 'active' : '')}>
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>

            <div className="card flex-1" style={{ minHeight: '300px' }}>
              {activeTab === 'unicode' && (
                <div className="p-5 h-full flex flex-col" style={{ minHeight: '300px' }}>
                  <div className="flex items-center justify-between mb-3">
                    <label className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>BRAILLE UNICODE</label>
                    <button onClick={() => setUnicodeBraille('')} className="text-xs" style={{ color: 'var(--muted)' }}>Clear</button>
                  </div>
                  <textarea value={unicodeBraille} onChange={e => { setUnicodeBraille(e.target.value); setError(''); }} placeholder="Paste Braille Unicode here... (e.g. ⠓⠑⠇⠇⠕)" className="flex-1 resize-none outline-none text-2xl tracking-widest leading-loose" style={{ background: 'transparent', color: 'var(--accent)', fontFamily: 'monospace' }} />
                  <div className="pt-3 border-t text-xs" style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}>{unicodeBraille.length} characters</div>
                </div>
              )}

              {activeTab === 'image' && (
                <div className="p-5 h-full flex flex-col" style={{ minHeight: '300px' }}>
                  <div className="flex items-center justify-between mb-3">
                    <label className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>BRAILLE IMAGE</label>
                    {imageFile && <button onClick={() => { setImageFile(null); setImagePreview(null); setResult(null); }} className="text-xs" style={{ color: 'var(--muted)' }}>Clear</button>}
                  </div>
                  {imagePreview ? (
                    <div className="flex-1 flex flex-col items-center justify-center gap-3">
                      <img src={imagePreview} alt="Braille upload" className="rounded-xl object-contain" style={{ maxHeight: '200px', maxWidth: '100%', border: '1px solid var(--border)' }} />
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>{imageFile?.name}</p>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col items-center justify-center rounded-xl cursor-pointer transition-all" style={{ border: `2px dashed ${dragOver ? 'var(--accent)' : 'var(--border)'}`, background: dragOver ? 'rgba(108,78,242,0.05)' : 'transparent', minHeight: '200px' }} onDragOver={e => { e.preventDefault(); setDragOver(true); }} onDragLeave={() => setDragOver(false)} onDrop={handleFileDrop} onClick={() => fileInputRef.current?.click()}>
                      <div className="text-3xl mb-3">📷</div>
                      <p className="text-sm font-medium mb-1">Drop image here or click to upload</p>
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>PNG, JPG, WEBP supported</p>
                      <input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => { if (e.target.files?.[0]) handleImageSelect(e.target.files[0]); }} />
                    </div>
                  )}
                </div>
              )}

              {(activeTab === 'camera' || activeTab === 'batch') && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
            </div>

            <button onClick={handleConvert} disabled={loading || !canConvert} className="btn-primary py-3 text-sm flex items-center justify-center gap-2" style={{ opacity: loading || !canConvert ? 0.6 : 1 }}>
              {loading ? <><div className="spinner" />{STEPS[step]}</> : 'Convert & Speak'}
            </button>
          </div>

          <div className="flex flex-col gap-4">
            <div className="card p-5 flex-1" style={{ minHeight: '220px' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="dot-badge" style={{ background: result ? '#22c55e' : 'var(--muted)' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>TRANSLATION OUTPUT</span>
                </div>
                {result && <button onClick={handleCopy} className="text-xs font-medium px-2.5 py-1 rounded-lg" style={{ background: 'var(--surface2)', color: 'var(--muted)' }}>{copied ? '✓ Copied' : 'Copy Text'}</button>}
              </div>
              {loading ? (
                <div className="flex flex-col gap-3">
                  {STEPS.slice(0, 3).map((s, i) => (
                    <div key={s} className="flex items-center gap-2.5">
                      {i < step ? <span className="text-green-500 text-sm">✓</span> : i === step ? <div className="spinner" style={{ borderTopColor: 'var(--accent)', borderColor: 'rgba(108,78,242,0.2)' }} /> : <div className="w-4 h-4 rounded-full" style={{ background: 'var(--surface2)' }} />}
                      <span className="text-xs" style={{ color: i <= step ? 'var(--text)' : 'var(--muted)' }}>{s}</span>
                    </div>
                  ))}
                </div>
              ) : result ? (
                <div className="space-y-3">
                  <div><p className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Decoded</p><p className="text-sm font-mono" style={{ color: 'var(--muted)' }}>{result.decodedText}</p></div>
                  <div><p className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Translated ({result.lang})</p><p className="text-sm leading-relaxed font-medium">{result.translatedText}</p></div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-32 text-center">
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Converted text will appear here</p>
                </div>
              )}
            </div>

            <div className="card p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>CONFIDENCE SCORE</span>
                <span className="text-sm font-bold" style={{ color: result ? '#22c55e' : 'var(--muted)' }}>{result ? Math.round(result.confidence * 100) + '%' : '-'}</span>
              </div>
              <div className="confidence-track"><div className="confidence-fill" style={{ width: result ? (result.confidence * 100) + '%' : '0%' }} /></div>
            </div>

            <div className="card p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="dot-badge" style={{ background: audioPlaying ? '#6c4ef2' : 'var(--muted)' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>AUDIO OUTPUT</span>
                </div>
                <span className="text-xs" style={{ color: 'var(--muted)' }}>{selectedLanguage}</span>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={handleSpeak} disabled={!result} className="btn-primary w-10 h-10 flex items-center justify-center p-0 flex-shrink-0" style={{ borderRadius: '10px', opacity: result ? 1 : 0.4, fontSize: '16px' }}>{audioPlaying ? '⏸' : '▶'}</button>
                <div className="flex-1 flex items-end gap-px h-8">
                  {Array.from({ length: 40 }).map((_, i) => { const h = Math.sin(i * 0.5) * 40 + 50; return <div key={i} className={'wave-bar flex-1 ' + (audioPlaying && result ? 'active' : '')} style={{ height: h + '%', animationDelay: (i * 0.04) + 's' }} />; })}
                </div>
              </div>
            </div>

            <div className="card p-4">
              <p className="text-xs font-semibold mb-3" style={{ color: 'var(--muted)' }}>TRANSLATE TO</p>
              <div className="flex flex-wrap gap-1.5">
                {LANGUAGES.map(l => <button key={l} onClick={() => setSelectedLanguage(l)} className={'lang-chip ' + (selectedLanguage === l ? 'active' : '')}>{l}</button>)}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}