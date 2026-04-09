import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-6">BrailleSpeak</h1>
      <p className="text-lg mb-8">Braille to Speech converter</p>
      <Link href="/converter" className="px-6 py-3 bg-purple-600 text-white rounded-lg">
        Go to Converter
      </Link>
    </main>
  );
}