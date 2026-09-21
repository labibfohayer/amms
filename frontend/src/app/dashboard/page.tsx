/* eslint-disable */
'use client';
import AppLayout from '@/components/layout/AppLayout';
import StatCard from '@/components/ui/StatCard';
import { useAuth } from '@/contexts/AuthContext';
import { Users, UserCheck, UserX, UserPlus, DollarSign, FileText, Bell, BarChart } from 'lucide-react';
import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function Dashboard() {
    const { user, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) router.push('/login');
        if (user && !['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(user.role)) router.push('/');
    }, [user, isAuthenticated, router]);

    if (!user) return null;

    return (
        <AppLayout title="ড্যাশবোর্ড">
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-primary-dark mb-1">আস-সালামু আলাইকুম, {user.name_bn || 'অধ্যক্ষ মহোদয়'}!</h2>
                <p className="text-sm text-gray-500">{new Date().toLocaleDateString('bn-BD', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
            </div>

            {['principal', 'vice_principal', 'managing_director'].includes(user.role) && (
                <PrincipalDashboard />
            )}

            {user.role === 'teacher' && (
                <>
                    <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                        <h3 className="text-gray-500 text-sm">আপনার বর্তমান বেতন অবস্থা</h3>
                        <p className="text-xl font-bold text-green-700">এই মাসের বেতন পরিশোধ করা হয়েছে</p>
                    </div>
                    <h3 className="font-bold text-gray-700 mb-3">দ্রুত কাজ</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি নিন" />
                        <QuickAction href="/exams" icon={<FileText />} text="রেজাল্ট এন্ট্রি" />
                        <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                    </div>
                </>
            )}

             {user.role === 'staff' && (
                <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                    <h3 className="text-gray-500 text-sm">আপনার বর্তমান বেতন অবস্থা</h3>
                    <p className="text-xl font-bold text-green-700">এই মাসের বেতন পরিশোধ করা হয়েছে</p>
                </div>
            )}
        </AppLayout>
    );
}

function QuickAction({ href, icon, text }: { href: string; icon: React.ReactNode; text: string }) {
    return (
        <Link href={href} className="flex flex-col items-center justify-center p-4 bg-white rounded-xl shadow-sm hover:bg-primary/5 hover:text-primary transition-all border border-gray-100 h-full">
            <div className="text-primary mb-2">{icon}</div>
            <span className="text-sm font-medium text-gray-700">{text}</span>
        </Link>
    );
}

function PrincipalDashboard() {
    const { data, isLoading } = useQuery({
        queryKey: ['dashboard_stats'],
        queryFn: async () => {
            const res = await api.get('/api/reports/dashboard/');
            return res.data;
        }
    });

    if (isLoading) return <div className="text-center p-4 text-gray-500">লোড হচ্ছে...</div>;

    const stats = data || { total_students: 0, today_present: 0, today_absent: 0, total_due_fees: 0, total_teachers: 0, total_staff: 0 };

    return (
        <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <StatCard title="মোট ছাত্র" value={stats.total_students} color="blue" icon={<Users size={24} />} />
                <StatCard title="আজ উপস্থিত" value={stats.today_present} color="green" icon={<UserCheck size={24} />} />
                <StatCard title="আজ অনুপস্থিত" value={stats.today_absent} color="red" icon={<UserX size={24} />} />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                <div className="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-red-500 flex justify-between items-center hover:shadow-md transition-shadow">
                    <div>
                        <h3 className="text-gray-500 text-sm font-medium mb-1">মোট বকেয়া ফি</h3>
                        <p className="text-3xl font-bold text-red-600">৳ {stats.total_due_fees}</p>
                    </div>
                    <div className="bg-red-50 p-3 rounded-full">
                        <DollarSign className="text-red-500" size={32} />
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-orange-500 flex justify-between items-center hover:shadow-md transition-shadow">
                    <div>
                        <h3 className="text-gray-500 text-sm font-medium mb-1">মোট স্টাফ</h3>
                        <p className="text-lg font-medium text-gray-700">শিক্ষক: <span className="font-bold">{stats.total_teachers}</span> | কর্মী: <span className="font-bold">{stats.total_staff}</span></p>
                    </div>
                    <div className="bg-orange-50 p-3 rounded-full">
                        <Users className="text-orange-500" size={32} />
                    </div>
                </div>
            </div>

            <h3 className="text-lg font-bold text-gray-800 mb-4 border-b pb-2">দ্রুত কাজ</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
                <QuickAction href="/students/add" icon={<UserPlus />} text="ছাত্র ভর্তি" />
                <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি" />
                <QuickAction href="/fees" icon={<DollarSign />} text="ফি সংগ্রহ" />
                <QuickAction href="/exams" icon={<FileText />} text="রেজাল্ট" />
                <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                <QuickAction href="/reports" icon={<BarChart />} text="রিপোর্ট" />
            </div>
        </>
    );
}
