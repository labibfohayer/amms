/* eslint-disable */
'use client';
import AppLayout from '@/components/layout/AppLayout';

export default function AddNotice() {
    return (
        <AppLayout title="নোটিশ দিন">
            <div className="bg-white p-4 rounded-xl shadow-sm">
                <form className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">শিরোনাম</label>
                        <input type="text" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">বিস্তারিত</label>
                        <textarea className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary h-32"></textarea>
                    </div>
                    <button type="button" className="w-full bg-primary text-white py-2 rounded-lg font-medium hover:bg-primary-dark">প্রকাশ করুন</button>
                </form>
            </div>
        </AppLayout>
    )
}
