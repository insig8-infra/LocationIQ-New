import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LocationIQ",
  description: "Purpose-aware location intelligence reports for exact pins in India.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

