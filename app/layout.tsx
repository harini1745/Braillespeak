import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "BrailleSpeak",
  description: "Braille to Speech - feel words, hear worlds",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
