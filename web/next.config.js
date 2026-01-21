/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'export',  // 开发模式不需要静态导出
  // distDir: 'out',    // 开发模式不需要
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

module.exports = nextConfig;
