import os

base_dir = r"C:\Users\assdi\.gemini\antigravity\scratch\amms\frontend"

files_to_create = {
    r"tailwind.config.ts": """import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2E7D32',
          dark: '#1B5E20',
          light: '#4CAF50',
        },
        gold: '#F9A825',
        'light-green': '#F1F8E9',
      },
    },
  },
  plugins: [],
} satisfies Config;
""",
    r"next.config.ts": """const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = withPWA(nextConfig);
""",
    r".env.local": """NEXT_PUBLIC_API_URL=http://localhost:8000\n""",
    r"public\manifest.json": """{
  "name": "Al Modina Madrasah",
  "short_name": "AMMS",
  "description": "আল মদিনা মডেল মাদ্রাসা ম্যানেজমেন্ট সিস্টেম",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1B5E20",
  "theme_color": "#2E7D32",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}""",
    r"src\lib\api.ts": """import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: API_BASE });

if (typeof window !== 'undefined') {
    api.interceptors.request.use((config) => {
        const token = localStorage.getItem('access_token');
        if (token && config.headers) config.headers.Authorization = `Bearer ${token}`;
        return config;
    });

    api.interceptors.response.use(
        (res) => res,
        async (error) => {
            if (error.response?.status === 401) {
            try {
                const refresh = localStorage.getItem('refresh_token');
                if (!refresh) throw new Error();
                const res = await axios.post(`${API_BASE}/api/auth/token/refresh/`, { refresh });
                localStorage.setItem('access_token', res.data.access);
                if (error.config.headers) {
                    error.config.headers.Authorization = `Bearer ${res.data.access}`;
                }
                return axios(error.config);
            } catch {
                localStorage.clear();
                window.location.href = '/login';
            }
            }
            return Promise.reject(error);
        }
    );
}

export default api;
""",
    r"src\lib\auth.ts": """export interface User {
  user_id: string;
  name: string;
  name_bn: string;
  role: 'principal' | 'teacher' | 'staff' | 'guardian' | 'student';
  phone: string;
  photo?: string;
}

export const getUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
};

export const isLoggedIn = () => {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
}

export const logout = () => {
    if (typeof window === 'undefined') return;
  localStorage.clear();
  window.location.href = '/login';
};
""",
    r"src\contexts\AuthContext.tsx": """'use client';
import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, getUser, isLoggedIn, logout } from '../lib/auth';
import { useRouter, usePathname } from 'next/navigation';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  logoutUser: () => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  logoutUser: logout,
  setUser: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUserState] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const u = getUser();
    setUserState(u);
    setIsAuthenticated(isLoggedIn());
    setLoading(false);
  }, [pathname]);

  const logoutUser = () => {
    logout();
    setUserState(null);
    setIsAuthenticated(false);
  };

  const setUser = (u: User | null) => {
      setUserState(u);
      setIsAuthenticated(!!u);
  }

  if (loading) return null;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, logoutUser, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""",
    r"src\components\layout\BottomNav.tsx": """'use client';
import { useAuth } from '@/contexts/AuthContext';
import { Home, Users, CalendarCheck, DollarSign, MoreHorizontal, FileText, Bell } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {
  const { user } = useAuth();
  const pathname = usePathname();

  if (!user) return null;

  const role = user.role;
  let tabs = [];

  if (role === 'principal' || role === 'teacher') {
    tabs = [
      { name: 'হোম', href: '/dashboard', icon: Home },
      { name: 'ছাত্র', href: '/students', icon: Users },
      { name: 'উপস্থিতি', href: '/attendance', icon: CalendarCheck },
      { name: 'অর্থ', href: '/fees', icon: DollarSign },
      { name: 'আরো', href: '/reports', icon: MoreHorizontal },
    ];
  } else if (role === 'guardian') {
    tabs = [
      { name: 'হোম', href: '/guardian', icon: Home },
      { name: 'উপস্থিতি', href: '/guardian/attendance', icon: CalendarCheck },
      { name: 'ফি', href: '/guardian/fees', icon: DollarSign },
      { name: 'রেজাল্ট', href: '/guardian/results', icon: FileText },
      { name: 'নোটিশ', href: '/notices', icon: Bell },
    ];
  } else {
    tabs = [
      { name: 'হোম', href: '/student', icon: Home },
      { name: 'রেজাল্ট', href: '/student/results', icon: FileText },
      { name: 'র্যাংকিং', href: '/student/ranking', icon: Users },
      { name: 'উপস্থিতি', href: '/student/attendance', icon: CalendarCheck },
      { name: 'নোটিশ', href: '/notices', icon: Bell },
    ];
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around p-2 pb-safe z-50">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = pathname.startsWith(tab.href);
        return (
          <Link key={tab.href} href={tab.href} className={`flex flex-col items-center p-2 rounded-lg ${isActive ? 'text-primary' : 'text-gray-500 hover:text-primary-light'}`}>
            <Icon size={24} />
            <span className="text-[10px] mt-1">{tab.name}</span>
          </Link>
        );
      })}
    </div>
  );
}
""",
    r"src\components\layout\TopBar.tsx": """import { Bell, UserCircle } from 'lucide-react';
import Link from 'next/link';

export default function TopBar({ title }: { title: string }) {
  return (
    <div className="bg-primary text-white p-4 sticky top-0 z-50 shadow-md">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
      <div className="relative flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-5 h-5 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <h1 className="font-semibold text-lg">{title}</h1>
        </div>
        <div className="flex items-center gap-3">
            <Link href="/notices"><Bell size={20} /></Link>
            <UserCircle size={24} />
        </div>
      </div>
    </div>
  );
}
""",
    r"src\components\layout\AppLayout.tsx": """import TopBar from './TopBar';
import BottomNav from './BottomNav';

export default function AppLayout({ children, title = 'AMMS' }: { children: React.ReactNode; title?: string }) {
  return (
    <div className="min-h-screen bg-light-green pb-20">
      <TopBar title={title} />
      <main className="p-4 max-w-md mx-auto">
        {children}
      </main>
      <BottomNav />
    </div>
  );
}
""",
    r"src\components\ui\StatCard.tsx": """import { ReactNode } from 'react';

export default function StatCard({ title, value, subtitle, color, icon }: { title: string; value: string | number; subtitle?: string; color: string; icon?: ReactNode }) {
  const colorMap: Record<string, string> = {
    blue: 'border-blue-500 text-blue-700',
    green: 'border-green-500 text-green-700',
    red: 'border-red-500 text-red-700',
    orange: 'border-orange-500 text-orange-700',
    purple: 'border-purple-500 text-purple-700',
  };
  return (
    <div className={`bg-white p-4 rounded-xl shadow-sm border-l-4 ${colorMap[color] || 'border-gray-500'}`}>
        <div className="flex justify-between items-start">
            <div>
                <p className="text-gray-500 text-sm">{title}</p>
                <h3 className="text-2xl font-bold mt-1">{value}</h3>
                {subtitle && <p className="text-xs mt-1 opacity-80">{subtitle}</p>}
            </div>
            {icon && <div className="opacity-80">{icon}</div>}
        </div>
    </div>
  );
}
""",
    r"src\components\ui\StudentCard.tsx": """import { UserCircle } from 'lucide-react';

export default function StudentCard({ student }: { student: any }) {
    return (
        <div className="bg-white p-3 rounded-xl shadow-sm flex items-center gap-3">
            {student.photo ? (
                <img src={student.photo} alt={student.name_bn} className="w-12 h-12 rounded-full object-cover" />
            ) : (
                <UserCircle size={48} className="text-gray-400" />
            )}
            <div className="flex-1">
                <h4 className="font-semibold">{student.name_bn}</h4>
                <p className="text-xs text-gray-500">{student.class_name}</p>
            </div>
            <span className={`px-2 py-1 text-[10px] rounded-full ${student.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {student.status === 'active' ? 'সক্রিয়' : 'নিষ্ক্রিয়'}
            </span>
        </div>
    )
}
""",
    r"src\components\ui\LoadingSpinner.tsx": """export default function LoadingSpinner() {
    return <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div></div>;
}""",
    r"src\components\ui\WhatsAppButton.tsx": """export default function WhatsAppButton({ phone, message }: { phone: string; message: string }) {
    return (
        <a href={`https://wa.me/${phone}?text=${encodeURIComponent(message)}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 bg-[#25D366] text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-[#128C7E] transition-colors">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            WhatsApp
        </a>
    )
}""",
    r"src\app\login\page.tsx": """'use client';
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { User, Lock, Eye, EyeOff } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function Login() {
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [showPass, setShowPass] = useState(false);
    const { setUser } = useAuth();
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post('/api/auth/login/', { phone, password });
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            setUser(res.data.user);
            
            const role = res.data.user.role;
            if (['principal', 'teacher', 'staff'].includes(role)) router.push('/dashboard');
            else if (role === 'guardian') router.push('/guardian');
            else router.push('/student');
        } catch (error) {
            toast.error('লগইন ব্যর্থ হয়েছে। নম্বর ও পাসওয়ার্ড চেক করুন।');
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-b from-primary-dark to-primary">
            <div className="h-[45vh] flex flex-col items-center justify-center text-white relative">
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mb-4 text-primary">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-12 h-12">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                        </svg>
                    </div>
                    <h2 className="text-gold italic font-serif text-sm">Al Modina Model Madrasah And Research Institute</h2>
                    <h1 className="text-xl font-bold mt-2 text-center">আল মদিনা মডেল মাদ্রাসা<br/>এন্ড রিসার্চ ইনস্টিটিউট</h1>
                </div>
            </div>
            
            <div className="flex-1 bg-white rounded-t-3xl p-6 pt-8">
                <h2 className="text-2xl font-bold text-primary-dark mb-6 text-center">লগইন করুন</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="relative">
                        <User className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input type="text" placeholder="ফোন নম্বর" value={phone} onChange={e=>setPhone(e.target.value)} className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
                    </div>
                    <div className="relative">
                        <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input type={showPass ? "text" : "password"} placeholder="পাসওয়ার্ড" value={password} onChange={e=>setPassword(e.target.value)} className="w-full pl-10 pr-10 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
                        <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-3 text-gray-400">
                            {showPass ? <EyeOff size={20} /> : <Eye size={20} />}
                        </button>
                    </div>
                    <button type="submit" className="w-full bg-primary text-white py-3 rounded-xl font-bold text-lg hover:bg-primary-dark transition-colors">
                        লগইন
                    </button>
                    <div className="text-center mt-4">
                        <a href="#" className="text-primary text-sm font-medium">পাসওয়ার্ড ভুলে গেছেন?</a>
                    </div>
                </form>
            </div>
        </div>
    );
}
""",
    r"src\app\dashboard\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import StatCard from '@/components/ui/StatCard';
import { useAuth } from '@/contexts/AuthContext';
import { Users, UserCheck, UserX, UserPlus, DollarSign, FileText, Bell, BarChart } from 'lucide-react';
import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
    const { user, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) router.push('/login');
        if (user && !['principal', 'teacher', 'staff'].includes(user.role)) router.push('/');
    }, [user, isAuthenticated, router]);

    if (!user) return null;

    return (
        <AppLayout title="ড্যাশবোর্ড">
            <div className="mb-6">
                <h2 className="text-xl font-bold text-primary">আস-সালামু আলাইকুম, {user.name_bn}!</h2>
                <p className="text-sm text-gray-500">{new Date().toLocaleDateString('bn-BD', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
            </div>

            {user.role === 'principal' && (
                <>
                    <div className="grid grid-cols-3 gap-3 mb-6">
                        <StatCard title="মোট ছাত্র" value="350" color="blue" icon={<Users size={20} />} />
                        <StatCard title="আজ উপস্থিত" value="310" color="green" icon={<UserCheck size={20} />} />
                        <StatCard title="আজ অনুপস্থিত" value="40" color="red" icon={<UserX size={20} />} />
                    </div>
                    
                    <div className="space-y-4 mb-6">
                        <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-500 flex justify-between items-center">
                            <div>
                                <h3 className="text-gray-500 text-sm">মোট বকেয়া ফি</h3>
                                <p className="text-xl font-bold text-red-600">৳১,২৫,০০০</p>
                            </div>
                            <DollarSign className="text-red-300" size={32} />
                        </div>
                        <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500 flex justify-between items-center">
                            <div>
                                <h3 className="text-gray-500 text-sm">স্টাফ</h3>
                                <p className="font-medium">শিক্ষক: ১৫ | কর্মী: ৫</p>
                            </div>
                            <Users className="text-orange-300" size={32} />
                        </div>
                    </div>

                    <h3 className="font-bold text-gray-700 mb-3">দ্রুত কাজ</h3>
                    <div className="grid grid-cols-2 gap-3 mb-6">
                        <QuickAction href="/students/add" icon={<UserPlus />} text="ছাত্র ভর্তি" />
                        <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি" />
                        <QuickAction href="/fees" icon={<DollarSign />} text="ফি সংগ্রহ" />
                        <QuickAction href="/exams" icon={<FileText />} text="রেজাল্ট" />
                        <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                        <QuickAction href="/reports" icon={<BarChart />} text="রিপোর্ট" />
                    </div>
                </>
            )}

            {user.role === 'teacher' && (
                <>
                    <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                        <h3 className="text-gray-500 text-sm">এই মাসের বেতন</h3>
                        <p className="text-xl font-bold text-green-700">৳১৫,০০০ — পরিশোধিত ✓</p>
                    </div>
                    <h3 className="font-bold text-gray-700 mb-3">আজকের কাজ</h3>
                    <div className="grid grid-cols-2 gap-3">
                        <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি নিন" />
                        <QuickAction href="/exams" icon={<FileText />} text="নম্বর দিন" />
                        <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                    </div>
                </>
            )}

             {user.role === 'staff' && (
                <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                    <h3 className="text-gray-500 text-sm">এই মাসের বেতন</h3>
                    <p className="text-xl font-bold text-green-700">৳১০,০০০ — পরিশোধিত ✓</p>
                </div>
            )}
        </AppLayout>
    );
}

function QuickAction({ href, icon, text }: { href: string; icon: React.ReactNode; text: string }) {
    return (
        <Link href={href} className="flex flex-col items-center justify-center p-4 bg-white rounded-xl shadow-sm hover:bg-gray-50 border border-gray-100">
            <div className="text-primary mb-2">{icon}</div>
            <span className="text-sm font-medium text-gray-700">{text}</span>
        </Link>
    );
}
""",
    r"src\app\page.tsx": """'use client';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
    const { user, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login');
        } else if (user) {
            if (['principal', 'teacher', 'staff'].includes(user.role)) router.push('/dashboard');
            else if (user.role === 'guardian') router.push('/guardian');
            else router.push('/student');
        }
    }, [user, isAuthenticated, router]);

    return <div className="min-h-screen flex items-center justify-center text-primary font-bold">লোড হচ্ছে...</div>;
}
""",
    r"src\app\layout.tsx": """import type { Metadata } from "next";
