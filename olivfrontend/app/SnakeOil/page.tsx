import Image from "next/image";

export default function SnakeOilPage() {
  const specs = [
    { label: "Polyphenols", value: "600+ mg/kg", detail: "Clinical Grade" },
    { label: "FFA", value: "< 0.3%", detail: "Free Fatty Acids" },
    { label: "Peroxide", value: "< 10 meq/kg", detail: "Oxidation Level" },
    { label: "Origin", value: "Catalonia, Spain", detail: "Single Source" },
  ];

  return (
    <main className="min-h-screen bg-zinc-50 text-black p-6 md:p-12 max-w-6xl mx-auto flex flex-col gap-16 dark:bg-black dark:text-white">
      
      {/* Header Section */}
      <nav className="flex justify-between items-center border-b border-black/10 dark:border-white/10 pb-6">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold tracking-[0.3em] uppercase">SnakeOIL</span>
          <span className="text-[10px] text-zinc-500 uppercase tracking-widest">Protocol Series: 001</span>
        </div>
        <a 
          href="https://blueprint.bryanjohnson.com/products/extra-virgin-olive-oil"
          className="text-[10px] font-bold tracking-[0.2em] uppercase bg-black text-white dark:bg-white dark:text-black px-8 py-3 rounded-full"
        >
          Acquire
        </a>
      </nav>

      {/* Hero Section */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-16">
        <div className="flex flex-col gap-8">
          <h1 className="text-6xl md:text-8xl font-bold tracking-tighter leading-[0.85]">
            SNAKE <br /> OIL
          </h1>
          <div className="flex flex-col gap-4">
            <p className="text-xl font-medium tracking-tight">
              Extra Virgin Olive Oil. Tested for 70+ markers of quality.
            </p>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-md">
              Selected by Bryan Johnson and his medical team. Specifically chosen for high polyphenol 
              content and low oxidation levels to support cardiovascular health and cellular longevity.
            </p>
          </div>
          
          {/* Technical Specs Table */}
          <div className="mt-4 border-t border-black/5 dark:border-white/5">
            {specs.map((spec, i) => (
              <div key={i} className="flex justify-between py-4 border-b border-black/5 dark:border-white/5">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">{spec.label}</p>
                  <p className="text-sm font-semibold uppercase">{spec.detail}</p>
                </div>
                <p className="text-2xl font-light tracking-tighter">{spec.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Visual / Product Section */}
        <div className="flex flex-col gap-6">
          <div className="aspect-[3/4] bg-zinc-200 dark:bg-zinc-900 flex items-center justify-center border border-black/5 dark:border-white/5">
             <div className="text-[10px] uppercase tracking-[0.4em] text-zinc-400 rotate-90">
                Blueprint / EVOO / 750ML
             </div>
          </div>
          <div className="p-6 bg-zinc-100 dark:bg-zinc-900 border border-black/5">
            <h4 className="text-[10px] font-bold uppercase tracking-widest mb-4">Dosage Recommendation</h4>
            <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              Consume 15mL (1 Tbsp) with every meal. Do not heat above 180°C to preserve 
              molecular integrity of the polyphenols.
            </p>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 py-20 border-t border-black/10">
        <div className="flex flex-col gap-4">
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">01 / Selection</span>
          <p className="text-sm font-medium uppercase leading-tight">Harvested within 2 hours of picking to stop oxidation.</p>
        </div>
        <div className="flex flex-col gap-4">
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">02 / Verification</span>
          <p className="text-sm font-medium uppercase leading-tight">Every batch is third-party lab verified in Spain and USA.</p>
        </div>
        <div className="flex flex-col gap-4">
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">03 / Purpose</span>
          <p className="text-sm font-medium uppercase leading-tight">Optimized for biological age reversal, not just flavor.</p>
        </div>
      </section>

    </main>
  );
}