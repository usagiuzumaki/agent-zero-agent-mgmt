"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Image as ImageIcon, Sparkles, Calendar } from 'lucide-react';

interface JournalImage {
  id: string;
  url: string;
  title: string;
  reflection: string;
  date: string;
  tone: string;
}

const PhotoJournal: React.FC = () => {
  const [images, setImages] = useState<JournalImage[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = () => {
    setIsUploading(true);
    // Mock upload delay
    setTimeout(() => {
      const newImage: JournalImage = {
        id: Math.random().toString(),
        url: 'https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?q=80&w=400&auto=format&fit=crop',
        title: 'Morning Light',
        reflection: 'The way the dust motes danced in the sun reminded me of old libraries and forgotten dreams.',
        date: new Date().toLocaleDateString(),
        tone: 'Melancholic yet hopeful',
      };
      setImages([newImage, ...images]);
      setIsUploading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-stone-50 py-24 px-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-16 flex justify-between items-end">
          <div>
            <h1 className="text-4xl font-serif text-stone-800 mb-2">Photo Journal</h1>
            <p className="text-stone-500 font-serif italic">Your creative identity evolution archive.</p>
          </div>
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="flex items-center space-x-2 px-6 py-3 bg-stone-900 text-white rounded-full hover:bg-stone-800 transition-all disabled:opacity-50"
          >
            <Upload className="w-4 h-4" />
            <span className="font-serif">{isUploading ? 'Aria is reflecting...' : 'Share a moment'}</span>
          </button>
        </header>

        {images.length === 0 ? (
          <div className="h-96 border-2 border-dashed border-stone-200 rounded-3xl flex flex-col items-center justify-center text-stone-400 space-y-4">
            <ImageIcon className="w-12 h-12 opacity-20" />
            <p className="font-serif italic">"If you'd like to share what today looked like, I'd love to respond."</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
            {images.map((image, index) => (
              <motion.div
                key={image.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="group"
              >
                <div className="relative aspect-[4/5] overflow-hidden rounded-2xl mb-6 shadow-sm group-hover:shadow-xl transition-shadow duration-500">
                  <img src={image.url} alt={image.title} className="w-full h-full object-cover grayscale-[0.2] group-hover:grayscale-0 transition-all duration-700" />
                  <div className="absolute inset-0 bg-gradient-to-t from-stone-900/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <div className="absolute bottom-6 left-6 right-6 text-white opacity-0 group-hover:opacity-100 transition-opacity transform translate-y-2 group-hover:translate-y-0 transition-transform">
                    <p className="text-xs font-mono uppercase tracking-widest mb-1">{image.date}</p>
                    <h3 className="text-lg font-serif">{image.title}</h3>
                  </div>
                </div>

                <div className="space-y-4">
                   <div className="flex items-center space-x-2 text-[10px] uppercase tracking-widest text-stone-400 font-mono">
                      <Sparkles className="w-3 h-3" />
                      <span>Aria's Reflection</span>
                   </div>
                   <p className="text-stone-600 font-serif italic text-sm leading-relaxed leading-relaxed border-l border-stone-200 pl-4 py-1">
                      "{image.reflection}"
                   </p>
                   <div className="text-[10px] text-stone-400 font-serif uppercase tracking-widest">
                      Tone: {image.tone}
                   </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {/* Timeline clustering would go here */}
      </div>
    </div>
  );
};

export default PhotoJournal;
