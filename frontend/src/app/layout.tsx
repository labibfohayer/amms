/* eslint-disable */
import type { Metadata } from "next";
import { Hind_Siliguri } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "@/contexts/AuthContext";
import QueryProvider from "@/providers/QueryProvider";

const hindSiliguri = Hind_Siliguri({ 
    weight: ['300', '400', '500', '600', '700'],
    subsets: ["bengali", "latin"] 
});

export const metadata: Metadata = {
  title: "AMMS | আল মদিনা মাদ্রাসা",
  description: "আল মদিনা মডেল মাদ্রাসা ম্যানেজমেন্ট সিস্টেম",
  manifest: "/manifest.json",
};

export const viewport = {
  themeColor: "#2E7D32",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="bn">
      <body className={hindSiliguri.className}>
        <QueryProvider>
          <AuthProvider>
              {children}
              <Toaster position="top-center" />
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
