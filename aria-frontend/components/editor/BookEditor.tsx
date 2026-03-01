"use client";

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { motion, AnimatePresence } from 'framer-motion';
import React, { useState } from 'react';
import { Book, Feather, Sparkles } from 'lucide-react';

interface BookEditorProps {
  projectId: string;
}

const BookEditor: React.FC<BookEditorProps> = ({ projectId }) => {
  const [activeChapter, setActiveChapter] = useState(0);

  const editor = useEditor({
    extensions: [StarterKit],
    content: '<p>The ink is still wet, the story yet to breathe...</p>',
    editorProps: {
      attributes: {
        class: 'prose prose-stone lg:prose-xl focus:outline-none max-w-none font-serif',
      },
    },
  });

  return (
    <div className="flex min-h-screen">
      {/* Chapter Sidebar */}
      <aside className="w-64 border-r border-stone-200/50 p-8 hidden md:block bg-stone-50/30 backdrop-blur-sm">
        <h2 className="text-stone-400 font-serif uppercase tracking-[0.2em] text-[10px] mb-12">The Archive</h2>
        <nav className="space-y-6">
          <button className="flex items-center space-x-3 text-stone-900 font-serif group">
            <Book className="w-4 h-4 text-stone-300 group-hover:text-indigo-400 transition-colors" />
            <span className="text-sm">Introduction</span>
          </button>
          <button className="flex items-center space-x-3 text-stone-400 font-serif hover:text-stone-600 transition-colors group">
            <Feather className="w-4 h-4 text-stone-200 group-hover:text-stone-400 transition-colors" />
            <span className="text-sm italic">Chapter I: Seeds</span>
          </button>
        </nav>
      </aside>

      {/* Main Book Page */}
      <main className="flex-1 overflow-y-auto bg-white/40 shadow-inner">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeChapter}
            initial={{ opacity: 0, rotateY: 15, scale: 0.98 }}
            animate={{ opacity: 1, rotateY: 0, scale: 1 }}
            exit={{ opacity: 0, rotateY: -15, scale: 0.98 }}
            transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
            className="max-w-3xl mx-auto py-32 px-12 relative"
          >
            {/* Aria Margin Notes (Annotations) */}
            <div className="absolute -left-48 top-40 w-40 hidden xl:block">
                <motion.div
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 0.8, x: 0 }}
                  transition={{ delay: 1 }}
                  className="group relative"
                >
                  <div className="flex items-center space-x-2 text-[10px] uppercase tracking-widest text-indigo-300 mb-3 font-mono">
                    <Sparkles className="w-3 h-3" />
                    <span>Aria</span>
                  </div>
                  <p className="aria-margin-note text-sm border-l-2 border-indigo-50/50 pl-6 py-2 group-hover:text-stone-800 group-hover:border-indigo-200 transition-all duration-700">
                    "There is a quiet resonance in this passage—a mirror to the seeds we planted in the garden of your visual subconscious."
                  </p>
                </motion.div>
            </div>

            <header className="mb-20 text-center">
               <span className="text-[10px] uppercase tracking-[0.4em] text-stone-400 font-mono mb-4 block">Chapter One</span>
               <h1 className="text-5xl font-serif text-stone-800 mb-6 tracking-tight">Introduction</h1>
               <div className="w-16 h-px bg-stone-200 mx-auto"></div>
            </header>

            <EditorContent editor={editor} className="min-h-[60vh] text-stone-700/90 selection:bg-indigo-50" />

            {/* Emotional Architecture: Soft Margin Prompt */}
            <footer className="mt-32 pt-16 border-t border-stone-100/50 flex flex-col items-center">
                <motion.button
                    initial={{ opacity: 0.1 }}
                    whileHover={{ opacity: 0.6 }}
                    className="text-stone-400 text-sm italic font-serif cursor-pointer transition-all duration-1000 tracking-wide"
                >
                    "How does this change your story?"
                </motion.button>
                <div className="mt-8 text-[8px] uppercase tracking-[0.6em] text-stone-300 font-mono">End of Leaf</div>
            </footer>
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
};

export default BookEditor;
