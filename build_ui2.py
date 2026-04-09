import os

os.makedirs('app/converter', exist_ok=True)

# ── globals.css ──────────────────────────────────────────────
globals_css = r"""@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --bg: #f4f6fb;
  --surface: #ffffff;
  --surface2: #f0f2f8;
  --border: #e2e6f0;
  --accent: #6c4ef2;
  --accent2: #06b6d4;
  --text: #0f1123;
  --muted: #8b93a7;
  --shadow: 0 2px 20px rgba(108,78,242,0.08);
  --shadow-md: 0 8px 40px rgba(108,78,242,0.12);
}

.dark {
  --bg: #0b0d1a;
  --surface: #131628;
  --surface2: #1a1e33;
  --border: rgba(255,255,255,0.07);
  --accent: #7c5ef4;
  --accent2: #06b6d4;
  --text: #e8eaf6;
  --muted: #6b7280;
  --shadow: 0 2px 20px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 40px rgba(0,0,0,0.4);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: background 0.3s ease, color 0.3s ease;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: var(--shadow);
  transition: background 0.3s, border 0.3s, box-shadow 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent), #9b7ff8);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(108,78,242,0.35); }
.btn-primary:active { transform: translateY(0); }

.btn-ghost {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.btn-ghost:hover { border-color: var(--accent); color: var(--accent); }

.tab-pill {
  border-radius: 10px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  background: transparent;
  color: var(--muted);
  font-family: inherit;
}
.tab-pill.active {
  background: linear-gradient(135deg, rgba(108,78,242,0.12), rgba(6,182,212,0.08));
  border-color: rgba(108,78,242,0.3);
  color: var(--accent);
  font-weight: 600;
}
.tab-pill:hover:not(.active) { background: var(--surface2); color: var(--text); }

.upload-zone {
  border: 2px dashed var(--border);
  border-radius: 16px;
  transition: all 0.2s;
  cursor: pointer;
}
.upload-zone:hover, .upload-zone.drag { border-color: var(--accent); background: rgba(108,78,242,0.04); }

.confidence-track { background: var(--surface2); border-radius: 99px; height: 6px; }
.confidence-fill {
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border-radius: 99px;
  height: 100%;
  transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
}

.lang-chip {
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--muted);
  transition: all 0.2s;
  font-family: inherit;
}
.lang-chip.active { background: var(--accent); border-color: var(--accent); color: white; }
.lang-chip:hover:not(.active) { border-color: var(--accent); color: var(--accent); }

.dot-badge {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}

/* Audio waveform bars */
.wave-bar {
  width: 3px;
  border-radius: 99px;
  background: var(--accent);
  opacity: 0.4;
  animation: wave 1.2s ease-in-out infinite;
}
.wave-bar.active { opacity: 1; }
@keyframes wave {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}

/* Progress spinner */
.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Scroll fade */
.fade-up { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-up.visible { opacity: 1; transform: none; }

/* Nav blur */
.nav-blur {
  backdrop-filter: blur(12px);
  background: rgba(244,246,251,0.85);
  border-bottom: 1px solid var(--border);
  transition: background 0.3s, border 0.3s;
}
.dark .nav-blur {
  background: rgba(11,13,26,0.85);
}

/* Braille dot grid bg (subtle) */
.dot-grid {
  background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
  background-size: 24px 24px;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 99px; opacity: 0.5; }

select option { background: var(--surface); color: var(--text); }
"""

# ── layout.tsx ──────────────────────────────────────────────
layout_tsx = r"""import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BrailleSpeak",
  description: "Braille to Speech — feel words, hear worlds",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
"""

