/* eslint-disable */
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
