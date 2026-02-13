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
    <div className="min-h-screen bg-[#030712] text-slate-200 font-sans selection:bg-blue-500/30 scroll-smooth flex flex-col">
      
      {/* 1. CYBER NAVIGATION */}
      <nav className="border-b border-white/5 bg-black/20 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            {/* LOGO ICON BOX */}
            <div className="relative group cursor-pointer" onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})}>
              <div className="absolute -inset-2 bg-gradient-to-br from-indigo-600 via-blue-500 to-cyan-400 rounded-2xl blur-md opacity-40 group-hover:opacity-60 transition duration-500"></div>
              <div className="relative w-10 h-10 bg-[#080c17] rounded-xl flex items-center justify-center border border-white/20">
                <span className="text-xl font-black text-transparent bg-clip-text bg-gradient-to-tr from-indigo-400 via-blue-400 to-cyan-300 filter drop-shadow-[0_0_8px_rgba(34,211,238,0.8)]">
                  C
                </span>
              </div>
            </div>

            <div className="flex flex-col">
              <h1 className="text-xl font-bold tracking-tight drop-shadow-[0_0_12px_rgba(34,211,238,0.5)] leading-none">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-500">
                  Connect2Faculty
                </span>
              </h1>
              <span className="text-[8px] text-blue-300/50 font-mono tracking-[0.2em] uppercase mt-1">
                AI Research Collaboration
              </span>
            </div>
          </div>

          {/* NAVBAR LINKS - REPLACED LAUNCH WITH GITHUB */}
          <div className="hidden md:flex gap-8 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 items-center">
            <a href="#hero" className="hover:text-cyan-400 transition-all">Engine</a>
            <a href="#results" className="hover:text-cyan-400 transition-all">Directory</a>
            
            {/* PROJECT DETAILS BUTTON */}
            <a 
              href="https://github.com/Kunal-Pramanik/Faculty-Finder" 
              target="_blank" 
              rel="noopener noreferrer"
              className="bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-white hover:bg-blue-600 hover:border-blue-500 transition-all duration-300 flex items-center gap-2"
            >
              <span>Project Details</span>
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
            </a>
          </div>
        </div>
      </nav>

      {/* 2. NEURAL HERO SECTION */}
      <header id="hero" className="relative pt-8 pb-8 px-6 overflow-hidden flex flex-col justify-center border-b border-white/5">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/10 via-transparent to-transparent -z-10" />
        
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block px-3 py-1 mb-4 rounded-full border border-blue-500/20 bg-blue-500/5 text-blue-400 text-[9px] font-bold uppercase tracking-widest">
            Semantic Intelligence Active
          </div>
          <h1 className="text-3xl md:text-5xl font-black text-white mb-6 tracking-tight leading-tight">
            Find Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300"> Research DNA. </span>
          </h1>
          
          <div className="relative group max-w-2xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
            <div className="relative flex flex-col md:flex-row gap-2 bg-[#0f172a] p-1.5 rounded-2xl border border-white/10 shadow-2xl">
              <input 
                id="search-input"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                placeholder="Describe research vision..."
                className="flex-1 bg-transparent px-4 py-3 outline-none text-white text-base placeholder:text-slate-500"
              />
              <button onClick={handleSearch} disabled={loading} className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-bold transition-all text-sm disabled:opacity-50">
                {loading ? "..." : "RIDE THE DATA"}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 3. RESULTS SECTION */}
      <main id="results" className="flex-1 max-w-7xl mx-auto px-6 py-8 w-full">
        {loading && (
          <div className="flex flex-col items-center py-10 animate-pulse">
            <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-blue-400 font-mono text-[10px] tracking-widest uppercase">Analyzing Semantic Layers...</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((faculty, i) => (
            <div key={i} className="group bg-[#0f172a]/50 border border-white/5 rounded-2xl overflow-hidden hover:border-blue-500/40 transition-all duration-500 flex flex-col">
              <div className="p-4 flex gap-4 bg-white/5">
                <img 
                  src={faculty.image_url.startsWith("http") ? faculty.image_url : `https://www.daiict.ac.in${faculty.image_url}`} 
                  className="w-12 h-12 rounded-lg object-cover border border-white/10"
                  alt={faculty.name}
                />
                <div className="flex-1">
                  <h3 className="font-bold text-white text-base leading-tight">{faculty.name}</h3>
                  <div className="mt-1 inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[9px] font-black uppercase">
                    {(faculty.score * 100).toFixed(0)}% MATCH
                  </div>
                </div>
              </div>
              <div className="p-4 flex-1">
                <p className="text-[10px] text-slate-500 font-bold uppercase mb-2">Core Specialization</p>
                <p className="text-xs text-slate-300 line-clamp-2">{faculty.specialization}</p>
              </div>
              <a href={faculty.profile_url} target="_blank" rel="noopener noreferrer" className="p-3 text-center text-[10px] font-bold text-slate-400 hover:text-white border-t border-white/5 hover:bg-blue-600 transition-all">
                ACCESS PROFILE →
              </a>
            </div>
          ))}
        </div>

        {!loading && !hasSearched && (
          <div className="text-center py-12 opacity-50 border border-dashed border-white/5 rounded-3xl">
            <p className="text-xs font-mono uppercase tracking-[0.2em]">Ready for Semantic Discovery</p>
          </div>
        )}
      </main>

      {/* 4. TEAM FOOTER */}
      <footer className="border-t border-white/5 bg-black/40 py-6 px-6 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex flex-col items-center md:items-start">
            <h4 className="text-white font-bold text-sm mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
              Developed by Data Riders
            </h4>
            <div className="flex gap-6 text-[12px] font-bold tracking-wide">
              <span className="flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.2)]">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"/> 
                Kunal Pramanik
              </span>
              <span className="flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shadow-[0_0_10px_rgba(34,211,238,0.2)]">
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"/> 
                Jinal Sasiya
              </span>
            </div>
          </div>
          <div className="text-slate-500 text-[9px] font-mono uppercase tracking-[0.3em] opacity-50">
            © 2026 Semantic Intelligence Hub
          </div>
        </div>
      </footer>
    </div>
  );
}
