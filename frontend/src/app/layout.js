import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ReduxProvider } from "@/lib/redux/provider";
import NavBar from "@/components/NavBar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Smart Travel",
  description: "Find your perfect travel destination",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ReduxProvider>
          <div className="min-h-screen bg-gray-50">
              <NavBar />
              <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                {children}
            </main>
            <footer className="bg-white">
              <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <p className="text-center text-gray-500 text-sm">
                  &copy; {new Date().getFullYear()} Smart Travel. All rights reserved.
                </p>
              </div>
            </footer>
          </div>
        </ReduxProvider>
      </body>
    </html>
  );
}
