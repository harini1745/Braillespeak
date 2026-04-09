import os

content = r"""'use client';

import { useState } from 'react';

const decodeBraille = {'⠀': ' ','⠁': 'a','⠂': 'b','⠃': 'ab','⠄': 'c','⠅': 'ac','⠆': 'bc','⠇': 'abc','⠈': 'd','⠉': 'ad','⠊': 'bd','⠋': 'abd','⠌': 'cd','⠍': 'acd','⠎': 'bcd','⠏': 'abcd','⠐': 'e','⠑': 'ae','⠒': 'be','⠓': 'abe','⠔': 'ce','⠕': 'ace','⠖': 'bce','⠗': 'abce','⠘': 'de','⠙': 'ade','⠚': 'bde','⠛': 'abde','⠜': 'cde','⠝': 'acde','⠞': 'bcde','⠟': 'abcde','⠠': 'f','⠡': 'af','⠢': 'bf','⠣': 'abf','⠤': 'cf','⠥': 'acf','⠦': 'bcf','⠧': 'abcf','⠨': 'df','⠩': 'adf','⠪': 'bdf','⠫': 'abdf','⠬': 'cdf','⠭': 'acdf','⠮': 'bcdf','⠯': 'abcdf','⠰': 'ef','⠱': 'aef','⠲': 'bef','⠳': 'abef','⠴': 'cef','⠵': 'acef','⠶': 'bcef','⠷': 'abcef','⠸': 'def','⠹': 'adef','⠺': 'bdef','⠻': 'abdef','⠼': 'cdef','⠽': 'acdef','⠾': 'bcdef','⠿': 'abcdef','⡀': 'g','⡁': 'ag','⡂': 'bg','⡃': 'abg','⡄': 'cg','⡅': 'acg','⡆': 'bcg','⡇': 'abcg','⡈': 'dg','⡉': 'adg','⡊': 'bdg','⡋': 'abdg','⡌': 'cdg','⡍': 'acdg','⡎': 'bcdg','⡏': 'abcdg','⡐': 'eg','⡑': 'aeg','⡒': 'beg','⡓': 'abeg','⡔': 'ceg','⡕': 'aceg','⡖': 'bceg','⡗': 'abceg','⡘': 'deg','⡙': 'adeg','⡚': 'bdeg','⡛': 'abdeg','⡜': 'cdeg','⡝': 'acdeg','⡞': 'bcdeg','⡟': 'abcdeg','⡠': 'fg','⡡': 'afg','⡢': 'bfg','⡣': 'abfg','⡤': 'cfg','⡥': 'acfg','⡦': 'bcfg','⡧': 'abcfg','⡨': 'dfg','⡩': 'adfg','⡪': 'bdfg','⡫': 'abdfg','⡬': 'cdfg','⡭': 'acdfg','⡮': 'bcdfg','⡯': 'abcdfg','⡰': 'efg','⡱': 'aefg','⡲': 'befg','⡳': 'abefg','⡴': 'cefg','⡵': 'acefg','⡶': 'bcefg','⡷': 'abcefg','⡸': 'defg','⡹': 'adefg','⡺': 'bdefg','⡻': 'abdefg','⡼': 'cdefg','⡽': 'acdefg','⡾': 'bcdefg','⡿': 'abcdefg','⢀': 'h','⢁': 'ah','⢂': 'bh','⢃': 'abh','⢄': 'ch','⢅': 'ach','⢆': 'bch','⢇': 'abch','⢈': 'dh','⢉': 'adh','⢊': 'bdh','⢋': 'abdh','⢌': 'cdh','⢍': 'acdh','⢎': 'bcdh','⢏': 'abcdh','⢐': 'eh','⢑': 'aeh','⢒': 'beh','⢓': 'abeh','⢔': 'ceh','⢕': 'aceh','⢖': 'bceh','⢗': 'abceh','⢘': 'deh','⢙': 'adeh','⢚': 'bdeh','⢛': 'abdeh','⢜': 'cdeh','⢝': 'acdeh','⢞': 'bcdeh','⢟': 'abcdeh','⢠': 'fh','⢡': 'afh','⢢': 'bfh','⢣': 'abfh','⢤': 'cfh','⢥': 'acfh','⢦': 'bcfh','⢧': 'abcfh','⢨': 'dfh','⢩': 'adfh','⢪': 'bdfh','⢫': 'abdfh','⢬': 'cdfh','⢭': 'acdfh','⢮': 'bcdfh','⢯': 'abcdfh','⢰': 'efh','⢱': 'aefh','⢲': 'befh','⢳': 'abefh','⢴': 'cefh','⢵': 'acefh','⢶': 'bcefh','⢷': 'abcefh','⢸': 'defh','⢹': 'adefh','⢺': 'bdefh','⢻': 'abdefh','⢼': 'cdefh','⢽': 'acdefh','⢾': 'bcdefh','⢿': 'abcdefh','⣀': 'gh','⣁': 'agh','⣂': 'bgh','⣃': 'abgh','⣄': 'cgh','⣅': 'acgh','⣆': 'bcgh','⣇': 'abcgh','⣈': 'dgh','⣉': 'adgh','⣊': 'bdgh','⣋': 'abdgh','⣌': 'cdgh','⣍': 'acdgh','⣎': 'bcdgh','⣏': 'abcdgh','⣐': 'egh','⣑': 'aegh','⣒': 'begh','⣓': 'abegh','⣔': 'cegh','⣕': 'acegh','⣖': 'bcegh','⣗': 'abcegh','⣘': 'degh','⣙': 'adegh','⣚': 'bdegh','⣛': 'abdegh','⣜': 'cdegh','⣝': 'acdegh','⣞': 'bcdegh','⣟': 'abcdegh','⣠': 'fgh','⣡': 'afgh','⣢': 'bfgh','⣣': 'abfgh','⣤': 'cfgh','⣥': 'acfgh','⣦': 'bcfgh','⣧': 'abcfgh','⣨': 'dfgh','⣩': 'adfgh','⣪': 'bdfgh','⣫': 'abdfgh','⣬': 'cdfgh','⣭': 'acdfgh','⣮': 'bcdfgh','⣯': 'abcdfgh','⣰': 'efgh','⣱': 'aefgh','⣲': 'befgh','⣳': 'abefgh','⣴': 'cefgh','⣵': 'acefgh','⣶': 'bcefgh','⣷': 'abcefgh','⣸': 'defgh','⣹': 'adefgh','⣺': 'bdefgh','⣻': 'abdefgh','⣼': 'cdefgh','⣽': 'acdefgh','⣾': 'bcdefgh','⣿': 'abcdefgh'};

const LANGUAGES = ['English','Tamil','Hindi','French','Spanish','German','Japanese','Arabic','Portuguese','Italian'];
const TABS = ['unicode','image','camera','batch'];

export default function Converter() {
  const [activeTab, setActiveTab] = useState('unicode');
  const [unicodeBraille, setUnicodeBraille] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [audioPlaying, setAudioPlaying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [step, setStep] = useState(0);

  const STEPS = ['Detecting Braille dots...', 'Decoding characters...', 'Translating text...', 'Ready!'];

  const decodeBrailleText = (text) =>
    text.split('').map((char) => decodeBraille[char] ?? char).join('');

  const handleConvert = async () => {
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
      setResult({ decodedText, translatedText, confidence: confidence || 0.95, lang: selectedLanguage });
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleSpeak = () => {
    if (!result?.translatedText) return;
    if (audioPlaying) { window.speechSynthesis.cancel(); setAudioPlaying(false); return; }
    const utterance = new SpeechSynthesisUtterance(result.translatedText);
    const langMap = { Tamil: 'ta-IN', Hindi: 'hi-IN', French: 'fr-FR', Spanish: 'es-ES', German: 'de-DE', Japanese: 'ja-JP', Arabic: 'ar-SA', Portuguese: 'pt-PT', Italian: 'it-IT' };
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
          <a href="/" style={{ textDecoration: 'none', color: 'inherit' }} className="flex items-center gap-2.5 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>B</div>
            <span className="font-bold text-lg" style={{ letterSpacing: '-0.02em' }}>Braille<span style={{ color: 'var(--accent)' }}>Speak</span></span>
          </a>
          <div className="flex items-center gap-3">
            <select value={selectedLanguage} onChange={e => setSelectedLanguage(e.target.value)}
              className="text-xs px-3 py-1.5 rounded-lg font-medium"
              style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', cursor: 'pointer' }}>
              {LANGUAGES.map(l => <option key={l}>{l}</option>)}
            </select>
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
                <button key={t} onClick={() => setActiveTab(t)} className={'tab-pill flex-1 ' + (activeTab === t ? 'active' : '')}>
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
                  <textarea
                    value={unicodeBraille}
                    onChange={e => { setUnicodeBraille(e.target.value); setError(''); }}
                    placeholder="Paste Braille Unicode here... (e.g. ⠓⠑⠇⠇⠕)"
                    className="flex-1 resize-none outline-none text-2xl tracking-widest leading-loose"
                    style={{ background: 'transparent', color: 'var(--accent)', fontFamily: 'monospace' }}
                  />
                  <div className="pt-3 border-t text-xs" style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}>
                    {unicodeBraille.length} characters
                  </div>
                </div>
              )}
              {activeTab === 'image' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">Image / PDF Upload</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
              {activeTab === 'camera' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">Live Camera Capture</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
              {activeTab === 'batch' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <p className="text-sm font-semibold mb-1">Batch Processing</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
            </div>

            <button onClick={handleConvert} disabled={loading || !unicodeBraille.trim()} className="btn-primary py-3 text-sm flex items-center justify-center gap-2" style={{ opacity: loading || !unicodeBraille.trim() ? 0.6 : 1 }}>
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
                {result && (
                  <button onClick={handleCopy} className="text-xs font-medium px-2.5 py-1 rounded-lg" style={{ background: 'var(--surface2)', color: 'var(--muted)' }}>
                    {copied ? '✓ Copied' : 'Copy Text'}
                  </button>
                )}
              </div>
              {loading ? (
                <div className="flex flex-col gap-3">
                  {STEPS.slice(0,3).map((s, i) => (
                    <div key={s} className="flex items-center gap-2.5">
                      {i < step
                        ? <span className="text-green-500 text-sm">✓</span>
                        : i === step
                          ? <div className="spinner" style={{ borderTopColor: 'var(--accent)', borderColor: 'rgba(108,78,242,0.2)' }} />
                          : <div className="w-4 h-4 rounded-full" style={{ background: 'var(--surface2)' }} />}
                      <span className="text-xs" style={{ color: i <= step ? 'var(--text)' : 'var(--muted)' }}>{s}</span>
                    </div>
                  ))}
                </div>
              ) : result ? (
                <div className="space-y-3">
                  <div>
                    <p className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Decoded</p>
                    <p className="text-sm font-mono" style={{ color: 'var(--muted)' }}>{result.decodedText}</p>
                  </div>
                  <div>
                    <p className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Translated ({result.lang})</p>
                    <p className="text-sm leading-relaxed font-medium">{result.translatedText}</p>
                  </div>
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
                <span className="text-sm font-bold" style={{ color: result ? '#22c55e' : 'var(--muted)' }}>
                  {result ? Math.round(result.confidence * 100) + '%' : '-'}
                </span>
              </div>
              <div className="confidence-track">
                <div className="confidence-fill" style={{ width: result ? (result.confidence * 100) + '%' : '0%' }} />
              </div>
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
                <button onClick={handleSpeak} disabled={!result}
                  className="btn-primary w-10 h-10 flex items-center justify-center p-0 flex-shrink-0"
                  style={{ borderRadius: '10px', opacity: result ? 1 : 0.4, fontSize: '16px' }}>
                  {audioPlaying ? '⏸' : '▶'}
                </button>
                <div className="flex-1 flex items-end gap-px h-8">
                  {Array.from({ length: 40 }).map((_, i) => {
                    const h = Math.sin(i * 0.5) * 40 + 50;
                    return <div key={i} className={'wave-bar flex-1 ' + (audioPlaying && result ? 'active' : '')} style={{ height: h + '%', animationDelay: (i * 0.04) + 's' }} />;
                  })}
                </div>
              </div>
            </div>

            <div className="card p-4">
              <p className="text-xs font-semibold mb-3" style={{ color: 'var(--muted)' }}>TRANSLATE TO</p>
              <div className="flex flex-wrap gap-1.5">
                {LANGUAGES.map(l => (
                  <button key={l} onClick={() => setSelectedLanguage(l)} className={'lang-chip ' + (selectedLanguage === l ? 'active' : '')}>{l}</button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
"""

path = r"C:\Users\dell\OneDrive\Desktop\Braille to speech\app\dashboard\converter.tsx"
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")