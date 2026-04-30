export default function Home() {
  const participants = [
    "Niko Grbic",
    "Mona J Kang",
    "John Cassar",
    "Mocorram Hussain",
    "Philipp",
    "My brother",
    "My mother",
    "My father",
  ];

  const biomarkers = [
    {
      name: "oxLDL",
      label: "Oxidised LDL",
      baseline: "88 U/L",
      current: "67 U/L",
      target: "< 60 U/L",
      status: "Improving",
    },
    {
      name: "ApoB",
      label: "Apolipoprotein B",
      baseline: "112 mg/dL",
      current: "89 mg/dL",
      target: "< 80 mg/dL",
      status: "On Track",
    },
    {
      name: "hs-CRP",
      label: "Inflammation marker",
      baseline: "2.1 mg/L",
      current: "1.2 mg/L",
      target: "< 1.0 mg/L",
      status: "Improving",
    },
  ];

  const brandOptions = [
    { name: "OlivLimits", useCase: "High polyphenol baseline protocol" },
    { name: "Alya Oil", useCase: "Balanced daily use" },
    { name: "Getsolio", useCase: "Entry price optimization" },
  ];

  const testPlan = [
    { step: "Test 1", detail: "Baseline panel (LDL, HDL, ApoB, hs-CRP, oxLDL)", cost: "100 EUR" },
    { step: "8 Weeks", detail: "Follow EVOO protocol + adherence tracking", cost: "Included" },
    { step: "Test 2", detail: "Post-cycle panel to measure delta", cost: "100 EUR" },
  ];

  return (
    <main className="min-h-screen bg-black text-white p-6 md:p-12 max-w-7xl mx-auto flex flex-col gap-20">
      <nav className="flex justify-between items-end border-b border-zinc-800 pb-6">
        <div className="flex flex-col gap-2">
          <span className="text-[10px] font-bold tracking-[0.3em] uppercase text-zinc-500">
            Community Build Up
          </span>
          <h1 className="font-bold tracking-tighter text-4xl md:text-5xl">LONGEVITY TRACKER</h1>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-bold tracking-widest uppercase text-zinc-500">Target cohort</p>
          <p className="text-xl font-bold">20+ Participants</p>
        </div>
      </nav>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
        <div className="flex flex-col gap-8">
          <h2 className="text-5xl md:text-7xl font-bold tracking-tighter leading-[0.85]">
            TRACK oxLDL, ApoB,
            <br />
            AND hs-CRP
          </h2>
          <p className="text-zinc-400 leading-relaxed text-lg max-w-xl">
            A premium protocol dashboard inspired by Bryan Johnson style biomarker delivery. Users sign in,
            select EVOO brand strategy, choose tests from Germany/EU labs, and monitor measurable progress.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { k: "Baseline + Post", v: "2 Tests" },
              { k: "Estimated Cost", v: "200 EUR / person" },
              { k: "12-Month Goal", v: "Retention + outcomes" },
            ].map((item) => (
              <div key={item.k} className="border border-zinc-800 p-4">
                <p className="text-[10px] uppercase tracking-widest text-zinc-500">{item.k}</p>
                <p className="text-xl font-bold mt-2">{item.v}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="border border-zinc-800 bg-zinc-900/30 p-8 flex flex-col gap-6">
          <h3 className="text-sm font-bold uppercase tracking-[0.25em] text-zinc-400">Feature Focus</h3>
          <ul className="space-y-4 text-zinc-300">
            <li>1) Biomarker timeline for oxLDL, ApoB, hs-CRP with baseline, current, target.</li>
            <li>2) EVOO buying assistant: OlivLimits, Alya Oil, Getsolio recommendations.</li>
            <li>3) Labwork selector for Germany/EU test packages and budget matching.</li>
          </ul>
          <p className="text-xs text-zinc-500 uppercase tracking-widest">
            Includes subscription prompts, 30% offer hooks, and yearly protocol tracking.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 border-t border-zinc-800 pt-12">
        {biomarkers.map((marker) => (
          <article key={marker.name} className="border border-zinc-800 p-6 flex flex-col gap-4">
            <p className="text-[10px] uppercase tracking-[0.25em] text-zinc-500">{marker.label}</p>
            <p className="text-3xl font-bold tracking-tight">{marker.name}</p>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <p className="text-zinc-500">Baseline</p>
              <p>{marker.baseline}</p>
              <p className="text-zinc-500">Current</p>
              <p>{marker.current}</p>
              <p className="text-zinc-500">Target</p>
              <p>{marker.target}</p>
            </div>
            <span className="text-[10px] uppercase tracking-widest text-emerald-400">{marker.status}</span>
          </article>
        ))}
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-zinc-800 pt-12">
        <div className="flex flex-col gap-5">
          <h3 className="text-3xl font-bold tracking-tighter">Brand + Lab Planner</h3>
          <p className="text-zinc-400">
            Help users answer: What are your goals? What is your budget? Which EVOO should you buy? Which tests
            should you run in Germany/EU?
          </p>
          <div className="space-y-4">
            {brandOptions.map((brand) => (
              <div key={brand.name} className="border border-zinc-800 p-4">
                <p className="text-lg font-bold">{brand.name}</p>
                <p className="text-zinc-400 text-sm">{brand.useCase}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-5">
          <h3 className="text-3xl font-bold tracking-tighter">Test Protocol (Augsburg + EU)</h3>
          <div className="space-y-4">
            {testPlan.map((plan) => (
              <div key={plan.step} className="border border-zinc-800 p-4 grid grid-cols-3 gap-4 items-center">
                <p className="text-sm font-bold uppercase tracking-widest text-zinc-500">{plan.step}</p>
                <p className="col-span-2 text-sm text-zinc-300">{plan.detail}</p>
                <p className="text-xs uppercase tracking-widest text-zinc-500">Cost</p>
                <p className="col-span-2 font-bold">{plan.cost}</p>
              </div>
            ))}
          </div>
          <a
            className="mt-2 inline-block border border-white px-6 py-3 text-[10px] uppercase tracking-[0.2em] font-bold hover:bg-white hover:text-black transition-colors"
            href="https://www.aware.app/de/shop/munich-maxvorstadt/HH"
            target="_blank"
            rel="noopener noreferrer"
          >
            Open aware.app Lab Option
          </a>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8 border-t border-zinc-800 pt-12">
        <article className="border border-zinc-800 p-6 lg:col-span-2">
          <h3 className="text-2xl font-bold tracking-tight mb-4">Participant Build-Up</h3>
          <p className="text-zinc-400 text-sm mb-6">Current draft cohort. Scale this to 20+ users minimum.</p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {participants.map((person) => (
              <div key={person} className="border border-zinc-800 px-3 py-2 text-sm text-zinc-300">
                {person}
              </div>
            ))}
            <div className="border border-dashed border-zinc-700 px-3 py-2 text-sm text-zinc-500">
              + Add remaining participants
            </div>
          </div>
        </article>

        <article className="border border-zinc-800 p-6 flex flex-col gap-4">
          <h3 className="text-sm font-bold uppercase tracking-[0.2em] text-zinc-500">Revenue + Retention</h3>
          <p className="text-zinc-300 text-sm">Subscription with 30% off first cycle to increase conversion.</p>
          <p className="text-zinc-300 text-sm">
            Add monthly coaching and 1-year progress views to keep customers engaged and reduce churn.
          </p>
          <div className="pt-3 border-t border-zinc-800">
            <p className="text-[10px] uppercase tracking-widest text-zinc-500">Scenario</p>
            <p className="text-xl font-bold">30K users * 10 EUR/month</p>
          </div>
        </article>
      </section>
    </main>
  );
}
