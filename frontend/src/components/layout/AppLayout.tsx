/* eslint-disable */
import TopBar from './TopBar';
import BottomNav from './BottomNav';

export default function AppLayout({ children, title = 'AMMS' }: { children: React.ReactNode; title?: string }) {
  return (
    <div className="min-h-screen bg-light-green pb-20">
      <TopBar title={title} />
      <main className="p-4 max-w-md mx-auto">
        {children}
      </main>
      <BottomNav />
    </div>
  );
}
