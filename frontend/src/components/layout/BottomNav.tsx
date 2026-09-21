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
      { name: 'ড্যাশবোর্ড', href: '/dashboard', icon: Home },
      { name: 'ছাত্র-ছাত্রী', href: '/students', icon: Users },
      { name: 'উপস্থিতি', href: '/attendance', icon: CalendarCheck },
      { name: 'ফি/বেতন', href: '/fees', icon: DollarSign },
      { name: 'রিপোর্ট', href: '/reports', icon: MoreHorizontal },
    ];
  } else if (role === 'guardian') {
    tabs = [
      { name: 'ড্যাশবোর্ড', href: '/guardian', icon: Home },
      { name: 'উপস্থিতি', href: '/guardian/attendance', icon: CalendarCheck },
      { name: 'বেতন', href: '/guardian/fees', icon: DollarSign },
      { name: 'রেজাল্ট', href: '/guardian/results', icon: FileText },
      { name: 'নোটিশ', href: '/notices', icon: Bell },
    ];
  } else {
    tabs = [
      { name: 'ড্যাশবোর্ড', href: '/student', icon: Home },
      { name: 'রেজাল্ট', href: '/student/results', icon: FileText },
      { name: 'র‍্যাংকিং', href: '/student/ranking', icon: Users },
      { name: 'উপস্থিতি', href: '/student/attendance', icon: CalendarCheck },
      { name: 'নোটিশ', href: '/notices', icon: Bell },
    ];
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 md:top-0 md:bottom-0 md:right-auto md:w-64 bg-white md:bg-[#004d38] border-t md:border-t-0 md:border-r border-gray-200 md:border-none flex md:flex-col justify-around md:justify-start p-2 pb-safe md:p-4 z-50 md:shadow-2xl transition-all">
      <div className="hidden md:flex items-center gap-3 p-4 mb-8 border-b border-white/10">
          <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center backdrop-blur-sm border border-white/20 shadow-inner">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-7 h-7 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <div>
            <h1 className="font-bold text-xl text-white tracking-wide">AMMS</h1>
            <p className="text-white/60 text-xs">মাদ্রাসা ম্যানেজমেন্ট</p>
          </div>
      </div>
      
      <div className="md:flex-1 md:overflow-y-auto w-full flex justify-around md:block">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = pathname.startsWith(tab.href) && (tab.href !== '/dashboard' || pathname === '/dashboard');
          return (
            <Link key={tab.href} href={tab.href} className={`flex flex-col md:flex-row md:items-center p-2 md:px-4 md:py-3.5 md:mb-2 rounded-lg md:rounded-xl transition-all duration-200 group ${isActive ? 'text-primary md:text-white md:bg-white/15 md:shadow-inner' : 'text-gray-500 hover:text-primary md:text-white/70 md:hover:text-white md:hover:bg-white/5'}`}>
              <Icon size={24} className={`md:mr-4 transition-transform group-hover:scale-110 ${isActive ? 'md:text-white' : 'md:text-white/70 group-hover:text-white'}`} />
              <span className="text-[10px] md:text-sm font-semibold mt-1 md:mt-0 tracking-wide">{tab.name}</span>
            </Link>
          );
        })}
      </div>
      
      <div className="hidden md:block mt-auto pt-4 border-t border-white/10">
         <div className="flex items-center gap-3 px-4 py-3 bg-white/5 rounded-xl cursor-pointer hover:bg-white/10 transition-colors">
            <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-white font-bold">
               {user.name_bn?.charAt(0) || 'U'}
            </div>
            <div className="overflow-hidden">
                <p className="text-white font-medium text-sm truncate">{user.name_bn || 'Admin'}</p>
                <p className="text-white/60 text-xs truncate capitalize">{user.role.replace('_', ' ')}</p>
            </div>
         </div>
      </div>
    </div>
  );
}
