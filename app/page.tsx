'use client';
import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

const STATS = [
  { value: '40+', label: 'Languages supported' },
  { value: '99%', label: 'Recognition accuracy' },
  { value: '<2s', label: 'Average convert time' },
  { value: '4', label: 'Input methods' },
];

const FEATURES = [
  { icon: 'ðŸ“„', title: 'Image & PDF Upload', desc: 'Upload scanned Braille documents or images for instant AI-powered recognition and translation.' },
  { icon: 'ðŸ“·', title: 'Live Camera Capture', desc: 'Point your camera at any Braille text for real-time detection and audio playback.' },
  { icon: 'â ¿', title: 'Unicode Paste', desc: 'Paste Braille Unicode characters directly and hear them spoken aloud in your language.' },
  { icon: 'ðŸŒ', title: '40+ Languages', desc: 'Translate converted Braille text into over 40 languages with natural AI voices.' },
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
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg,#6c4ef2,#06b6d4)' }}>â ƒ</div>
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
              {dark ? 'â˜€ï¸' : 'ðŸŒ™'}
            </button>
            <Link href="/sign-in" className="btn-ghost px-4 py-2 text-sm font-medium" style={{ display: 'inline-block', textDecoration: 'none', color: 'var(--muted)' }}>Sign in</Link>
            <Link href="/dashboard" className="btn-primary px-5 py-2 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>Get Started</Link>
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
              Upload images, use your camera, or paste Unicode â€” BrailleSpeak decodes and speaks Braille in 40+ languages with AI accuracy.
            </p>
            <div className="flex items-center gap-3 flex-wrap">
              <Link href="/dashboard" className="btn-primary px-7 py-3 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>
                Try it free â†’
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
                <div className="text-3xl tracking-widest" style={{ color: 'var(--accent)', fontFamily: 'monospace' }}>â “â ‘â ‡â ‡â • â ºâ •â —â ‡â ™</div>
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
                  <button className="btn-primary w-8 h-8 flex items-center justify-center text-xs p-0" style={{ borderRadius: '8px' }}>â–¶</button>
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
          <Link href="/dashboard" className="btn-primary px-10 py-3.5 text-sm" style={{ display: 'inline-block', textDecoration: 'none', borderRadius: '12px' }}>
            Open Converter â†’
          </Link>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t py-6 text-center text-xs" style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}>
        Â© 2025 BrailleSpeak â€” Making Braille accessible to everyone
      </footer>
    </div>
  );
}
