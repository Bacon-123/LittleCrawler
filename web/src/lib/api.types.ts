// 数据板块相关类型定义

export interface NoteItem {
  note_id: string;
  title?: string;
  desc?: string;
  nickname?: string;
  type?: string;
  liked_count?: string;
  collected_count?: string;
  comment_count?: string;
  share_count?: string;
  time?: number | string;
  time_formatted?: string;
  note_url?: string;
}

export interface NoteListResponse {
  items: NoteItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface NoteDetail extends NoteItem {
  avatar?: string;
  image_list?: string;
  tag_list?: string;
}

export interface CommentItem {
  comment_id: string;
  content?: string;
  nickname?: string;
  avatar?: string;
  create_time?: number | string;
  time_formatted?: string;
  like_count?: string;
  sub_comment_count?: number;
  ip_location?: string;
  parent_comment_id?: string;
}

export interface CommentListResponse {
  items: CommentItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface DataStatsResponse {
  platforms: Record<string, {
    notes?: number;
    contents?: number;
    comments?: number;
  }>;
  total_notes: number;
  total_comments: number;
}
