// 侧边栏导航组件 - 简化版（无需认证）
"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import {
  Bug,
  LayoutDashboard,
  Database,
} from "lucide-react";
import { Tooltip } from "@nextui-org/react";
import { useI18n } from "@/contexts/I18nContext";

interface NavItem {
  key: string;
  href: string;
  icon: React.ReactNode;
}

export function Sidebar() {
  const pathname = usePathname();
  const { t } = useI18n();

  const navItems: NavItem[] = [
    {
      key: "dashboard",
      href: "/dashboard",
      icon: <LayoutDashboard size={22} />,
    },
    {
      key: "data",
      href: "/dashboard/data",
      icon: <Database size={22} />,
    },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-16 lg:w-64 bg-content1 border-r border-divider flex flex-col z-40">
      {/* Logo */}
      <div className="h-16 flex items-center justify-center lg:justify-start px-4 border-b border-divider">
        <Bug className="text-primary" size={28} />
        <span className="hidden lg:block ml-2 font-bold text-lg">
          {t("common.appName")}
        </span>
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.key}>
                <Tooltip
                  content={t(`nav.${item.key}`)}
                  placement="right"
                  className="lg:hidden"
                >
                  <Link href={item.href}>
                    <div
                      className={`
                        flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors
                        ${
                          isActive
                            ? "bg-primary text-primary-foreground"
                            : "hover:bg-default-100 text-default-600"
                        }
                      `}
                    >
                      {item.icon}
                      <span className="hidden lg:block">
                        {t(`nav.${item.key}`)}
                      </span>
                    </div>
                  </Link>
                </Tooltip>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* 底部版本信息 */}
      <div className="border-t border-divider p-4">
        <p className="text-xs text-default-400 text-center lg:text-left">
          LittleCrawler v1.0
        </p>
      </div>
    </aside>
  );
}