# ── app/page.tsx ─────────────────────────────────────────────
page_tsx = r"""'use client';
import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

const STATS = [
  { value: '40+', label: 'Languages supported' },
  { value: '99%', label: 'Recognition accuracy' },
  { value: '<2s', label: 'Average convert time' },
  { value: '4', label: 'Input methods' },
];

const FEATURES = [
  { icon: '📄', title: 'Image & PDF Upload', desc: 'Upload scanned Braille documents or images for instant AI-powered recognition and translation.' },
  { icon: '📷', title: 'Live Camera Capture', desc: 'Point your camera at any Braille text for real-time detection and audio playback.' },
  { icon: '⠿', title: 'Unicode Paste', desc: 'Paste Braille Unicode characters directly and hear them spoken aloud in your language.' },
  { icon: '🌐', title: '40+ Languages', desc: 'Translate converted Braille text into over 40 languages with natural AI voices.' },
];

export default function Home() {
  const [dark, setDark] = useState(false);
  const fadeRefs = useRef<HTMLElement[]>([]);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  useEffect(() => {
    const obs = new IntersectionObserver(entries =>
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.12 }
    );
    fadeRefs.current.forEach(el => el && obs.observe(el));
    return () => obs.disconnect();
  }, []);

  const r = (el: HTMLElement | null) => { if (el && !fadeRefs.current.includes(el)) fadeRefs.current.push(el); };

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)', color: 'var(--text)' }}>
      {/* NAV */}
      <nav className="nav-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>⠃</div>
            <span className="font-bold text-lg" style={{ letterSpacing: '-0.02em' }}>
              Braille<span style={{ color: 'var(--accent)' }}>Speak</span>
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium" style={{ color: 'var(--muted)' }}>
            <a href="#features" className="hover:text-current transition-colors">Features</a>
            <a href="#how" className="hover:text-current transition-colors">How it Works</a>
            <a href="#" className="hover:text-current transition-colors">About</a>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => setDark(!dark)} className="btn-ghost w-9 h-9 flex items-center justify-center text-base p-0" style={{ borderRadius: '10px' }}>
              {dark ? '☀️' : '🌙'}
            </button>
            <Link href="/sign-in" className="btn-ghost px-4 py-2 text-sm font-medium" style={{ display: 'inline-block', textDecoration: 'none', color: 'var(--muted)' }}>Sign in</Link>
            <Link href="/converter" className="btn-primary px-5 py-2 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>Get Started</Link>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="max-w-6xl mx-auto px-6 pt-24 pb-20">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-6" style={{ background: 'rgba(108,78,242,0.1)', color: 'var(--accent)', border: '1px solid rgba(108,78,242,0.2)' }}>
              <span className="dot-badge" style={{ background: 'var(--accent)' }} />
              AI-Powered Braille Recognition
            </div>
            <h1 className="text-5xl font-extrabold leading-tight mb-5" style={{ letterSpacing: '-0.03em' }}>
              Convert Braille<br />
              to Speech <span style={{ color: 'var(--accent)' }}>instantly</span>
            </h1>
            <p className="text-lg mb-8 leading-relaxed" style={{ color: 'var(--muted)' }}>
              Upload images, use your camera, or paste Unicode — BrailleSpeak decodes and speaks Braille in 40+ languages with AI accuracy.
            </p>
            <div className="flex items-center gap-3 flex-wrap">
              <Link href="/converter" className="btn-primary px-7 py-3 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>
                Try it free →
              </Link>
              <Link href="/sign-up" className="btn-ghost px-7 py-3 text-sm font-medium" style={{ display: 'inline-block', textDecoration: 'none' }}>
                Create account
              </Link>
            </div>
          </div>

          {/* Hero card preview */}
          <div className="card p-6 dot-grid relative overflow-hidden">
            <div className="absolute inset-0 opacity-30" style={{ background: 'radial-gradient(ellipse at top right, rgba(108,78,242,0.15), transparent 60%)' }} />
            <div className="relative">
              <div className="card p-4 mb-4" style={{ background: 'var(--surface2)' }}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="dot-badge" style={{ background: '#6c4ef2' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>Braille Input</span>
                </div>
                <div className="text-3xl tracking-widest" style={{ color: 'var(--accent)', fontFamily: 'monospace' }}>⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙</div>
              </div>
              <div className="flex gap-3 mb-4">
                <div className="card p-3 flex-1 text-center" style={{ background: 'var(--surface2)' }}>
                  <div className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Detected</div>
                  <div className="text-sm font-bold">Grade 1</div>
                </div>
                <div className="card p-3 flex-1 text-center" style={{ background: 'var(--surface2)' }}>
                  <div className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Confidence</div>
                  <div className="text-sm font-bold" style={{ color: '#22c55e' }}>98%</div>
                </div>
                <div className="card p-3 flex-1 text-center" style={{ background: 'var(--surface2)' }}>
                  <div className="text-xs mb-1" style={{ color: 'var(--muted)' }}>Language</div>
                  <div className="text-sm font-bold">English</div>
                </div>
              </div>
              <div className="card p-4" style={{ background: 'rgba(108,78,242,0.06)', border: '1px solid rgba(108,78,242,0.15)' }}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="dot-badge" style={{ background: '#22c55e' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>Translation</span>
                </div>
                <p className="text-sm font-medium">"Hello World"</p>
                <div className="flex items-center gap-2 mt-3">
                  <button className="btn-primary w-8 h-8 flex items-center justify-center text-xs p-0" style={{ borderRadius: '8px' }}>▶</button>
                  <div className="flex-1 flex items-end gap-0.5 h-6">
                    {[3,5,8,5,9,6,4,7,5,8,4,6,9,5,3].map((h,i) => (
                      <div key={i} className="wave-bar" style={{ height: `${h * 3}px`, animationDelay: `${i * 0.08}s` }} />
                    ))}
                  </div>
                  <span className="text-xs" style={{ color: 'var(--muted)' }}>0:02</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* STATS */}
      <section ref={r} className="fade-up max-w-5xl mx-auto px-6 pb-20">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {STATS.map(s => (
            <div key={s.label} className="card p-6 text-center">
              <div className="text-3xl font-extrabold mb-1" style={{ color: 'var(--accent)', letterSpacing: '-0.02em' }}>{s.value}</div>
              <div className="text-xs font-medium" style={{ color: 'var(--muted)' }}>{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" ref={r} className="fade-up max-w-5xl mx-auto px-6 pb-24">
        <h2 className="text-3xl font-bold text-center mb-2" style={{ letterSpacing: '-0.02em' }}>Everything you need</h2>
        <p className="text-center mb-10 text-sm" style={{ color: 'var(--muted)' }}>Four powerful input methods, one seamless experience</p>
        <div className="grid md:grid-cols-2 gap-4">
          {FEATURES.map(f => (
            <div key={f.title} className="card p-6 flex gap-4 group hover:border-purple-300 transition-all" style={{ borderColor: 'var(--border)' }}>
              <div className="text-2xl flex-shrink-0">{f.icon}</div>
              <div>
                <h3 className="font-semibold mb-1.5 text-sm">{f.title}</h3>
                <p className="text-xs leading-relaxed" style={{ color: 'var(--muted)' }}>{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section ref={r} className="fade-up max-w-2xl mx-auto px-6 pb-24 text-center">
        <div className="card p-12" style={{ background: 'linear-gradient(135deg, rgba(108,78,242,0.08), rgba(6,182,212,0.04))' }}>
          <h2 className="text-3xl font-bold mb-3" style={{ letterSpacing: '-0.02em' }}>Start converting today</h2>
          <p className="mb-8 text-sm" style={{ color: 'var(--muted)' }}>No credit card required. Free to use.</p>
          <Link href="/converter" className="btn-primary px-10 py-3.5 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>
            Open Converter →
          </Link>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t py-6 text-center text-xs" style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}>
        © 2025 BrailleSpeak — Making Braille accessible to everyone
      </footer>
    </div>
  );
}
"""

