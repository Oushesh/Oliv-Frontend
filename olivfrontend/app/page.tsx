import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto flex flex-col gap-16">
      
      {/* Navigation Header */}
      <nav className="flex justify-between items-center border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <span className="font-bold tracking-tighter text-xl">BLUEPRINT</span>
        <a 
          href="https://blueprint.bryanjohnson.com/products/extra-virgin-olive-oil"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[10px] font-bold tracking-widest uppercase border border-black dark:border-white px-5 py-2 rounded-full hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition-all"
        >
          Shop Now
        </a>
      </nav>

      {/* Hero Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div className="flex flex-col gap-6">
          <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-zinc-500">
            Premium Longevity
          </span>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter leading-[0.9]">
            EXTRA VIRGIN <br /> OLIVE OIL
          </h1>
          <p className="max-w-md text-zinc-600 dark:text-zinc-400 leading-relaxed italic">
            "The most important food for longevity."
          </p>
          <div className="flex gap-4 pt-4">
            <div className="border-l-2 border-black dark:border-white pl-4">
              <p className="text-xs font-bold uppercase tracking-widest">Polyphenols</p>
              <p className="text-2xl font-medium">600+ mg/kg</p>
            </div>
          </div>
        </div>

        <div className="bg-zinc-100 dark:bg-zinc-900 aspect-[4/5] flex items-center justify-center rounded-sm overflow-hidden border border-zinc-200 dark:border-zinc-800">
          <div className="relative w-full h-full p-12">
             {/* Placeholder for Product Image */}
             <div className="w-full h-full bg-zinc-200 dark:bg-zinc-800 animate-pulse rounded-sm flex items-center justify-center text-[10px] tracking-widest text-zinc-400 uppercase">
                Product Image
             </div>
          </div>
        </div>
      </section>

      {/* Details Grid */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t border-zinc-200 dark:border-zinc-800 pt-8">
        {[
          { label: "Origin", value: "Spain" },
          { label: "Harvest", value: "Nov 2023" },
          { label: "Acidity", value: "< 0.2%" },
          { label: "Flavor", value: "Peppery" },
        ].map((item, i) => (
          <div key={i} className="flex flex-col gap-1">
            <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">
              {item.label}
            </span>
            <span className="text-lg font-medium tracking-tight">
              {item.value}
            </span>
          </div>
        ))}
      </section>

    </main>
  );
}

//Add a search Bar to search for a brand name from the list of avaialble brands -->
//Deploy an agent to search harvest date and see if harvest is avaaialble --> 


//Secnario: olvlimits --> 




