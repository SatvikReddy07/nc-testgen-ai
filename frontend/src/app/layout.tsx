import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Test Case Generator MVP",
  description: "Generate structured test cases from user stories.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "sans-serif", margin: 0, padding: 0 }}>
        {children}
      </body>
    </html>
  );
}
