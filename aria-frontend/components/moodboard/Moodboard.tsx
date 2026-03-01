"use client";

import React, { useState, useEffect } from 'react';
import { Stage, Layer, Rect, Circle, Text, Image as KonvaImage } from 'react-konva';
import { motion } from 'framer-motion';
import { Plus, Save, Sparkles } from 'lucide-react';

interface MoodboardItem {
  id: string;
  type: 'sticker' | 'text' | 'image' | 'swatch';
  x: number;
  y: number;
  content: string;
  rotation: number;
  scale: number;
}

const Moodboard: React.FC = () => {
  const [items, setItems] = useState<MoodboardItem[]>([]);
  const [suggestion, setSuggestion] = useState<string | null>(null);

  const addItem = (type: MoodboardItem['type']) => {
    const newItem: MoodboardItem = {
      id: Math.random().toString(36).substr(2, 9),
      type,
      x: window.innerWidth / 2,
      y: window.innerHeight / 2,
      content: type === 'text' ? 'New Thought' : type === 'swatch' ? '#d4d4d8' : '✨',
      rotation: 0,
      scale: 1,
    };
    setItems([...items, newItem]);
  };

  const handleDragEnd = (id: string, e: any) => {
    setItems(items.map(item =>
      item.id === id ? { ...item, x: e.target.x(), y: e.target.y() } : item
    ));
  };

  return (
    <div className="relative w-full h-screen bg-[#1a1a1a] overflow-hidden">
      {/* Background Texture */}
      <div className="absolute inset-0 opacity-10 pointer-events-none"
           style={{ backgroundImage: 'radial-gradient(#ffffff 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>

      {/* Controls */}
      <div className="absolute top-8 left-8 z-10 flex flex-col space-y-4">
        <button onClick={() => addItem('text')} className="p-3 bg-white/10 hover:bg-white/20 rounded-full transition-colors text-white">
          <Text className="w-5 h-5" />
        </button>
        <button onClick={() => addItem('sticker')} className="p-3 bg-white/10 hover:bg-white/20 rounded-full transition-colors text-white">
          <Plus className="w-5 h-5" />
        </button>
      </div>

      <div className="absolute top-8 right-8 z-10 flex space-x-4">
        <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-500/20 text-indigo-200 border border-indigo-500/30 rounded-full hover:bg-indigo-500/30 transition-all">
          <Sparkles className="w-4 h-4" />
          <span className="text-sm font-serif">Ask Aria</span>
        </button>
        <button className="p-2 bg-white/5 text-stone-400 rounded-lg hover:text-stone-200 transition-colors">
          <Save className="w-5 h-5" />
        </button>
      </div>

      {/* Aria Suggestion Overlay */}
      {suggestion && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute bottom-12 left-1/2 -translate-x-1/2 z-20 bg-stone-900/80 backdrop-blur-md border border-white/10 p-6 rounded-2xl max-w-md"
        >
          <div className="text-[10px] uppercase tracking-widest text-indigo-400 mb-2 font-mono">Motif Detected</div>
          <p className="text-stone-200 font-serif italic text-sm leading-relaxed">
            "{suggestion}"
          </p>
          <div className="mt-4 flex space-x-4">
            <button onClick={() => setSuggestion(null)} className="text-[10px] uppercase tracking-widest text-stone-500 hover:text-stone-300 transition-colors">Dismiss</button>
            <button className="text-[10px] uppercase tracking-widest text-indigo-400 hover:text-indigo-300 transition-colors">Explore Arc</button>
          </div>
        </motion.div>
      )}

      {/* Canvas Layer */}
      <Stage width={typeof window !== 'undefined' ? window.innerWidth : 1000} height={typeof window !== 'undefined' ? window.innerHeight : 1000}>
        <Layer>
          {items.map((item) => (
            <React.Fragment key={item.id}>
              {item.type === 'text' && (
                <Text
                  text={item.content}
                  x={item.x}
                  y={item.y}
                  draggable
                  fontSize={20}
                  fontFamily="serif"
                  fill="#ffffff"
                  onDragEnd={(e) => handleDragEnd(item.id, e)}
                />
              )}
              {item.type === 'sticker' && (
                <Text
                  text={item.content}
                  x={item.x}
                  y={item.y}
                  draggable
                  fontSize={40}
                  onDragEnd={(e) => handleDragEnd(item.id, e)}
                />
              )}
              {item.type === 'swatch' && (
                <Rect
                  x={item.x}
                  y={item.y}
                  width={60}
                  height={60}
                  fill={item.content}
                  draggable
                  cornerRadius={8}
                  onDragEnd={(e) => handleDragEnd(item.id, e)}
                />
              )}
            </React.Fragment>
          ))}
        </Layer>
      </Stage>
    </div>
  );
};

export default Moodboard;
