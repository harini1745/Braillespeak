layout = '''export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
'''

converter = '''export default function ConverterPage() {
  return (
    <main>
      <h1>Converter</h1>
    </main>
  )
}
'''

with open('app/layout.tsx', 'w', encoding='utf-8') as f:
    f.write(layout)

with open('app/converter/page.tsx', 'w', encoding='utf-8') as f:
    f.write(converter)

print('Done')
