'use client';

import { useState } from 'react';
import { Spinner, Button } from '@nextui-org/react';
import { MessageCircle } from 'lucide-react';

interface Comment {
  comment_id: string;
  content?: string;
  nickname?: string;
  avatar?: string;
  time_formatted?: string;
  like_count?: string;
  sub_comment_count?: number;
  ip_location?: string;
}

interface CommentListProps {
  comments: Comment[];
  total: number;
  loading?: boolean;
  onPageChange?: (page: number) => void;
  currentPage?: number;
  totalPages?: number;
}

export function CommentList({
  comments,
  total,
  loading = false,
  onPageChange,
  currentPage = 1,
  totalPages = 1,
}: CommentListProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <MessageCircle className="w-5 h-5 text-gray-500" />
        <h3 className="text-lg font-semibold">评论 ({total})</h3>
        {loading && <Spinner size="sm" />}
      </div>

      {comments.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          {loading ? '加载中...' : '暂无评论'}
        </div>
      ) : (
        <div className="space-y-4">
          {comments.map((comment) => (
            <div key={comment.comment_id} className="border-b pb-4 last:border-0">
              <div className="flex items-start gap-3">
                {comment.avatar && (
                  <img
                    src={comment.avatar}
                    alt={comment.nickname}
                    className="w-8 h-8 rounded-full"
                  />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-medium text-sm">
                      {comment.nickname || '匿名用户'}
                    </span>
                    {comment.ip_location && (
                      <span className="text-xs text-gray-400">
                        {comment.ip_location}
                      </span>
                    )}
                  </div>
                  <p className="text-gray-700 mt-1 whitespace-pre-wrap">
                    {comment.content}
                  </p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    <span>{comment.time_formatted || '-'}</span>
                    {comment.like_count && (
                      <span>点赞 {comment.like_count}</span>
                    )}
                    {comment.sub_comment_count !== undefined && comment.sub_comment_count > 0 && (
                      <span>{comment.sub_comment_count} 条回复</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 分页 */}
      {totalPages > 1 && onPageChange && (
        <div className="flex justify-center gap-2 mt-4">
          <Button
            size="sm"
            variant="flat"
            disabled={currentPage <= 1}
            onClick={() => onPageChange(currentPage - 1)}
          >
            上一页
          </Button>
          <span className="flex items-center text-sm">
            {currentPage} / {totalPages}
          </span>
          <Button
            size="sm"
            variant="flat"
            disabled={currentPage >= totalPages}
            onClick={() => onPageChange(currentPage + 1)}
          >
            下一页
          </Button>
        </div>
      )}
    </div>
  );
}
