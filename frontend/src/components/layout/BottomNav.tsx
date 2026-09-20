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
