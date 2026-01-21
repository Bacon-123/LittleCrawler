// 全局Providers - 包装NextUI、主题、国际化上下文
"use client";

import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { I18nProvider } from "@/contexts/I18nContext";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <NextUIProvider>
      <NextThemesProvider
        attribute="class"
        defaultTheme="light"
        enableSystem={false}
      >
        <I18nProvider>
          {children}
        </I18nProvider>
      </NextThemesProvider>
    </NextUIProvider>
  );
}
