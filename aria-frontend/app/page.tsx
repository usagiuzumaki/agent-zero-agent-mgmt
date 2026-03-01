"use client";

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Book, Image as ImageIcon, LayoutGrid, Sparkles } from 'lucide-react';

export default function Home() {
  const cards = [
    { title: "The Living Book", desc: "Every conversation a chapter, every moment a page.", icon: Book, href: "/book/latest", color: "bg-stone-800" },
    { title: "Photo Journal", desc: "Your creative identity evolution archive.", icon: ImageIcon, href: "/journal", color: "bg-stone-700" },
    { title: "Living Moodboard", desc: "A spatial canvas for your visual subconscious.", icon: LayoutGrid, href: "/moodboard", color: "bg-stone-600" }
  ];

  return (
    <main className="min-h-screen bg-[#f8f5f0] text-stone-900 font-serif">
      <div className="max-w-4xl mx-auto py-32 px-8">
        <header className="mb-24 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-center space-x-3 mb-6"
          >
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-[0.4em] text-stone-400 font-mono">Creative Atelier</span>
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-7xl font-serif tracking-tight mb-8"
          >
            Aria
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-stone-500 italic text-xl"
          >
            A space that feels like a myth unfolding.
          </motion.p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {cards.map((card, index) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 + index * 0.1 }}
            >
              <Link href={card.href} className="group block h-full">
                <div className="h-full p-8 border border-stone-200 rounded-3xl hover:border-indigo-400/50 hover:bg-white transition-all duration-500 hover:shadow-2xl hover:shadow-indigo-500/5">
                  <card.icon className="w-6 h-6 mb-8 text-stone-400 group-hover:text-indigo-500 transition-colors" />
                  <h2 className="text-xl mb-4 group-hover:translate-x-1 transition-transform">{card.title}</h2>
                  <p className="text-stone-500 text-sm italic group-hover:translate-x-1 transition-transform delay-75">{card.desc}</p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        <footer className="mt-32 text-center opacity-30">
            <p className="text-[10px] uppercase tracking-widest font-mono">Agent Zero Architecture &copy; 2026</p>
        </footer>
      </div>
    </main>
  );
}
