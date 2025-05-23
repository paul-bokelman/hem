"use client";
import { Geist, Geist_Mono, Inria_Serif } from "next/font/google";
import { QueryClientProvider } from "react-query";
import NextTopLoader from "nextjs-toploader";
import { Toaster } from "@/components/ui/sonner";
import { UserProvider } from "@/partials/user-context";
import "./globals.css";
import { qc } from "@/lib/qc";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});
const inriaSerif = Inria_Serif({
  variable: "--font-inria-serif",
  subsets: ["latin"],
  weight: ["700"],
});

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark" style={{ colorScheme: "dark" }}>
      <head>
        <title>Hem</title>
        <meta name="description" content="Effortless Control, Infinite Possibility — Your Home, Your Way." />
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable} ${inriaSerif.variable} antialiased`}>
        <NextTopLoader color="#fff" />
        <QueryClientProvider client={qc}>
          <UserProvider>
            <div className="lg:w-120 lg:px-0 px-8 mx-auto h-screen flex flex-col items-center bg-background">
              {children}
            </div>
          </UserProvider>
          <Toaster />
        </QueryClientProvider>
      </body>
    </html>
  );
}
