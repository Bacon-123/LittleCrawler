"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { Button, Chip } from "@nextui-org/react";
import {
  Bug,
  LayoutDashboard,
  Database,
  Sun,
  Moon,
  Languages,
  RefreshCw,
} from "lucide-react";
import { useTheme } from "next-themes";
import { useI18n } from "@/contexts/I18nContext";
import { healthApi } from "@/lib/api";

// 导航项配置
const NAV_ITEMS = [
  { key: "dashboard", href: "/dashboard", icon: LayoutDashboard, label: "仪表盘" },
  { key: "data", href: "/dashboard/data", icon: Database, label: "数据管理" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { t, locale, setLocale } = useI18n();
  const [apiStatus, setApiStatus] = useState<"healthy" | "unhealthy" | "checking">("checking");

  const checkApiHealth = async () => {
    setApiStatus("checking");
    try {
      await healthApi.check();
      setApiStatus("healthy");
    } catch {
      setApiStatus("unhealthy");
    }
  };

  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-background">
      {/* 左侧固定侧边栏 - 240px */}
      <aside className="w-60 bg-content1 border-r border-divider flex flex-col flex-shrink-0">
        {/* Logo 区域 */}
        <div className="h-16 flex items-center px-5 border-b border-divider">
          <Bug className="text-primary" size={28} />
          <div className="ml-2">
            <span className="font-bold text-lg">LittleCrawler</span>
            <span className="text-xs text-default-400 block -mt-1">数据管理平台</span>
          </div>
        </div>

        {/* 导航菜单 */}
        <nav className="flex-1 py-4 px-3 space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
            const Icon = item.icon;
            return (
              <Link
                key={item.key}
                href={item.href}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all
                  ${isActive
                    ? "bg-primary text-primary-foreground font-medium"
                    : "hover:bg-default-100 text-default-600"
                  }
                `}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* 底部版本信息 */}
        <div className="p-4 border-t border-divider">
          <p className="text-xs text-default-400">v1.0.0</p>
          <p className="text-xs text-default-400 mt-1">© 2025</p>
        </div>
      </aside>

      {/* 右侧内容区 */}
      <div className="flex-1 flex flex-col overflow-hidden bg-default-50">
        {/* 顶部 Header 工具栏 */}
        <header className="h-16 bg-content1 border-b border-divider flex items-center justify-between px-6 flex-shrink-0">
          {/* 左侧：页面标题 */}
          <h1 className="text-xl font-semibold">
            {NAV_ITEMS.find(item => pathname === item.href)?.label ||
             (pathname.startsWith("/dashboard/data") ? "数据管理" : "仪表盘")}
          </h1>

          {/* 右侧：工具栏 */}
          <div className="flex items-center gap-3">
            <Chip
              color={apiStatus === "healthy" ? "success" : apiStatus === "unhealthy" ? "danger" : "warning"}
              variant="dot"
              size="sm"
            >
              ● API {apiStatus === "checking" ? "检测中" : apiStatus === "healthy" ? "正常" : "异常"}
            </Chip>

            <Button
              isIconOnly
              size="sm"
              variant="light"
              onClick={() => setLocale(locale === "zh" ? "en" : "zh")}
            >
              <Languages size={18} />
            </Button>

            <Button
              isIconOnly
              size="sm"
              variant="light"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
            </Button>

            <Button
              isIconOnly
              size="sm"
              variant="light"
              onClick={checkApiHealth}
            >
              <RefreshCw size={18} />
            </Button>
          </div>
        </header>

        {/* 主内容区 - 可滚动 */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
