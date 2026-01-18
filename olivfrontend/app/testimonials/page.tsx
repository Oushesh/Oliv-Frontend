import Image from "next/image";


//export a default render as tsx react component

export default function Testimonials()
{
	const dataPoints = [
		{ label: "Annual Investment", value: "€2M+" },
    	{ label: "Medical Team", value: "30 Doctors" },
    	{ label: "Age Reduction", value: "5+ Years" },
    	{ label: "Core Nutrient", value: "EVOO" },
	];
	return (
		<main className="min-h-screen bg-black text-white p-6 md:p-12 max-w-6xl mx-auto flex flex-col gap-20">
      
      {/* Navigation Header */}
      <nav className="flex justify-between items-center border-b border-zinc-800 pb-4">
        <a href="/" className="font-bold tracking-tighter text-xl hover:opacity-70 transition-opacity">
          BLUEPRINT
        </a>
        <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-zinc-500">
          Longevity Protocol
        </span>
      </nav>

      {/* Case Study Section */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
        <div className="flex flex-col gap-8">
          <div className="flex flex-col gap-2">
            <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-zinc-500">
              Subject 01: Bryan Johnson
            </span>
            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter leading-tight">
              THE €2M <br /> LONGEVITY PLAN
            </h1>
          </div>

          <p className="text-zinc-400 text-lg leading-relaxed max-w-md">
            Bryan Johnson is working to reverse his biological age through a 
            highly optimized daily protocol. His #1 essential food? 
            Premium Extra Virgin Olive Oil.
          </p>

          <blockquote className="border-l-2 border-white pl-6 my-4">
            <p className="text-xl italic text-zinc-200">
              "Premium Extra Virgin Olive Oil is more powerful than resveratrol, 
              NR, cold plunge, and sauna."
            </p>
            <footer className="mt-2 text-xs font-bold uppercase tracking-widest text-zinc-500">
              — @bryan_johnson
            </footer>
          </blockquote>

          {/* Data Grid */}
          <div className="grid grid-cols-2 gap-8 pt-8 border-t border-zinc-800">
            {dataPoints.map((point, i) => (
              <div key={i}>
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-500 mb-1">
                  {point.label}
                </p>
                <p className="text-2xl font-medium tracking-tight">{point.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Image / Evidence Section */}
        <div className="flex flex-col gap-4">
          <div className="aspect-square bg-zinc-900 border border-zinc-800 relative overflow-hidden flex items-center justify-center group">
             {/* Replace with your Bryan Johnson image */}
             <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
             <div className="text-[10px] uppercase tracking-widest text-zinc-700">
                [ Insert Bryan Johnson Image ]
             </div>
          </div>
          <p className="text-[10px] leading-relaxed text-zinc-500 uppercase tracking-widest">
            Protocol Evidence: 1 Tbsp (15 mL) consumed with every daily meal to 
            support cardiovascular and brain health[cite: 29, 36, 37].
          </p>
        </div>
      </section>

      {/* Trust Markers Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-12 border-t border-zinc-800 pt-16 mb-20">
        <div>
          <h3 className="text-xs font-bold uppercase tracking-[0.3em] mb-4">Verification</h3>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Every drop is lab-tested for polyphenol content. Green Machine 
            delivers 1378 mg/kg—700% more than average oil[cite: 58, 64].
          </p>
        </div>
        <div>
          <h3 className="text-xs font-bold uppercase tracking-[0.3em] mb-4">Global Impact</h3>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Rated 4.8/5 on Trustpilot with thousands of customers across 
            25+ countries[cite: 73, 75, 102].
          </p>
        </div>
        <div>
          <h3 className="text-xs font-bold uppercase tracking-[0.3em] mb-4">Guarantee</h3>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Not satisfied? We offer a 100% money-back guarantee because 
            quality is our only priority[cite: 77].
          </p>
        </div>
      </section>
    </main>
  );	
}