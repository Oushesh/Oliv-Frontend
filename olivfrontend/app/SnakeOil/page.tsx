import Image from "next/image";

export default function SnakeOilPage() {
  const specs = [
    { label: "Polyphenols", value: "600+ mg/kg", detail: "Clinical Grade" },
    { label: "FFA", value: "< 0.3%", detail: "Free Fatty Acids" },
    { label: "Peroxide", value: "< 10 meq/kg", detail: "Oxidation Level" },
    { label: "Origin", value: "Catalonia, Spain", detail: "Single Source" },
  ];

  return (
    <main className="min-h-screen bg-zinc-50 text-black p-6 md:p-12 max-w-6xl mx-auto flex flex-col gap-16 dark:bg-black dark:text-white font-sans">
      
      {/* Header Section */}
      <nav className="flex justify-between items-center border-b border-black/10 dark:border-white/10 pb-6">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold tracking-[0.3em] uppercase">SnakeOIL</span>
          <span className="text-[10px] text-zinc-500 uppercase tracking-widest">Protocol Series: 001</span>
        </div>
        <a 
          href="https://blueprint.bryanjohnson.com/products/extra-virgin-olive-oil"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[10px] font-bold tracking-[0.2em] uppercase bg-black text-white dark:bg-white dark:text-black px-8 py-3 rounded-full hover:opacity-80 transition-all"
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
            <p className="text-xl font-medium tracking-tight italic">
              "The most important food in my longevity protocol."
            </p>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-md">
              Selected by Bryan Johnson and his medical team. Specifically chosen for high polyphenol 
              content and low oxidation levels to support cardiovascular health and cellular longevity.
            </p>
          </div>
          
          {/* Technical Specs Table */}
          <div className="mt-4 border-t border-black/5 dark:border-white/5">
            {specs.map((spec, i) => (
              <div key={i} className="flex justify-between py-4 border-b border-black/5 dark:border-white/5 group hover:bg-zinc-100 dark:hover:bg-zinc-900 px-2 transition-colors">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">{spec.label}</p>
                  <p className="text-sm font-semibold uppercase">{spec.detail}</p>
                </div>
                <p className="text-2xl font-light tracking-tighter">{spec.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Visual / Product Section with Hover Effect */}
        <div className="flex flex-col gap-6">
          <div className="group relative aspect-[3/4] bg-zinc-200 dark:bg-zinc-900 flex items-center justify-center border border-black/5 dark:border-white/5 overflow-hidden">
            
            {/* The Badge (Top Right) */}
            <div className="absolute top-6 right-6 z-20">
              <div className="bg-black text-white dark:bg-white dark:text-black px-3 py-1.5 rounded-sm flex items-center gap-2 shadow-xl border border-white/20">
                <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                <span className="text-[9px] font-bold tracking-[0.2em] uppercase">Lab Verified</span>
              </div>
            </div>

            {/* Hover Analysis Overlay */}
            <div className="absolute inset-0 z-10 bg-black/80 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-center p-10 text-white">
               <h3 className="text-[10px] font-bold tracking-[0.3em] uppercase mb-6 text-zinc-400">Batch Analysis Report</h3>
               <div className="space-y-4">
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-xs uppercase tracking-widest">Oleocanthal</span>
                    <span className="text-xs font-mono">High-Potency</span>
                  </div>
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-xs uppercase tracking-widest">UV Protection</span>
                    <span className="text-xs font-mono">Dark Glass 100%</span>
                  </div>
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-xs uppercase tracking-widest">Harvest Window</span>
                    <span className="text-xs font-mono">Oct 2025</span>
                  </div>
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-xs uppercase tracking-widest">Purity</span>
                    <span className="text-xs font-mono">99.9% Pure EVOO</span>
                  </div>
               </div>
               <p className="mt-8 text-[9px] text-zinc-500 uppercase leading-relaxed tracking-widest">
                 Certified for biological age reduction protocol. Tested by 3rd party labs in Spain.
               </p>
            </div>

            {/* Placeholder / Bottle Image */}
            <div className="text-[10px] uppercase tracking-[0.4em] text-zinc-400 rotate-90 group-hover:scale-90 transition-transform duration-500">
               Blueprint / EVOO / 750ML
            </div>
            
            {/* If you have the image file, uncomment this: */}
            {/* <Image 
              src="/images/snakeoil.png" 
              alt="SnakeOIL" 
              fill 
              className="object-contain p-12 transition-transform duration-700 group-hover:scale-110"
            /> 
            */}
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
        {[
          { id: "01", label: "Selection", text: "Harvested within 2 hours of picking to stop oxidation." },
          { id: "02", label: "Verification", text: "Every batch is third-party lab verified in Spain and USA." },
          { id: "03", label: "Purpose", text: "Optimized for biological age reversal, not just flavor." }
        ].map((item) => (
          <div key={item.id} className="flex flex-col gap-4 group cursor-default">
            <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 group-hover:text-black dark:group-hover:text-white transition-colors">
              {item.id} / {item.label}
            </span>
            <p className="text-sm font-medium uppercase leading-tight">{item.text}</p>
          </div>
        ))}
      </section>

    </main>
  );
}