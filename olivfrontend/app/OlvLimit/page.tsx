import Image from "next/image";


interface Product {
  name: string;
  tagline: string; 
  desc: string;
  stats: {
    polyphenol: string;
    acidity: string;
    origin: string;
  };
  price: string; 
  link: string; 
  image: string; //Added for typescript 

}


export default function () {
	//Define all the components for the page to appear on the Frontend of the page.
	//Defined as const List of components

	const products: Product[] = [
		{
			name: "Green Machine",
			tagline: "For a health boost",
			desc: "Ultra-high polyphenol, maximum functional depth. Harvested early when olives are green and hard.",
			stats: { polyphenol: "1378 mg/kg",
				acidity:"0.22%",origin: "Puglia,IT"},
			price: "€23",
			link: "https://www.olvlimits.com/products/green-machine",
      image: "/images/olvlimits/GreenMachine.avif"
			},
		{
      name: "Green Queen",
      tagline: "For finishing meals",
      desc: "Balanced polyphenols, everyday nourishment. A flavor bomb designed to finish your dishes.",
      stats: { polyphenol: "371 mg/kg", acidity: "0.20%", origin: "Spain/Italy" },
      price: "€21",
      link: "https://www.olvlimits.com/products/green-queen",
      image: "/images/olvlimits/GreenQueen.avif"
    },
    {
      name: "Yellow Mellow",
      tagline: "For daily cooking",
      desc: "Mellow in flavor, heat-resistant, and perfect for roasting, baking, and warm dishes.",
      stats: { polyphenol: "404 mg/kg", acidity: "0.18%", origin: "Spain" },
      price: "€18",
      link: "https://www.olvlimits.com/products/yellow-mellow",
      image: "/images/olvlimits/YellowMellow.avif"
    }
	];

	return (
		<main className="min-h-screen bg-black text-white p-6 md:p-12 max-w-7xl mx-auto flex flex-col gap-24">
      
      {/* Brand Header */}
      <nav className="flex justify-between items-end border-b border-zinc-800 pb-6">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold tracking-[0.3em] uppercase text-zinc-500">Brand Discovery</span>
          <h1 className="font-bold tracking-tighter text-4xl">OLVLIMITS</h1>
        </div>
        <div className="hidden md:block text-[10px] font-bold tracking-widest uppercase text-zinc-500">
          Amsterdam, NL • Puglia, IT
        </div>
      </nav>

      {/* Hero: The Mission */}
      <section className="max-w-3xl">
        <h2 className="text-5xl md:text-7xl font-bold tracking-tighter leading-[0.85] mb-8">
          NOT ALL OLIVE <br /> OILS ARE EQUAL.
        </h2>
        <p className="text-xl text-zinc-400 leading-relaxed italic border-l border-zinc-700 pl-8">
          "After realizing that 90% of supermarket olive oils are low in health-supporting polyphenols, 
          we made it our mission to provide access to lab-tested, fresh, single-source oil."
        </p>
      </section>

      {/* Product Grid */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {products.map((product: Product, i: number) => (
          <div key={i} className="flex flex-col gap-6 border border-zinc-800 p-8 hover:border-zinc-500 transition-colors group">
            
            {/* Bottle Image Container */}
            <div className="relative aspect-[4/5] w-full bg-zinc-900/30 mb-4 overflow-hidden flex items-center justify-center border border-zinc-800/50">
              <Image 
                src={product.image}
                alt={product.name}
                fill
                sizes="(max-width: 768px) 100vw, 33vw"
                className="object-contain p-8 group-hover:scale-110 transition-transform duration-500 ease-in-out"
                priority={i === 0} // Loads the first image faster
              />
              <div className="absolute top-3 right-3 bg-black/40 backdrop-blur-md border border-white/10 px-2 py-0.5 rounded-sm">
                 <span className="text-[8px] font-bold tracking-widest text-zinc-300 uppercase">Lab Verified</span>
              </div>
            </div>

            <div className="flex justify-between items-start">
              <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-zinc-500">
                {product.tagline}
              </span>
              <span className="font-medium text-lg">{product.price}</span>
            </div>
            
            <h3 className="text-3xl font-bold tracking-tighter uppercase">{product.name}</h3>
            <p className="text-sm text-zinc-400 leading-relaxed min-h-[60px]">
              {product.desc}
            </p>

            {/* Lab Markers */}
            <div className="grid grid-cols-2 gap-4 py-6 border-y border-zinc-900">
              <div>
                <p className="text-[9px] uppercase tracking-widest text-zinc-600 mb-1">Polyphenols</p>
                <p className="text-sm font-bold">{product.stats.polyphenol}</p>
              </div>
              <div>
                <p className="text-[9px] uppercase tracking-widest text-zinc-600 mb-1">Acidity</p>
                <p className="text-sm font-bold">{product.stats.acidity}</p>
              </div>
            </div>

            <a 
              href={product.link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 w-full bg-white text-black text-[10px] font-bold py-4 text-center uppercase tracking-widest hover:bg-zinc-200 transition-colors"
            >
              Order Now
            </a>
          </div>
        ))}
      </section>

      {/* Trust & Transparency Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-16 border-t border-zinc-800 pt-16 mb-20">
        <div className="flex flex-col gap-6">
          <span className="text-[10px] font-bold tracking-[0.3em] uppercase text-zinc-500">Transparency</span>
          <h3 className="text-3xl font-bold tracking-tighter uppercase">Verified Lab Results</h3>
          <p className="text-zinc-400 leading-relaxed">
            We third-party lab-test every batch for key quality markers. Every bottle includes 
            a QR code traceable to its origin in Puglia or Spain. 
          </p>
          <div className="flex gap-8 mt-4">
             <div>
                <p className="text-2xl font-bold">4.8/5</p>
                <p className="text-[10px] uppercase tracking-widest text-zinc-500">Trustpilot Score</p>
             </div>
             <div>
                <p className="text-2xl font-bold">100%</p>
                <p className="text-[10px] uppercase tracking-widest text-zinc-500">Fresh Harvest</p>
             </div>
          </div>
        </div>
        
        <div className="bg-zinc-900/50 p-8 rounded-sm border border-zinc-800 flex flex-col justify-center">
          <p className="text-sm text-zinc-300 italic mb-4">
            "We genuinely couldn't find any competing brands that balance health benefits, transparency, and ease of ordering as well as this one does."
          </p>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">— Longevity Enthusiast Review</p>
        </div>
      </section>

    </main>

		);
}