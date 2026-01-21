# -*- coding: utf-8 -*-
"""
数据相关数据模型

定义帖子、评论相关的请求和响应模型
"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field


class NoteItem(BaseModel):
    """帖子项模型"""
    note_id: str = Field(..., description="帖子ID")
    title: Optional[str] = Field(None, description="标题")
    desc: Optional[str] = Field(None, description="描述")
    nickname: Optional[str] = Field(None, description="作者昵称")
    type: Optional[str] = Field(None, description="类型")
    liked_count: Optional[str] = Field(None, description="点赞数")
    collected_count: Optional[str] = Field(None, description="收藏数")
    comment_count: Optional[str] = Field(None, description="评论数")
    share_count: Optional[str] = Field(None, description="分享数")
    time: Optional[Any] = Field(None, description="发布时间戳")
    time_formatted: Optional[str] = Field(None, description="格式化时间")
    note_url: Optional[str] = Field(None, description="帖子链接")


class NoteListResponse(BaseModel):
    """帖子列表响应模型"""
    items: List[NoteItem] = Field(default_factory=list, description="帖子列表")
    total: int = Field(0, description="总数量")
    page: int = Field(1, description="当前页")
    page_size: int = Field(20, description="每页数量")
    total_pages: int = Field(0, description="总页数")


class NoteDetail(BaseModel):
    """帖子详情模型"""
    note_id: str = Field(..., description="帖子ID")
    title: Optional[str] = Field(None, description="标题")
    desc: Optional[str] = Field(None, description="描述")
    nickname: Optional[str] = Field(None, description="作者昵称")
    avatar: Optional[str] = Field(None, description="作者头像")
    type: Optional[str] = Field(None, description="类型")
    liked_count: Optional[str] = Field(None, description="点赞数")
    collected_count: Optional[str] = Field(None, description="收藏数")
    comment_count: Optional[str] = Field(None, description="评论数")
    share_count: Optional[str] = Field(None, description="分享数")
    time: Optional[Any] = Field(None, description="发布时间戳")
    time_formatted: Optional[str] = Field(None, description="格式化时间")
    note_url: Optional[str] = Field(None, description="帖子链接")
    image_list: Optional[str] = Field(None, description="图片列表")
    tag_list: Optional[str] = Field(None, description="标签列表")


class CommentItem(BaseModel):
    """评论项模型"""
    comment_id: str = Field(..., description="评论ID")
    content: Optional[str] = Field(None, description="评论内容")
    nickname: Optional[str] = Field(None, description="评论者昵称")
    avatar: Optional[str] = Field(None, description="评论者头像")
    create_time: Optional[Any] = Field(None, description="评论时间戳")
    time_formatted: Optional[str] = Field(None, description="格式化时间")
    like_count: Optional[str] = Field(None, description="点赞数")
    sub_comment_count: Optional[int] = Field(None, description="子评论数")
    ip_location: Optional[str] = Field(None, description="IP地理位置")
    parent_comment_id: Optional[str] = Field(None, description="父评论ID")


class CommentListResponse(BaseModel):
    """评论列表响应模型"""
    items: List[CommentItem] = Field(default_factory=list, description="评论列表")
    total: int = Field(0, description="总数量")
    page: int = Field(1, description="当前页")
    page_size: int = Field(50, description="每页数量")
    total_pages: int = Field(0, description="总页数")


class DataStats(BaseModel):
    """数据统计模型"""
    notes: Optional[int] = Field(None, description="笔记数")
    contents: Optional[int] = Field(None, description="内容数（知乎）")
    comments: Optional[int] = Field(None, description="评论数")


class PlatformStats(BaseModel):
    """平台统计模型"""
    xhs: Optional[DataStats] = Field(None, description="小红书统计")
    zhihu: Optional[DataStats] = Field(None, description="知乎统计")


class DataStatsResponse(BaseModel):
    """数据统计响应模型"""
    platforms: dict = Field(default_factory=dict, description="各平台统计")
    total_notes: int = Field(0, description="总帖子数")
    total_comments: int = Field(0, description="总评论数")
