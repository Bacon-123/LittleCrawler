'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // 直接跳转到数据查看页面
    router.push('/dashboard/data');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p>加载中...</p>
    </div>
  );
}
