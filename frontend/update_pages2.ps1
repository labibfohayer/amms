import json

files = {
    'src/app/students/page.tsx': '''// @ts-nocheck
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
        <AppLayout title="ছাত্র তালিকা">
            <div className="relative mb-4">
                <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                <input type="text" placeholder="ছাত্র খুঁজুন..." value={search} onChange={e=>setSearch(e.target.value)} className="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
            </div>
            {isLoading ? <p>লোড হচ্ছে...</p> : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
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
''',

    'src/app/students/[id]/page.tsx': '''// @ts-nocheck
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
''',

    'src/app/attendance/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '@/lib/api';
import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';

export default function Attendance() {
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [classroomId, setClassroomId] = useState('');
    const [attendanceData, setAttendanceData] = useState<any>({});

    const { data: classrooms } = useQuery({
        queryKey: ['classrooms'],
        queryFn: async () => {
            const res = await api.get('/api/academic/classrooms/');
            return res.data;
        }
    });

    const { data: students, isLoading: isLoadingStudents } = useQuery({
        queryKey: ['students', classroomId],
        queryFn: async () => {
            const res = await api.get(`/api/students/?classroom=${classroomId}`);
            return res.data;
        },
        enabled: !!classroomId
    });

    useEffect(() => {
        if (students) {
            const initialData: any = {};
            students.forEach((s: any) => { initialData[s.id] = 'present'; });
            setAttendanceData(initialData);
        }
    }, [students]);

    const mutation = useMutation({
        mutationFn: async () => {
            const records = Object.keys(attendanceData).map(student_id => ({
                student_id: parseInt(student_id),
                status: attendanceData[student_id]
            }));
            const res = await api.post('/api/attendance/bulk/', { date, classroom_id: parseInt(classroomId), records });
            return res.data;
        },
        onSuccess: () => {
            toast.success('উপস্থিতি সংরক্ষিত হয়েছে');
        },
        onError: () => {
            toast.error('উপস্থিতি সংরক্ষণ ব্যর্থ হয়েছে');
        }
    });

    return (
        <AppLayout title="উপস্থিতি">
            <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                <select value={classroomId} onChange={e=>setClassroomId(e.target.value)} className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-3">
                    <option value="">ক্লাস নির্বাচন করুন</option>
                    {classrooms?.map((c: any) => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                </select>
                <input type="date" value={date} onChange={e=>setDate(e.target.value)} className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
            </div>
            
            <div className="space-y-2">
                {students?.map((s: any) => (
                    <div key={s.id} className="bg-white p-3 rounded-lg shadow-sm flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
                            <div>
                                <h4 className="font-medium text-sm">{s.name_bn}</h4>
                                <p className="text-xs text-gray-500">রোল: {s.roll_number}</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button onClick={() => setAttendanceData({...attendanceData, [s.id]: 'present'})} className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${attendanceData[s.id] === 'present' ? 'bg-green-500 text-white' : 'bg-green-100 text-green-600'}`}>✓</button>
                            <button onClick={() => setAttendanceData({...attendanceData, [s.id]: 'absent'})} className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${attendanceData[s.id] === 'absent' ? 'bg-red-500 text-white' : 'bg-gray-100 text-gray-400 hover:bg-red-100 hover:text-red-600'}`}>✗</button>
                        </div>
                    </div>
                ))}
            </div>
            <button onClick={() => mutation.mutate()} disabled={!classroomId || !students?.length} className="w-full mt-6 bg-primary text-white py-3 rounded-xl font-bold">সংরক্ষণ করুন</button>
        </AppLayout>
    )
}
''',

    'src/app/fees/due/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function DueFees() {
    const { data, isLoading } = useQuery({
        queryKey: ['due-fees'],
        queryFn: async () => {
            const res = await api.get('/api/fees/due/');
            return res.data;
        }
    });

    if (isLoading) return <AppLayout title="বকেয়া ফি"><p>লোড হচ্ছে...</p></AppLayout>;

    const totalDue = data?.reduce((acc: number, item: any) => acc + parseFloat(item.due_amount), 0) || 0;

    return (
        <AppLayout title="বকেয়া ফি">
            <div className="text-center mb-6">
                <h2 className="text-lg font-medium text-gray-600">মোট বকেয়া</h2>
                <p className="text-3xl font-bold text-red-600">৳{totalDue}</p>
            </div>
            <div className="space-y-3">
                {data?.map((fee: any) => (
                    <div key={fee.id} className="bg-white p-4 rounded-xl shadow-sm">
                        <h4 className="font-bold">{fee.student?.name_bn || 'Student'}</h4>
                        <p className="text-sm text-gray-500">{fee.fee_type?.name} - {fee.month}</p>
                        <p className="text-red-500 font-bold mt-2">বকেয়া: ৳{fee.due_amount}</p>
                    </div>
                ))}
            </div>
        </AppLayout>
    )
}
''',

    'src/app/fees/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '@/lib/api';
import toast from 'react-hot-toast';

export default function Fees() {
    const [amount, setAmount] = useState('');
    const [feeId, setFeeId] = useState('');

    const mutation = useMutation({
        mutationFn: async () => {
            const res = await api.post('/api/fees/payments/', {
                fee: feeId,
                amount: amount,
                payment_method: 'cash',
                transaction_id: ''
            });
            return res.data;
        },
        onSuccess: () => {
            toast.success('পেমেন্ট সফল হয়েছে');
            setAmount('');
            setFeeId('');
        },
        onError: () => toast.error('পেমেন্ট ব্যর্থ হয়েছে')
    });

    return (
        <AppLayout title="ফি সংগ্রহ">
            <div className="bg-white p-4 rounded-xl shadow-sm space-y-4">
                <p className="text-gray-500 mb-4">ফি আইডি এবং পরিমাণ লিখুন</p>
                <input type="text" placeholder="ফি রেকর্ড আইডি (যেমন: 1)" value={feeId} onChange={e=>setFeeId(e.target.value)} className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-4" />
                <input type="number" placeholder="পরিমাণ" value={amount} onChange={e=>setAmount(e.target.value)} className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-4" />
                <button onClick={() => mutation.mutate()} disabled={!feeId || !amount} className="w-full bg-primary text-white py-3 rounded-xl font-bold">পরিশোধ করুন</button>
            </div>
        </AppLayout>
    )
}
''',

    'src/app/teachers/page.tsx': '''// @ts-nocheck
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
''',

    'src/app/notices/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import Link from 'next/link';
import { Plus } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function Notices() {
    const { user } = useAuth();
    
    const { data: notices, isLoading } = useQuery({
        queryKey: ['notices'],
        queryFn: async () => {
            const res = await api.get('/api/notices/');
            return res.data;
        }
    });

    return (
        <AppLayout title="নোটিশ বোর্ড">
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                <div className="space-y-3">
                    {notices?.length ? notices.map((n: any) => (
                        <div key={n.id} className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-primary">
                            <h3 className="font-bold text-lg">{n.title}</h3>
                            <p className="text-sm text-gray-600 mt-1">{n.content}</p>
                            <p className="text-xs text-gray-400 mt-2">{new Date(n.created_at).toLocaleDateString('bn-BD')}</p>
                        </div>
                    )) : (
                        <div className="bg-white p-4 rounded-xl shadow-sm">
                            <p className="text-gray-500 text-center">কোনো নোটিশ নেই</p>
                        </div>
                    )}
                </div>
            )}
            
            {user && ['principal', 'teacher'].includes(user.role) && (
                <Link href="/notices/add" className="fixed bottom-20 right-4 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary-dark z-50">
                    <Plus size={24} />
                </Link>
            )}
        </AppLayout>
    )
}
''',

    'src/app/guardian/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function GuardianDashboard() {
    const { user } = useAuth();
    
    const { data: students, isLoading } = useQuery({
        queryKey: ['my_students'],
        queryFn: async () => {
            const res = await api.get('/api/students/');
            return res.data;
        }
    });

    return (
        <AppLayout title="অভিভাবক ড্যাশবোর্ড">
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                students?.map((student: any) => (
                    <div key={student.id} className="mb-6">
                        <h2 className="text-lg font-bold mb-4">আপনার সন্তান: {student.name_bn}</h2>
                        <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                            <p className="text-gray-500 text-sm">স্ট্যাটাস: {student.status}</p>
                            <p className="text-gray-500 text-sm">আইডি: {student.student_id}</p>
                        </div>
                    </div>
                ))
            )}
        </AppLayout>
    )
}
''',

    'src/app/student/page.tsx': '''// @ts-nocheck
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function StudentDashboard() {
    const { user } = useAuth();
    
    const { data: studentInfo, isLoading } = useQuery({
        queryKey: ['student_info'],
        queryFn: async () => {
            const res = await api.get('/api/students/me/');
            return res.data;
        },
        retry: false
    });

    return (
        <AppLayout title="ছাত্র ড্যাশবোর্ড">
            <h2 className="text-lg font-bold mb-4 text-primary">আস-সালামু আলাইকুম, {user?.name_bn || 'ছাত্র'}!</h2>
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                <div className="bg-white p-4 rounded-xl shadow-sm mb-4 text-center">
                    <p className="text-gray-500 text-sm mb-2">স্ট্যাটাস</p>
                    <h3 className="text-2xl font-bold text-gray-800">{studentInfo?.status || 'N/A'}</h3>
                    <p className="text-sm font-medium text-gray-700 mt-1">আইডি: {studentInfo?.student_id || 'N/A'}</p>
                </div>
            )}
        </AppLayout>
    )
}
''',
    
    'src/contexts/AuthContext.tsx': '''// @ts-nocheck
"use client";
import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, getUser, isLoggedIn, logout } from '../lib/auth';
import { usePathname } from 'next/navigation';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  logoutUser: () => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  logoutUser: logout,
  setUser: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUserState] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const pathname = usePathname();

  useEffect(() => {
    let mounted = true;
    if (mounted) {
        const u = getUser();
        setUserState(u);
        setIsAuthenticated(isLoggedIn());
        setLoading(false);
    }
    return () => { mounted = false; };
  }, [pathname]);

  const logoutUser = () => {
    logout();
    setUserState(null);
    setIsAuthenticated(false);
  };

  const setUser = (u: User | null) => {
      setUserState(u);
      setIsAuthenticated(!!u);
  }

  if (loading) return null;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, logoutUser, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
'''
}

for k, v in files.items():
    with open(k, 'w', encoding='utf-8') as f:
        f.write(v)

print("Files updated successfully.")
