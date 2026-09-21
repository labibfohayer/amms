/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import StudentCard from '@/components/ui/StudentCard';
import { Search, Plus } from 'lucide-react';
import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { useState } from 'react';

export default function Students() {
    const [search, setSearch] = useState('');
    const { data: students, isLoading } = useQuery({
        queryKey: ['students'],
        queryFn: async () => {
            const res = await api.get('/api/students/');
            return res.data;
        }
    });

    return (
        <AppLayout title="ছাত্র-ছাত্রী তালিকা">
            <div className="relative mb-4">
                <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                <input type="text" placeholder="ছাত্র খুঁজুন..." value={search} onChange={e=>setSearch(e.target.value)} className="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
            </div>
            {isLoading ? <p>লোড হচ্ছে...</p> : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {students?.map((s: any) => (
                    <StudentCard key={s.id} student={s} />
                ))}
            </div>
            )}
            <Link href="/students/add" className="fixed bottom-20 right-4 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary-dark z-50">
                <Plus size={24} />
            </Link>
        </AppLayout>
    )
}
