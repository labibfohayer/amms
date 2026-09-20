/* eslint-disable */
import { Bell, UserCircle } from 'lucide-react';
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
