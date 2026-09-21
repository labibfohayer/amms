"use client";
import AppLayout from '@/components/layout/AppLayout';

export default function Fees() {
    return (
        <AppLayout title="ফি সংগ্রহ">
            <div className="bg-white p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
                <p className="text-gray-500 mb-4 text-center">ছাত্র নির্বাচন করে ফি ও বেতন সংগ্রহ করুন</p>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">ছাত্র খুঁজুন</label>
                    <input type="text" placeholder="নাম বা আইডি লিখুন..." className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-shadow" />
                </div>
                <button className="w-full bg-primary text-white py-3 rounded-xl font-bold hover:bg-primary-dark transition-colors shadow-lg hover:shadow-xl">খুঁজুন</button>
            </div>
        </AppLayout>
    )
}
