import type { Metadata } from "next";
import { EB_Garamond, Dancing_Script } from "next/font/google";
import "./globals.css";

const ebGaramond = EB_Garamond({
  subsets: ["latin"],
  variable: '--font-eb-garamond',
});

const dancingScript = Dancing_Script({
  subsets: ["latin"],
  variable: '--font-dancing-script',
});

export const metadata: Metadata = {
  title: "Aria - Living Creative Atelier",
  description: "A space that feels like a myth unfolding.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${ebGaramond.variable} ${dancingScript.variable}`}>
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
