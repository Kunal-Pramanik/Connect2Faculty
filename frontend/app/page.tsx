"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]); 
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setHasSearched(true);

    try {
      const response = await fetch("https://faculty-connect.onrender.com/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
      });
      const data = await response.json();
      if (data && Array.isArray(data.results)) {
        setResults(data.results);
      }
    } catch (error) {
      console.error("Search Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-slate-200 font-sans selection:bg-blue-500/30">
      
      {/* 1. CYBER NAVIGATION */}
      <nav className="border-b border-white/5 bg-black/20 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <span className="text-white font-black text-xl">D</span>
            </div>
            <span className="text-xl font-bold tracking-tighter text-white">Connect2Faculty</span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium uppercase tracking-widest text-slate-400">
            <a href="#results" className="hover:text-cyan-400 transition-colors">Results</a>
            <div className="flex items-center gap-4 text-xs font-bold text-slate-500 border-l border-white/10 pl-6">
              <span>TEAM: KUNAL & JINAL</span>
            </div>
          </div>
        </div>
      </nav>

      {/* 2. NEURAL HERO SECTION */}
      <header className="relative pt-20 pb-20 px-6 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent -z-10" />
        
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block px-4 py-1.5 mb-6 rounded-full border border-blue-500/20 bg-blue-500/5 text-blue-400 text-[10px] font-bold uppercase tracking-widest">
            Semantic Intelligence Active
          </div>
          <h1 className="text-5xl md:text-7xl font-black text-white mb-8 tracking-tight leading-[1.1]">
            Connect With <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300"> Best Faculty </span>
          </h1>
          
          {/* THE COMMAND CENTER SEARCH BAR - NOW CONNECTED */}
          <div className="relative group max-w-3xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
            <div className="relative flex flex-col md:flex-row gap-2 bg-[#0f172a] p-2 rounded-2xl border border-white/10 shadow-2xl">
              <input 
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                placeholder="Describe your research vision..."
                className="flex-1 bg-transparent px-6 py-4 outline-none text-white text-lg placeholder:text-slate-500"
              />
              <button 
                onClick={handleSearch}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-500 text-white px-10 py-4 rounded-xl font-bold transition-all flex items-center justify-center gap-2 group disabled:opacity-50"
              >
                {loading ? "PROCESSING..." : "RIDE THE DATA"} 
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 3. SEARCH RESULTS - NEW SECTION */}
      <main id="results" className="max-w-7xl mx-auto px-6 pb-24">
        {loading && (
          <div className="flex flex-col items-center py-20 animate-pulse">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-blue-400 font-mono text-sm tracking-widest uppercase">Analyzing Semantic Layers...</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((faculty, i) => (
            <div key={i} className="group bg-[#0f172a]/50 border border-white/5 rounded-2xl overflow-hidden hover:border-blue-500/40 transition-all duration-500 flex flex-col">
              <div className="p-6 flex gap-4 bg-white/5">
                <img 
                  src={faculty.image_url.startsWith("http") ? faculty.image_url : `https://www.daiict.ac.in${faculty.image_url}`} 
                  className="w-16 h-16 rounded-xl object-cover transition-all duration-500 border border-white/10"
                  alt={faculty.name}
                />
                <div className="flex-1">
                  <h3 className="font-bold text-white text-lg leading-tight">{faculty.name}</h3>
                  <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[10px] font-black uppercase tracking-tighter">
                    <div className="w-1 h-1 rounded-full bg-blue-400 animate-pulse" />
                    {(faculty.score * 100).toFixed(0)}% MATCH
                  </div>
                </div>
              </div>
              <div className="p-6 flex-1 space-y-4">
                <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">Core Specialization</p>
                <p className="text-sm text-slate-300 leading-relaxed line-clamp-3">{faculty.specialization}</p>
              </div>
              <a 
                href={faculty.profile_url} target="_blank"
                className="p-4 text-center text-xs font-bold text-slate-400 hover:text-white border-t border-white/5 hover:bg-blue-600 transition-all"
              >
                ACCESS PROFILE →
              </a>
            </div>
          ))}
        </div>

        {!loading && hasSearched && results.length === 0 && (
          <div className="text-center py-20 text-slate-500 font-mono uppercase tracking-widest text-sm">
            Zero Matches Found in Research DNA.
          </div>
        )}
      </main>

      {/* 4. TEAM FOOTER */}
      <footer className="border-t border-white/5 py-12 px-6 bg-black/40">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-center md:text-left">
            <h4 className="text-white font-bold text-lg mb-2">Developed by Data Riders</h4>
            <div className="flex gap-4 text-slate-400 text-sm">
              <span className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-blue-500"/> Kunal Pramanik</span>
              <span className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-cyan-500"/> Jinal Sasiya</span>
            </div>
          </div>
          <div className="text-slate-500 text-[10px] font-mono uppercase tracking-[0.3em]">
            © 2026 Semantic Intelligence Hub
          </div>
        </div>
      </footer>
    </div>
  );
}
