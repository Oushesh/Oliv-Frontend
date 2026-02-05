
/*
import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            To get started, edit the page.tsx file.
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Looking for a starting point or more instructions? Head over to{" "}
            <a
              href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Templates
            </a>{" "}
            or the{" "}
            <a
              href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Learning
            </a>{" "}
            center.
          </p>
        </div>
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy Now
          </a>
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
        </div>
      </main>
    </div>
  );
}

Update page.tsx with new Bryan Johnson style borders and fonts
*/

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

        {/* Video Preview Container */}
        <div className="bg-zinc-100 dark:bg-zinc-900 aspect-[4/5] flex items-center justify-center rounded-sm overflow-hidden border border-zinc-200 dark:border-zinc-800 relative">
          <iframe
            className="absolute inset-0 w-full h-full object-cover pointer-events-none scale-[1.2]" 
            src="https://www.youtube.com/embed/bYLkSXq54k4?autoplay=1&mute=1&loop=1&playlist=bYLkSXq54k4&controls=0&showinfo=0&rel=0&start=0&end=15"
            title="Bryan Johnson Olive Oil Preview"
            allow="autoplay; encrypted-media"
            allowFullScreen
          ></iframe>
          {/* Optional Overlay to match the Blueprint "muted" look */}
          <div className="absolute inset-0 bg-black/5 pointer-events-none"></div>
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