import { Hind_Siliguri } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "@/contexts/AuthContext";

const hindSiliguri = Hind_Siliguri({ 
    weight: ['300', '400', '500', '600', '700'],
    subsets: ["bengali", "latin"] 
});

export const metadata: Metadata = {
  title: "AMMS | আল মদিনা মাদ্রাসা",
  description: "আল মদিনা মডেল মাদ্রাসা ম্যানেজমেন্ট সিস্টেম",
  manifest: "/manifest.json",
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
        <AuthProvider>
            {children}
            <Toaster position="top-center" />
        </AuthProvider>
      </body>
    </html>
  );
}
""",
    r"src\app\students\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import StudentCard from '@/components/ui/StudentCard';
import { Search, Plus } from 'lucide-react';
import Link from 'next/link';

export default function Students() {
    return (
        <AppLayout title="ছাত্র তালিকা">
            <div className="relative mb-4">
                <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                <input type="text" placeholder="ছাত্র খুঁজুন..." className="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
            </div>
            <div className="flex gap-2 overflow-x-auto pb-2 mb-4 scrollbar-hide">
                {['সকল', 'নূরানী', 'নাজেরা', 'হিফজ', 'Play', 'Class 1'].map(f => (
                    <button key={f} className="px-4 py-1.5 bg-white border border-gray-200 rounded-full text-sm whitespace-nowrap hover:border-primary focus:bg-primary-light focus:text-white focus:border-primary">{f}</button>
                ))}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[1, 2, 3].map(i => (
                    <StudentCard key={i} student={{name_bn: 'আব্দুল্লাহ', class_name: 'নূরানী', status: 'active'}} />
                ))}
            </div>
            <Link href="/students/add" className="fixed bottom-20 right-4 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary-dark z-50">
                <Plus size={24} />
            </Link>
        </AppLayout>
    )
}
""",
    r"src\app\students\add\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function AddStudent() {
    return (
        <AppLayout title="ছাত্র ভর্তি">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <h2 className="text-lg font-bold mb-4">ছাত্র ভর্তির ফরম</h2>
                <p className="text-sm text-gray-500 mb-4">ধাপ ১: ব্যক্তিগত তথ্য</p>
                <form className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">নাম (বাংলা)</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">পিতার নাম (বাংলা)</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <button type="button" className="w-full bg-primary text-white py-2 rounded-lg font-medium hover:bg-primary-dark">পরবর্তী ধাপ</button>
                </form>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\students\[id]\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import { UserCircle } from 'lucide-react';

export default function StudentDetail({ params }: { params: { id: string } }) {
    return (
        <AppLayout title="ছাত্রের প্রোফাইল">
            <div className="bg-primary text-white p-6 rounded-xl text-center mb-6 shadow-md relative overflow-hidden">
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mb-3">
                        <UserCircle size={60} className="text-gray-300" />
                    </div>
                    <h2 className="text-2xl font-bold">আব্দুল্লাহ</h2>
                    <p className="opacity-90">আইডি: AMMS-2024-001</p>
                    <span className="mt-2 px-3 py-1 bg-green-500/20 rounded-full text-xs font-medium border border-green-500/30">সক্রিয়</span>
                </div>
            </div>
            
            <div className="flex bg-white rounded-lg p-1 mb-4 shadow-sm">
                <button className="flex-1 py-2 text-sm font-medium bg-primary text-white rounded-md shadow-sm">তথ্য</button>
                <button className="flex-1 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-md">উপস্থিতি</button>
                <button className="flex-1 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-md">ফি</button>
                <button className="flex-1 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-md">রেজাল্ট</button>
            </div>
            
            <div className="bg-white p-4 rounded-xl shadow-sm space-y-3">
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">বিভাগ</span>
                    <span className="font-medium text-sm">নূরানী</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">পিতার নাম</span>
                    <span className="font-medium text-sm">আব্দুর রহমান</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">অভিভাবকের নম্বর</span>
                    <span className="font-medium text-sm">০১৭XXXXXXXX</span>
                </div>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\attendance\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Attendance() {
    return (
        <AppLayout title="উপস্থিতি">
            <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                <select className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-3">
                    <option>ক্লাস নির্বাচন করুন</option>
                    <option>নূরানী</option>
                </select>
                <input type="date" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
            </div>
            <div className="space-y-2">
                {[1,2,3].map(i => (
                    <div key={i} className="bg-white p-3 rounded-lg shadow-sm flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
                            <div>
                                <h4 className="font-medium text-sm">ছাত্র {i}</h4>
                                <p className="text-xs text-gray-500">রোল: {i}</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button className="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center font-bold">✓</button>
                            <button className="w-8 h-8 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center font-bold hover:bg-red-100 hover:text-red-600">✗</button>
                        </div>
                    </div>
                ))}
            </div>
            <button className="w-full mt-6 bg-primary text-white py-3 rounded-xl font-bold">সংরক্ষণ করুন</button>
        </AppLayout>
    )
}
""",
    r"src\app\fees\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Fees() {
    return (
        <AppLayout title="ফি সংগ্রহ">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 mb-4">ছাত্র নির্বাচন করে ফি সংগ্রহ করুন</p>
                <input type="text" placeholder="ছাত্র খুঁজুন..." className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-4" />
                <button className="w-full bg-primary text-white py-3 rounded-xl font-bold">খুঁজুন</button>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\fees\due\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function DueFees() {
    return (
        <AppLayout title="বকেয়া ফি">
            <div className="text-center mb-6">
                <h2 className="text-lg font-medium text-gray-600">মোট বকেয়া</h2>
                <p className="text-3xl font-bold text-red-600">৳১,২৫,০০০</p>
            </div>
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">বকেয়া তালিকা লোড হচ্ছে...</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\teachers\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Teachers() {
    return (
        <AppLayout title="শিক্ষক ও কর্মী">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">তালিকা লোড হচ্ছে...</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\exams\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Exams() {
    return (
        <AppLayout title="পরীক্ষা সমূহ">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">পরীক্ষার তালিকা লোড হচ্ছে...</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\exams\[id]\ranking\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Ranking() {
    return (
        <AppLayout title="র্যাংকিং">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">র্যাংকিং লোড হচ্ছে...</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\notices\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import Link from 'next/link';
import { Plus } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export default function Notices() {
    const { user } = useAuth();
    return (
        <AppLayout title="নোটিশ বোর্ড">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">কোনো নোটিশ নেই</p>
            </div>
            {user && ['principal', 'teacher'].includes(user.role) && (
                <Link href="/notices/add" className="fixed bottom-20 right-4 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary-dark z-50">
                    <Plus size={24} />
                </Link>
            )}
        </AppLayout>
    )
}
""",
    r"src\app\notices\add\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function AddNotice() {
    return (
        <AppLayout title="নোটিশ দিন">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <form className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">শিরোনাম</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">বিস্তারিত</label>
                        <textarea className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary h-32"></textarea>
                    </div>
                    <button type="button" className="w-full bg-primary text-white py-2 rounded-lg font-medium hover:bg-primary-dark">প্রকাশ করুন</button>
                </form>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\guardian\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';

export default function GuardianDashboard() {
    const { user } = useAuth();
    return (
        <AppLayout title="অভিভাবক ড্যাশবোর্ড">
            <h2 className="text-lg font-bold mb-4">আপনার সন্তান: আব্দুল্লাহ</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                <p className="text-gray-500 text-sm">এই মাসের উপস্থিতি</p>
                <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2 mb-1">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '85%' }}></div>
                </div>
                <p className="text-xs text-right text-gray-500">৮৫% উপস্থিত</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\student\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';

export default function StudentDashboard() {
    const { user } = useAuth();
    return (
        <AppLayout title="ছাত্র ড্যাশবোর্ড">
            <h2 className="text-lg font-bold mb-4 text-primary">আস-সালামু আলাইকুম, {user?.name_bn}!</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm mb-4 text-center">
                <p className="text-gray-500 text-sm mb-2">সর্বশেষ ফলাফল</p>
                <h3 className="text-3xl font-bold text-gold">A+</h3>
                <p className="text-sm font-medium text-gray-700 mt-1">জিপিএ: ৪.৮০</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\hostel\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Hostel() {
    return (
        <AppLayout title="হোস্টেল">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">রুম তালিকা লোড হচ্ছে...</p>
            </div>
        </AppLayout>
    )
}
""",
    r"src\app\reports\page.tsx": """'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function Reports() {
    return (
        <AppLayout title="রিপোর্ট">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <p className="text-gray-500 text-center">রিপোর্ট অপশন সমূহ</p>
            </div>
        </AppLayout>
    )
}
"""
}

# Create missing directories and files
for filepath, content in files_to_create.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Files created.")
