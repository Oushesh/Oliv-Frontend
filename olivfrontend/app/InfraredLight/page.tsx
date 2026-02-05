"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [sessions, setSessions] = useState(0);
  const [mounted, setMounted] = useState(false);

  // Avoid hydration mismatch for stateful UI
  useEffect(() => setMounted(true), []);

  const progress = (sessions / 36) * 100; // Assuming 3 sessions/week for 12 weeks

  return (
    <main className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto flex flex-col gap-16 bg-white dark:bg-black text-black dark:text-white transition-colors duration-500">
      
      {/* Header */}
      <nav className="flex justify-between items-center border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <div className="flex flex-col">
           <span className="font-bold tracking-tighter text-xl uppercase italic">Protocol 660</span>
           <span className="text-[8px] font-mono text-red-600 uppercase tracking-[0.3em]">Mitochondrial Optimization</span>
        </div>
        <div className="flex gap-6 items-center">
           <span className="hidden md:inline text-[10px] font-mono text-zinc-400 uppercase">PMID: 19587693</span>
           <button className="text-[10px] font-bold tracking-widest uppercase border border-black dark:border-white px-5 py-2 rounded-full hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition-all">
             Access Data
           </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div className="flex flex-col gap-6">
          <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-red-600">
            Phase 1: Skin Architecture
          </span>
          <h1 className="text-5xl md:text-8xl font-bold tracking-tighter leading-[0.85] uppercase">
            REVERSE <br /> AGING
          </h1>
          <p className="max-w-md text-zinc-600 dark:text-zinc-400 leading-relaxed border-l border-zinc-200 dark:border-zinc-800 pl-6">
            Upregulating Type-1 Procollagen by <span className="text-black dark:text-white font-bold">+31%</span> using 660nm pulsed photobiomodulation. 
          </p>
        </div>

        {/* Results Tracker Component */}
        <div className="border border-zinc-200 dark:border-zinc-800 p-8 rounded-sm bg-zinc-50 dark:bg-zinc-950 relative overflow-hidden">
          <div className="absolute top-0 left-0 h-[2px] bg-red-600 transition-all duration-1000" style={{ width: `${progress}%` }}></div>
          
          <h3 className="text-[10px] font-bold uppercase tracking-widest mb-6 flex justify-between">
            Protocol Progress <span>{mounted ? Math.round(progress) : 0}%</span>
          </h3>
          <div className="flex items-end gap-2 mb-8">
            <span className="text-7xl font-bold tracking-tighter">{sessions}</span>
            <span className="text-zinc-400 pb-2 text-sm uppercase font-mono">Sessions Completed</span>
          </div>
          
          <button 
            onClick={() => setSessions(prev => prev + 1)}
            className="w-full bg-black dark:bg-white text-white dark:text-black py-4 font-bold uppercase text-[10px] tracking-widest hover:opacity-80 active:scale-[0.98] transition-all"
          >
            Log Session (10 min)
          </button>
          
          <div className="grid grid-cols-2 gap-4 mt-6 pt-6 border-t border-zinc-200 dark:border-zinc-800">
            <div className="flex flex-col">
              <span className="text-[8px] text-zinc-400 uppercase">Target</span>
              <span className="text-xs font-bold uppercase">Dermis (Deep)</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[8px] text-zinc-400 uppercase">Frequency</span>
              <span className="text-xs font-bold uppercase">Sequential Pulse</span>
            </div>
          </div>
        </div>
      </section>

      {/* Buying Guide & FAQ */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-12 border-t border-zinc-200 dark:border-zinc-800 pt-12">
        <div className="space-y-12">
          <div>
            <h2 className="text-xs font-bold tracking-[0.3em] mb-8 uppercase text-zinc-400">Biological FAQ</h2>
            <div className="space-y-8">
              {[
                { q: "Bare skin vs. Products?", a: "Apply on clean, dry skin. Zinc in SPF blocks 660nm light. Apply serums post-session." },
                { q: "Optimal Distance?", a: "6 inches for panels (approx. 50-100 mW/cm²). Masks should sit flush against the dermis." },
                { q: "Frequency?", a: "3-5x per week. Biological 'over-dosing' occurs past 20 minutes, yielding diminishing returns." }
              ].map((faq, i) => (
                <div key={i} className="group">
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-red-600 transition-all group-hover:pl-2">{faq.q}</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-2 leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-zinc-100 dark:bg-zinc-900 p-8 rounded-sm">
          <h2 className="text-xs font-bold tracking-[0.3em] mb-8 uppercase">Hardware Acquisition Checklist</h2>
          <ul className="space-y-6 text-[10px] font-mono uppercase tracking-widest">
            <li className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
              <span className="text-zinc-500 italic">Criteria 01</span>
              <span>660nm ± 5nm Wavelength</span>
            </li>
            <li className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
              <span className="text-zinc-500 italic">Criteria 02</span>
              <span>&gt;50mW/cm² Irradiance</span>
            </li>
            <li className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
              <span className="text-zinc-500 italic">Criteria 03</span>
              <span>Zero Flicker Driver</span>
            </li>
            <li className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
              <span className="text-zinc-500 italic">Criteria 04</span>
              <span>3rd Party Irradiance Map</span>
            </li>
          </ul>
          <div className="mt-8 p-4 border border-red-600/20 bg-red-600/5 text-[9px] text-red-600 leading-relaxed uppercase tracking-tighter">
            Note: If a manufacturer does not list mW/cm² (Irradiance) at specific distances, the device is likely underpowered and will not yield clinical results.
          </div>
        </div>
      </section>

      {/* Biological Visualization */}
      <div className="py-12 border-t border-zinc-200 dark:border-zinc-800">
        <h3 className="text-[10px] font-bold uppercase tracking-widest mb-8">Dermal Penetration Analysis</h3>
        
        <p className="text-[10px] text-zinc-500 mt-6 max-w-xl uppercase tracking-widest leading-relaxed">
          The 660nm wavelength specifically targets the <span className="text-black dark:text-white underline">Mitochondrial Cytochrome C Oxidase</span>, triggering a cascade that increases ATP production and subsequent collagen synthesis.
        </p>
      </div>

      <footer className="mt-auto pt-12 border-t border-zinc-200 dark:border-zinc-800 text-[8px] font-mono text-zinc-400 uppercase tracking-[0.5em] text-center">
        Blueprint System // Ver 1.0.4 // Non-Medical Advice
      </footer>
    </main>
  );
}