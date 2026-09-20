/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { UserCircle } from 'lucide-react';

export default function Teachers() {
    const { data: teachers, isLoading } = useQuery({
        queryKey: ['teachers'],
        queryFn: async () => {
            const res = await api.get('/api/teachers/');
            return res.data;
        }
    });

    if (isLoading) return <AppLayout title="শিক্ষক ও কর্মী"><p>লোড হচ্ছে...</p></AppLayout>;

    return (
        <AppLayout title="শিক্ষক ও কর্মী">
            <div className="space-y-3">
                {teachers?.map((t: any) => (
                    <div key={t.id} className="bg-white p-4 rounded-xl shadow-sm flex items-center gap-4">
                        <UserCircle size={40} className="text-gray-400" />
                        <div>
                            <h4 className="font-bold text-gray-800">{t.name_bn || t.user?.name_bn || t.user?.phone}</h4>
                            <p className="text-sm text-gray-500">{t.designation || 'শিক্ষক'}</p>
                        </div>
                    </div>
                ))}
            </div>
        </AppLayout>
    )
}
