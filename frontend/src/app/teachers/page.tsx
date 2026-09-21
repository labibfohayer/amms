'use client';
import AppLayout from '@/components/layout/AppLayout';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { UserCircle, Plus, Search } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

export default function Teachers() {
    const { user } = useAuth();
    const [search, setSearch] = useState('');
    const { data: teachers, isLoading } = useQuery({
        queryKey: ['teachers'],
        queryFn: async () => {
            const res = await api.get('/api/teachers/');
            return res.data;
        }
    });

    return (
        <AppLayout title="শিক্ষক ও স্টাফ">
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800">শিক্ষক ও স্টাফ তালিকা</h2>
                <p className="text-gray-500 text-sm">সকল শিক্ষক এবং কর্মচারীদের তথ্য</p>
            </div>

            <div className="relative mb-6">
                <Search className="absolute left-4 top-3.5 text-gray-400" size={20} />
                <input type="text" placeholder="নাম বা মোবাইল নম্বর দিয়ে খুঁজুন..." value={search} onChange={e=>setSearch(e.target.value)} className="w-full pl-12 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary shadow-sm" />
            </div>

            {isLoading ? (
                <div className="flex flex-col items-center justify-center p-12 bg-white rounded-2xl shadow-sm border border-gray-100">
                    <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-4"></div>
                    <p className="text-gray-500 font-medium">শিক্ষকদের তথ্য লোড হচ্ছে...</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {teachers?.filter((t: any) => t.name.toLowerCase().includes(search.toLowerCase()) || (t.name_bn && t.name_bn.includes(search)) || t.phone.includes(search)).map((t: any) => (
                        <div key={t.id} className="bg-white p-5 rounded-2xl shadow-sm flex items-center gap-4 border border-gray-100 hover:shadow-md transition-all">
                            {t.photo ? (
                                <img src={t.photo} alt={t.name} className="w-16 h-16 rounded-full object-cover border-2 border-primary/20" />
                            ) : (
                                <div className="w-16 h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                                    <UserCircle size={32} />
                                </div>
                            )}
                            <div className="flex-1 overflow-hidden">
                                <h4 className="font-bold text-gray-800 text-lg truncate">{t.name_bn || t.name}</h4>
                                <p className="text-sm text-primary font-medium">{t.designation_bn || t.designation || 'শিক্ষক'}</p>
                                <p className="text-xs text-gray-500 mt-1">{t.phone}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {user && ['principal', 'vice_principal', 'managing_director'].includes(user.role) && (
                <Link href="/teachers/add" className="fixed bottom-[88px] md:bottom-8 right-4 md:right-8 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg shadow-primary/30 hover:bg-primary-dark hover:scale-105 transition-all z-40">
                    <Plus size={24} />
                </Link>
            )}
        </AppLayout>
    )
}
