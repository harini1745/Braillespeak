'use client';
import { useState, useRef, useEffect } from 'react';

const TABS = [
  { id: 'image', label: 'Image / PDF', icon: '1' },
  { id: 'camera', label: 'Camera', icon: '2' },
  { id: 'unicode', label: 'Unicode', icon: '3' },
  { id: 'batch', label: 'Batch', icon: '4' },
];

const LANGUAGES = ['English','Tamil','Hindi','French','Spanish','German','Japanese','Arabic','Portuguese','Italian'];

export default function ConverterPage() {
  const [dark, setDark] = useState(false);
  const [tab, setTab] = useState('image');
  const [unicode, setUnicode] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [confidence, setConfidence] = useState(0);
  const [lang, setLang] = useState('English');
  const [drag, setDrag] = useState(false);
  const [fileName, setFileName] = useState('');
  const [file, setFile] = useState(null);
  const [playing, setPlaying] = useState(false);
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const fileRef = useRef(null);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const STEPS = ['Detecting Braille dots...', 'Decoding characters...', 'Translating text...', 'Ready!'];

  const handleConvert = async () => {
    setLoading(true);
    setOutput('');
    setConfidence(0);
    setError('');
    setStep(0);

    try {
      let braille = '';

      if (tab === 'unicode') {
        if (!unicode.trim()) { setError('Please paste some Braille Unicode first.'); setLoading(false); return; }
        braille = unicode.trim();
        setStep(1);
      } else if (tab === 'image') {
        if (!file) { setError('Please upload an image or PDF first.'); setLoading(false); return; }
        setStep(0);
        const formData = new FormData();
        formData.append('file', file);
        const ocrRes = await fetch('/api/ocr', { method: 'POST', body: formData });
        const ocrData = await ocrRes.json();
        if (!ocrRes.ok) { setError(ocrData.error || 'OCR failed'); setLoading(false); return; }
        braille = ocrData.text;
        setStep(1);
      } else {
        setError('This input method is coming soon.');
        setLoading(false);
        return;
      }

      setStep(2);
      const translateRes = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: braille, targetLanguage: lang })
      });
      const translateData = await translateRes.json();
      if (!translateRes.ok) { setError(translateData.error || 'Translation failed'); setLoading(false); return; }

      setStep(3);
      setOutput(translateData.text);
      setConfidence(translateData.confidence || 90);
    } catch (e: any) {
      setError(e.message || 'Something went wrong')
    }

    setLoading(false);
  };

  const handleSpeak = () => {
    if (!output) return;
    if (playing) {
      window.speechSynthesis.cancel();
      setPlaying(false);
      return;
    }
    const utter = new SpeechSynthesisUtterance(output);
    const langMap = { Tamil: 'ta-IN', Hindi: 'hi-IN', French: 'fr-FR', Spanish: 'es-ES', German: 'de-DE', Japanese: 'ja-JP', Arabic: 'ar-SA' };
    utter.lang = (langMap as Record<string, string>)[lang] || 'en-US';
    utter.onend = () => setPlaying(false);
    window.speechSynthesis.speak(utter);
    setPlaying(true);
  };

  const handleFile = (f) => { setFile(f); setFileName(f.name); };

  const tabIcons = { image: '[IMG]', camera: '[CAM]', unicode: '[UNI]', batch: '[BAT]' };

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)', color: 'var(--text)' }}>
      <nav className="nav-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2.5 hover:opacity-80 transition-opacity" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>B</div>
            <span className="font-bold text-lg" style={{ letterSpacing: '-0.02em' }}>
              Braille<span style={{ color: 'var(--accent)' }}>Speak</span>
            </span>
          </a>
          <div className="flex items-center gap-3">
            <select value={lang} onChange={e => setLang(e.target.value)}
              className="text-xs px-3 py-1.5 rounded-lg font-medium"
              style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', cursor: 'pointer' }}>
              {LANGUAGES.map(l => <option key={l}>{l}</option>)}
            </select>
            <button onClick={() => setDark(!dark)} className="btn-ghost w-9 h-9 flex items-center justify-center p-0" style={{ borderRadius: '10px' }}>
              {dark ? 'Light' : 'Dark'}
            </button>
            <a href="/sign-in" className="btn-ghost px-4 py-2 text-xs font-medium" style={{ textDecoration: 'none', display: 'inline-block' }}>Sign in</a>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-1" style={{ letterSpacing: '-0.02em' }}>Braille Converter</h1>
          <p className="text-sm" style={{ color: 'var(--muted)' }}>Upload, capture, or paste Braille to get instant speech output</p>
        </div>

        {error && (
          <div className="mb-4 px-4 py-3 rounded-xl text-sm font-medium" style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#ef4444' }}>
            {error}
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-5">
          <div className="flex flex-col gap-4">
            <div className="card p-1.5 flex gap-1">
              {TABS.map(t => (
                <button key={t.id} onClick={() => setTab(t.id)}
                  className={'tab-pill flex-1 flex items-center justify-center gap-1.5 ' + (tab === t.id ? 'active' : '')}>
                  <span className="hidden sm:inline">{t.label}</span>
                </button>
              ))}
            </div>

            <div className="card flex-1" style={{ minHeight: '300px' }}>
              {tab === 'image' && (
                <div
                  className={'upload-zone h-full flex flex-col items-center justify-center p-8 m-3 rounded-xl ' + (drag ? 'drag' : '')}
                  style={{ minHeight: '260px' }}
                  onDragOver={e => { e.preventDefault(); setDrag(true); }}
                  onDragLeave={() => setDrag(false)}
                  onDrop={e => { e.preventDefault(); setDrag(false); const f = e.dataTransfer.files[0]; if (f) handleFile(f); }}
                  onClick={() => fileRef.current?.click()}
                >
                  <input ref={fileRef} type="file" accept="image/*,.pdf" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
                  <div className="text-5xl mb-3 opacity-30">{fileName ? '+' : 'v'}</div>
                  {fileName ? (
                    <>
                      <p className="text-sm font-semibold mb-1" style={{ color: 'var(--accent)' }}>{fileName}</p>
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>Click to change</p>
                    </>
                  ) : (
                    <>
                      <p className="text-sm font-semibold mb-1">Drop image or PDF here</p>
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>or click to browse</p>
                    </>
                  )}
                </div>
              )}

              {tab === 'camera' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">Live Camera Capture</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}

              {tab === 'unicode' && (
                <div className="p-5 h-full flex flex-col" style={{ minHeight: '300px' }}>
                  <div className="flex items-center justify-between mb-3">
                    <label className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>BRAILLE UNICODE</label>
                    <button onClick={() => setUnicode('')} className="text-xs" style={{ color: 'var(--muted)' }}>Clear</button>
                  </div>
                  <textarea
                    value={unicode}
                    onChange={e => setUnicode(e.target.value)}
                    placeholder="Paste Braille Unicode here..."
                    className="flex-1 resize-none outline-none text-2xl tracking-widest leading-loose"
                    style={{ background: 'transparent', color: 'var(--accent)', fontFamily: 'monospace' }}
                  />
                  <div className="pt-3 border-t text-xs" style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}>
                    {unicode.length} characters
                  </div>
                </div>
              )}

              {tab === 'batch' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">Batch Processing</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
            </div>

            <button onClick={handleConvert} disabled={loading} className="btn-primary py-3 text-sm flex items-center justify-center gap-2">
              {loading ? (
                <><div className="spinner" /> {STEPS[step]}</>
              ) : 'Convert & Speak'}
            </button>
          </div>

          <div className="flex flex-col gap-4">
            <div className="card p-5 flex-1" style={{ minHeight: '220px' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="dot-badge" style={{ background: output ? '#22c55e' : 'var(--muted)' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>TRANSLATION OUTPUT</span>
                </div>
                {output && (
                  <button onClick={() => navigator.clipboard.writeText(output)} className="text-xs font-medium px-2.5 py-1 rounded-lg" style={{ background: 'var(--surface2)', color: 'var(--muted)' }}>
                    Copy Text
                  </button>
                )}
              </div>
              {loading ? (
                <div className="flex flex-col gap-3">
                  {STEPS.slice(0,3).map((s, i) => (
                    <div key={s} className="flex items-center gap-2.5">
                      {i < step
                        ? <span className="text-green-500 text-sm">ok</span>
                        : i === step
                          ? <div className="spinner" style={{ borderTopColor: 'var(--accent)', borderColor: 'rgba(108,78,242,0.2)' }} />
                          : <div className="w-4 h-4 rounded-full" style={{ background: 'var(--surface2)' }} />}
                      <span className="text-xs" style={{ color: i <= step ? 'var(--text)' : 'var(--muted)' }}>{s}</span>
                    </div>
                  ))}
                </div>
              ) : output ? (
                <p className="text-sm leading-relaxed">{output}</p>
              ) : (
                <div className="flex flex-col items-center justify-center h-32 text-center">
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Converted text will appear here</p>
                </div>
              )}
            </div>

            <div className="card p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>CONFIDENCE SCORE</span>
                <span className="text-sm font-bold" style={{ color: confidence > 0 ? '#22c55e' : 'var(--muted)' }}>{confidence > 0 ? confidence + '%' : '-'}</span>
              </div>
              <div className="confidence-track">
                <div className="confidence-fill" style={{ width: confidence + '%' }} />
              </div>
            </div>

            <div className="card p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="dot-badge" style={{ background: playing ? '#6c4ef2' : 'var(--muted)' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>AUDIO OUTPUT</span>
                </div>
                <span className="text-xs" style={{ color: 'var(--muted)' }}>{lang}</span>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={handleSpeak} disabled={!output}
                  className="btn-primary w-10 h-10 flex items-center justify-center p-0 flex-shrink-0"
                  style={{ borderRadius: '10px', opacity: output ? 1 : 0.4, fontSize: '16px' }}>
                  {playing ? '||' : '>'}
                </button>
                <div className="flex-1 flex items-end gap-px h-8">
                  {Array.from({ length: 40 }).map((_, i) => {
                    const h = Math.sin(i * 0.5) * 40 + 50;
                    return (
                      <div key={i} className={'wave-bar flex-1 ' + (playing && output ? 'active' : '')}
                        style={{ height: h + '%', animationDelay: (i * 0.04) + 's' }} />
                    );
                  })}
                </div>
                <button onClick={() => {
                  const blob = new Blob([output], { type: 'text/plain' });
                  const a = document.createElement('a');
                  a.href = URL.createObjectURL(blob);
                  a.download = 'braillespeak-output.txt';
                  a.click();
                }} disabled={!output} className="btn-ghost w-8 h-8 flex items-center justify-center p-0 text-sm" style={{ opacity: output ? 1 : 0.4 }}>
                  DL
                </button>
              </div>
            </div>

            <div className="card p-4">
              <p className="text-xs font-semibold mb-3" style={{ color: 'var(--muted)' }}>TRANSLATE TO</p>
              <div className="flex flex-wrap gap-1.5">
                {LANGUAGES.map(l => (
                  <button key={l} onClick={() => setLang(l)} className={'lang-chip ' + (lang === l ? 'active' : '')}>{l}</button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
