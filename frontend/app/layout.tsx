import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Sports Analytics Assistant',
  description: 'AI-powered sports analytics and fantasy metrics',
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
