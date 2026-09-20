/* eslint-disable */
import { ReactNode } from 'react';

export default function StatCard({ title, value, subtitle, color, icon }: { title: string; value: string | number; subtitle?: string; color: string; icon?: ReactNode }) {
  const colorMap: Record<string, string> = {
    blue: 'border-blue-500 text-blue-700',
    green: 'border-green-500 text-green-700',
    red: 'border-red-500 text-red-700',
    orange: 'border-orange-500 text-orange-700',
    purple: 'border-purple-500 text-purple-700',
  };
  return (
    <div className={`bg-white p-4 rounded-xl shadow-sm border-l-4 ${colorMap[color] || 'border-gray-500'}`}>
        <div className="flex justify-between items-start">
            <div>
                <p className="text-gray-500 text-sm">{title}</p>
                <h3 className="text-2xl font-bold mt-1">{value}</h3>
                {subtitle && <p className="text-xs mt-1 opacity-80">{subtitle}</p>}
            </div>
            {icon && <div className="opacity-80">{icon}</div>}
        </div>
    </div>
  );
}
