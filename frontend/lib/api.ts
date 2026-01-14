import axios from 'axios';

// 获取API基础URL
// 在服务端渲染时使用完整URL，在客户端使用相对路径
const getBaseURL = () => {
  // 服务端渲染时
  if (typeof window === 'undefined') {
    // 从环境变量获取，如果没有则使用默认值
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
  }
  // 客户端使用相对路径（会被Next.js的rewrites代理）
  return '/api';
};

const api = axios.create({
  baseURL: getBaseURL(),
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
