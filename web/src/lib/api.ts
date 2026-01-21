// API 基础配置和函数 - 动态检测后端地址
const API_BASE = typeof window !== 'undefined'
  ? `${window.location.protocol}//${window.location.hostname}:8080`
  : 'http://localhost:8080';

// 通用请求函数
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }));
    throw new Error(error.detail || '请求失败');
  }

  return response.json();
}

// ========== 数据文件 API ==========
export const dataApi = {
  // 获取文件列表
  getFiles: async (platform?: string, fileType?: string) => {
    const params = new URLSearchParams();
    if (platform) params.append('platform', platform);
    if (fileType) params.append('file_type', fileType);
    const query = params.toString() ? `?${params}` : '';
    return request<{ files: any[] }>(`/api/data/files${query}`);
  },

  // 获取文件内容
  getFileContent: async (filePath: string, limit: number = 100) => {
    return request<{ data: any[]; total: number }>(
      `/api/data/files/${filePath}?preview=true&limit=${limit}`
    );
  },

  // 下载数据统计
  getStats: async () => {
    return request('/api/data/stats');
  },
};

// ========== 数据库查询 API（新增）==========
export const dbApi = {
  // 获取帖子列表
  getNotes: async (platform: string = 'xhs', page: number = 1, pageSize: number = 20, keyword?: string) => {
    const params = new URLSearchParams({
      platform,
      page: page.toString(),
      page_size: pageSize.toString(),
    });
    if (keyword) params.append('keyword', keyword);
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
      total_pages: number;
    }>(`/api/data/notes?${params}`);
  },

  // 获取帖子详情
  getNoteDetail: async (noteId: string, platform: string = 'xhs') => {
    const params = new URLSearchParams({ platform });
    return request<any>(`/api/data/notes/${noteId}?${params}`);
  },

  // 获取帖子评论
  getNoteComments: async (noteId: string, platform: string = 'xhs', page: number = 1, pageSize: number = 50) => {
    const params = new URLSearchParams({
      platform,
      page: page.toString(),
      page_size: pageSize.toString(),
    });
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
      total_pages: number;
    }>(`/api/data/notes/${noteId}/comments?${params}`);
  },

  // 获取数据库统计
  getDbStats: async () => {
    return request<{
      platforms: Record<string, { notes?: number; contents?: number; comments?: number }>;
      total_notes: number;
      total_comments: number;
    }>('/api/data/db-stats');
  },
};

// ========== WebSocket URL ==========
export const getWsUrl = (): string => {
  const wsUrl = API_BASE.replace('http://', 'ws://').replace('https://', 'wss://');
  return `${wsUrl}/api/ws`;
};

// ========== 健康 API ==========
export const healthApi = {
  // 检查 API 健康状态
  check: async () => {
    return request<{ status: string }>('/health');
  },
};
