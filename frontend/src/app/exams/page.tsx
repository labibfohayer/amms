/* eslint-disable */
'use client';
import AppLayout from '@/components/layout/AppLayout';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { FileText, Plus, CheckCircle, Clock } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

export default function Exams() {
    const { user } = useAuth();
    const { data: exams, isLoading, error } = useQuery({
        queryKey: ['exams'],
        queryFn: async () => {
            const res = await api.get('/api/exams/');
            return res.data;
        }
    });

    return (
        <AppLayout title="পরীক্ষা সমূহ">
            <div className="mb-6 flex justify-between items-end">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800">পরীক্ষার তালিকা</h2>
                    <p className="text-gray-500 text-sm">সকল ক্লাস টেস্ট এবং টার্ম পরীক্ষার তথ্য</p>
                </div>
            </div>

            {isLoading ? (
                <div className="flex flex-col items-center justify-center p-12 bg-white rounded-2xl shadow-sm border border-gray-100">
                    <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-4"></div>
                    <p className="text-gray-500 font-medium">পরীক্ষার তালিকা লোড হচ্ছে...</p>
                </div>
            ) : error ? (
                <div className="bg-red-50 text-red-500 p-6 rounded-2xl border border-red-100 text-center">
                    ডেটা লোড করতে সমস্যা হয়েছে। দয়া করে আবার চেষ্টা করুন।
                </div>
            ) : exams?.length === 0 ? (
                <div className="bg-white p-12 rounded-2xl shadow-sm border border-gray-100 text-center">
                    <FileText className="mx-auto text-gray-300 mb-4" size={48} />
                    <h3 className="text-xl font-bold text-gray-700 mb-2">কোনো পরীক্ষা পাওয়া যায়নি</h3>
                    <p className="text-gray-500">এখনো কোনো পরীক্ষার রুটিন বা তালিকা তৈরি করা হয়নি।</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {exams.map((exam: any) => (
                        <Link href={`/exams/${exam.id}`} key={exam.id} className="bg-white p-6 rounded-2xl shadow-sm hover:shadow-md transition-all border border-gray-100 group">
                            <div className="flex justify-between items-start mb-4">
                                <div className="bg-primary/10 p-3 rounded-xl text-primary group-hover:scale-110 transition-transform">
                                    <FileText size={24} />
                                </div>
                                {exam.is_published ? (
                                    <span className="flex items-center gap-1 text-xs font-bold text-green-600 bg-green-50 px-2.5 py-1 rounded-full border border-green-100">
                                        <CheckCircle size={14} /> প্রকাশিত
                                    </span>
                                ) : (
                                    <span className="flex items-center gap-1 text-xs font-bold text-orange-500 bg-orange-50 px-2.5 py-1 rounded-full border border-orange-100">
                                        <Clock size={14} /> অপ্রকাশিত
                                    </span>
                                )}
                            </div>
                            <h3 className="text-xl font-bold text-gray-800 mb-1">{exam.title || exam.name || 'পরীক্ষা'}</h3>
                            <p className="text-sm font-medium text-primary mb-3">{exam.term || 'সাধারণ'} | বছর: {exam.year || new Date().getFullYear()}</p>
                            
                            <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-50">
                                <span>তারিখ: {exam.start_date || 'নির্ধারিত হয়নি'}</span>
                                <span className="font-semibold text-primary group-hover:underline">বিস্তারিত দেখুন &rarr;</span>
                            </div>
                        </Link>
                    ))}
                </div>
            )}

            {user && ['principal', 'teacher'].includes(user.role) && (
                <button className="fixed bottom-[88px] md:bottom-8 right-4 md:right-8 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg shadow-primary/30 hover:bg-primary-dark hover:scale-105 transition-all z-40">
                    <Plus size={24} />
                </button>
            )}
        </AppLayout>
    )
}
