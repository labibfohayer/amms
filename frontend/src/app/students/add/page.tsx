/* eslint-disable */
'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function AddStudent() {
    return (
        <AppLayout title="ছাত্র ভর্তি">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <h2 className="text-lg font-bold mb-4">ছাত্র ভর্তির ফরম</h2>
                <p className="text-sm text-gray-500 mb-4">ধাপ ১: ব্যক্তিগত তথ্য</p>
                <form className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">নাম (বাংলা)</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">পিতার নাম (বাংলা)</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <button type="button" className="w-full bg-primary text-white py-2 rounded-lg font-medium hover:bg-primary-dark">পরবর্তী ধাপ</button>
                </form>
            </div>
        </AppLayout>
    )
}
