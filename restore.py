layout = '''import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BrailleSpeak",
  description: "Braille to Speech converter",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
'''

home = '''import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-950">
      <h1 className="text-5xl font-bold mb-6 text-white">BrailleSpeak</h1>
      <p className="text-lg mb-8 text-gray-400">Braille to Speech converter</p>
      <Link href="/converter" className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
        Go to Converter
      </Link>
    </main>
  );
}
'''

with open('app/layout.tsx', 'w', encoding='utf-8') as f:
    f.write(layout)

with open('app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(home)

print('Done')