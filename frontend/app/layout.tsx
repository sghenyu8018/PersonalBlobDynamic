import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "个人技术博客",
    template: "%s | 个人技术博客",
  },
  description: "个人技术博客系统，分享技术经验和思考",
  keywords: ["技术博客", "个人博客", "编程", "开发"],
  authors: [{ name: "博主" }],
  openGraph: {
    type: "website",
    locale: "zh_CN",
    url: "https://example.com",
    siteName: "个人技术博客",
    title: "个人技术博客",
    description: "个人技术博客系统，分享技术经验和思考",
  },
  twitter: {
    card: "summary_large_image",
    title: "个人技术博客",
    description: "个人技术博客系统，分享技术经验和思考",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
