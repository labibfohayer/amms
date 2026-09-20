/* eslint-disable */
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
