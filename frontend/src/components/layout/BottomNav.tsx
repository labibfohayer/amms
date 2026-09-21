/* eslint-disable */
'use client';
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

  if (['principal', 'vice_principal', 'managing_director', 'teacher'].includes(role)) {
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
    <div className="fixed bottom-0 left-0 right-0 md:top-0 md:bottom-0 md:right-auto md:w-64 bg-white border-t md:border-t-0 md:border-r border-gray-200 flex md:flex-col justify-around md:justify-start p-2 pb-safe md:p-4 z-50">
      <div className="hidden md:flex items-center gap-3 p-4 mb-6 border-b border-gray-100">
          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-6 h-6 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <h1 className="font-bold text-xl text-primary-dark">AMMS</h1>
      </div>
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = pathname.startsWith(tab.href) && (tab.href !== '/dashboard' || pathname === '/dashboard');
        return (
          <Link key={tab.href} href={tab.href} className={`flex flex-col md:flex-row md:items-center p-2 md:p-3 md:mb-2 rounded-lg md:rounded-xl transition-colors ${isActive ? 'text-primary bg-primary/5' : 'text-gray-500 hover:text-primary hover:bg-gray-50'}`}>
            <Icon size={24} className="md:mr-3" />
            <span className="text-[10px] md:text-sm font-medium mt-1 md:mt-0">{tab.name}</span>
          </Link>
        );
      })}
    </div>
  );
}
