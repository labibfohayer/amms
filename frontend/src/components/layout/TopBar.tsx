/* eslint-disable */
import { Bell, UserCircle } from 'lucide-react';
import Link from 'next/link';

export default function TopBar({ title }: { title: string }) {
  return (
    <div className="bg-primary md:bg-white/80 md:backdrop-blur-md text-white md:text-gray-800 p-4 md:px-8 sticky top-0 z-40 shadow-md md:shadow-sm md:border-b border-gray-200 transition-all">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px] md:hidden"></div>
      <div className="relative flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-white/20 md:bg-primary/10 flex items-center justify-center md:hidden">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-5 h-5 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <h1 className="font-semibold text-lg md:text-xl tracking-tight">{title}</h1>
        </div>
        <div className="flex items-center gap-4">
            <Link href="/notices" className="relative p-2 rounded-full hover:bg-black/5 md:hover:bg-gray-100 transition-colors">
                <Bell size={20} className="md:text-gray-600" />
                <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 border-2 border-primary md:border-white rounded-full"></span>
            </Link>
            <Link href="/profile" className="w-8 h-8 rounded-full bg-white/20 md:bg-gray-100 flex items-center justify-center cursor-pointer md:hidden hover:bg-white/30 transition-colors">
                <UserCircle size={24} />
            </Link>
        </div>
      </div>
    </div>
  );
}
