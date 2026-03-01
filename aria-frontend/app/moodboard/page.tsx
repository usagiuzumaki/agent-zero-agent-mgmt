"use client";

import dynamic from 'next/dynamic';

// Konva needs to be dynamically imported as it requires 'window'
const Moodboard = dynamic(() => import('@/components/moodboard/Moodboard'), {
  ssr: false,
  loading: () => <div className="w-full h-screen bg-[#1a1a1a] flex items-center justify-center text-stone-500 font-serif italic">Opening the canvas...</div>
});

export default function MoodboardPage() {
  return <Moodboard />;
}
