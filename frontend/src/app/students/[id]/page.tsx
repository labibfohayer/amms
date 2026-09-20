/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { UserCircle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { use } from 'react';

export default function StudentDetail({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const { data: student, isLoading: isStudentLoading } = useQuery({
        queryKey: ['student', id],
        queryFn: async () => {
            const res = await api.get(`/api/students/${id}/`);
            return res.data;
        }
    });

    const { data: feesStatus, isLoading: isFeesLoading } = useQuery({
        queryKey: ['fees', id],
        queryFn: async () => {
            const res = await api.get(`/api/fees/students/${id}/status/`);
            return res.data;
        }
    });

    if (isStudentLoading || isFeesLoading) return <AppLayout title="ছাত্রের প্রোফাইল"><p>লোড হচ্ছে...</p></AppLayout>;

    return (
        <AppLayout title="ছাত্রের প্রোফাইল">
            <div className="bg-primary text-white p-6 rounded-xl text-center mb-6 shadow-md relative overflow-hidden">
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mb-3">
                        <UserCircle size={60} className="text-gray-300" />
                    </div>
                    <h2 className="text-2xl font-bold">{student?.name_bn}</h2>
                    <p className="opacity-90">আইডি: {student?.student_id}</p>
                    <span className="mt-2 px-3 py-1 bg-green-500/20 rounded-full text-xs font-medium border border-green-500/30">সক্রিয়</span>
                </div>
            </div>
            
            <div className="flex bg-white rounded-lg p-1 mb-4 shadow-sm">
                <button className="flex-1 py-2 text-sm font-medium bg-primary text-white rounded-md shadow-sm">তথ্য</button>
            </div>
            
            <div className="bg-white p-4 rounded-xl shadow-sm space-y-3">
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">বিভাগ</span>
                    <span className="font-medium text-sm">{student?.classroom?.name || 'N/A'}</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">পিতার নাম</span>
                    <span className="font-medium text-sm">{student?.father_name_bn}</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-2">
                    <span className="text-gray-500 text-sm">বকেয়া ফি</span>
                    <span className="font-medium text-sm text-red-500">৳{feesStatus?.total_due || 0}</span>
                </div>
            </div>
        </AppLayout>
    )
}
