/* eslint-disable */
import TopBar from './TopBar';
import BottomNav from './BottomNav';

export default function AppLayout({ children, title = 'AMMS' }: { children: React.ReactNode; title?: string }) {
  return (
    <div className="min-h-screen bg-light-green md:flex">
      <BottomNav />
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen">
        <TopBar title={title} />
        <main className="p-4 w-full max-w-6xl mx-auto flex-1 pb-24 md:pb-8">
          {children}
        </main>
      </div>
    </div>
  );
}