# ── app/converter/page.tsx ───────────────────────────────────
converter_tsx = r"""'use client';
import { useState, useRef, useEffect } from 'react';

const TABS = [
  { id: 'image', label: 'Image / PDF', icon: '📄' },
  { id: 'camera', label: 'Camera', icon: '📷' },
  { id: 'unicode', label: 'Unicode', icon: '⠿' },
  { id: 'batch', label: 'Batch', icon: '📦' },
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
  const [playing, setPlaying] = useState(false);
  const [step, setStep] = useState(0);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const STEPS = ['Detecting Braille dots...', 'Decoding characters...', 'Translating text...', 'Generating audio...'];

  const handleConvert = async () => {
    setLoading(true);
    setOutput('');
    setConfidence(0);
    setStep(0);
    for (let i = 0; i < STEPS.length; i++) {
      setStep(i);
      await new Promise(r => setTimeout(r, 600));
    }
    setOutput('Hello World! This is a sample converted output. Connect your APIs to get real Braille translation here.');
    setConfidence(98);
    setLoading(false);
  };

  const handleFile = (file: File) => setFileName(file.name);

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)', color: 'var(--text)' }}>
      {/* NAV */}
      <nav className="nav-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2.5 hover:opacity-80 transition-opacity" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>⠃</div>
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
              {dark ? '☀️' : '🌙'}
            </button>
            <a href="/sign-in" className="btn-ghost px-4 py-2 text-xs font-medium" style={{ textDecoration: 'none', display: 'inline-block' }}>Sign in</a>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-1" style={{ letterSpacing: '-0.02em' }}>Braille Converter</h1>
          <p className="text-sm" style={{ color: 'var(--muted)' }}>Upload, capture, or paste Braille — get instant speech output</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-5">
          {/* LEFT */}
          <div className="flex flex-col gap-4">
            {/* Tabs */}
            <div className="card p-1.5 flex gap-1">
              {TABS.map(t => (
                <button key={t.id} onClick={() => setTab(t.id)}
                  className={`tab-pill flex-1 flex items-center justify-center gap-1.5 ${tab === t.id ? 'active' : ''}`}>
                  <span>{t.icon}</span>
                  <span className="hidden sm:inline">{t.label}</span>
                </button>
              ))}
            </div>

            {/* Input */}
            <div className="card flex-1" style={{ minHeight: '300px' }}>
              {tab === 'image' && (
                <div
                  className={`upload-zone h-full flex flex-col items-center justify-center p-8 m-3 rounded-xl ${drag ? 'drag' : ''}`}
                  style={{ minHeight: '260px' }}
                  onDragOver={e => { e.preventDefault(); setDrag(true); }}
                  onDragLeave={() => setDrag(false)}
                  onDrop={e => { e.preventDefault(); setDrag(false); const f = e.dataTransfer.files[0]; if (f) handleFile(f); }}
                  onClick={() => fileRef.current?.click()}
                >
                  <input ref={fileRef} type="file" accept="image/*,.pdf" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
                  <div className="text-4xl mb-3">{fileName ? '✅' : '📄'}</div>
                  {fileName ? (
                    <>
                      <p className="text-sm font-semibold mb-1" style={{ color: 'var(--accent)' }}>{fileName}</p>
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>Click to change</p>
                    </>
                  ) : (
                    <>
                      <p className="text-sm font-semibold mb-1">Drop image or PDF here</p>
                      <p className="text-xs" style={{ color: 'var(--muted)' }}>or click to browse — PNG, JPG, PDF supported</p>
                    </>
                  )}
                </div>
              )}

              {tab === 'camera' && (
                <div className="h-full flex flex-col items-center justify-center p-8" style={{ minHeight: '300px' }}>
                  <div className="text-4xl mb-4">📷</div>
                  <p className="text-sm font-semibold mb-1">Live Camera Capture</p>
                  <p className="text-xs mb-5" style={{ color: 'var(--muted)' }}>Point your camera at Braille text</p>
                  <button className="btn-primary px-6 py-2.5 text-sm">Enable Camera</button>
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
                    placeholder="⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙"
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
                  <div className="text-4xl mb-4">📦</div>
                  <p className="text-sm font-semibold mb-1">Batch Processing</p>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Coming soon</p>
                </div>
              )}
            </div>

            <button onClick={handleConvert} disabled={loading} className="btn-primary py-3 text-sm flex items-center justify-center gap-2">
              {loading ? <><div className="spinner" /> {STEPS[step]}</> : '🔊 Convert & Speak →'}
            </button>
          </div>

          {/* RIGHT */}
          <div className="flex flex-col gap-4">
            {/* Output */}
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
                  {STEPS.map((s, i) => (
                    <div key={s} className="flex items-center gap-2.5">
                      {i < step ? (
                        <span className="text-green-500 text-sm">✓</span>
                      ) : i === step ? (
                        <div className="spinner" style={{ borderTopColor: 'var(--accent)', borderColor: 'rgba(108,78,242,0.2)' }} />
                      ) : (
                        <div className="w-4 h-4 rounded-full" style={{ background: 'var(--surface2)' }} />
                      )}
                      <span className="text-xs" style={{ color: i <= step ? 'var(--text)' : 'var(--muted)' }}>{s}</span>
                    </div>
                  ))}
                </div>
              ) : output ? (
                <p className="text-sm leading-relaxed">{output}</p>
              ) : (
                <div className="flex flex-col items-center justify-center h-32 text-center">
                  <div className="text-3xl mb-2 opacity-20">⠿</div>
                  <p className="text-xs" style={{ color: 'var(--muted)' }}>Converted text will appear here</p>
                </div>
              )}
            </div>

            {/* Confidence */}
            <div className="card p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>CONFIDENCE SCORE</span>
                <span className="text-sm font-bold" style={{ color: confidence > 0 ? '#22c55e' : 'var(--muted)' }}>{confidence > 0 ? `${confidence}%` : '—'}</span>
              </div>
              <div className="confidence-track">
                <div className="confidence-fill" style={{ width: `${confidence}%` }} />
              </div>
            </div>

            {/* Audio player */}
            <div className="card p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="dot-badge" style={{ background: playing ? '#6c4ef2' : 'var(--muted)' }} />
                  <span className="text-xs font-semibold" style={{ color: 'var(--muted)' }}>AUDIO OUTPUT</span>
                </div>
                <span className="text-xs" style={{ color: 'var(--muted)' }}>{lang}</span>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setPlaying(!playing)}
                  disabled={!output}
                  className="btn-primary w-10 h-10 flex items-center justify-center p-0 flex-shrink-0"
                  style={{ borderRadius: '10px', opacity: output ? 1 : 0.4 }}>
                  {playing ? '⏸' : '▶'}
                </button>
                <div className="flex-1 flex items-end gap-px h-8">
                  {Array.from({ length: 40 }).map((_, i) => {
                    const h = Math.sin(i * 0.5) * 40 + 50;
                    return (
                      <div key={i} className={`wave-bar flex-1 ${playing && output ? 'active' : ''}`}
                        style={{ height: `${h}%`, animationDelay: `${i * 0.04}s` }} />
                    );
                  })}
                </div>
                <button disabled={!output} className="btn-ghost w-8 h-8 flex items-center justify-center p-0 text-sm" style={{ opacity: output ? 1 : 0.4 }}>⬇</button>
              </div>
            </div>

            {/* Language chips */}
            <div className="card p-4">
              <p className="text-xs font-semibold mb-3" style={{ color: 'var(--muted)' }}>TRANSLATE TO</p>
              <div className="flex flex-wrap gap-1.5">
                {LANGUAGES.map(l => (
                  <button key={l} onClick={() => setLang(l)} className={`lang-chip ${lang === l ? 'active' : ''}`}>{l}</button>
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

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(globals_css)
with open('app/layout.tsx', 'w', encoding='utf-8') as f:
    f.write(layout_tsx)
with open('app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(page_tsx)
with open('app/converter/page.tsx', 'w', encoding='utf-8') as f:
    f.write(converter_tsx)

print('All files written!')