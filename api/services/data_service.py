# -*- coding: utf-8 -*-
"""
数据服务模块

提供从 SQLite 数据库查询帖子和评论数据的功能：
- 获取帖子列表（分页、筛选）
- 获取单个帖子详情
- 获取帖子评论列表
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# 数据库路径
DB_PATH = Path(__file__).parent.parent.parent / "database" / "sqlite_tables.db"


def _get_db_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    if not DB_PATH.exists():
        print(f"[Data] 数据库不存在: {DB_PATH}")
        # 创建空数据库
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.close()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(row: sqlite3.Row) -> dict:
    """将数据库行转换为字典"""
    return dict(row) if row else {}


def get_available_tables() -> List[str]:
    """
    获取数据库中所有可用的表

    返回表名列表，用于检测哪些平台有数据
    """
    conn = _get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tables


def get_notes_list(
    platform: str = "xhs",
    page: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取帖子列表

    Args:
        platform: 平台 (xhs/zhihu/xhy)
        page: 页码（从1开始）
        page_size: 每页数量
        keyword: 搜索关键词（搜索标题和描述）

    Returns:
        {
            "items": [帖子列表],
            "total": 总数量,
            "page": 当前页,
            "page_size": 每页数量,
            "total_pages": 总页数
        }
    """
    # 根据平台确定表名
    table_map = {
        "xhs": "xhs_note",
        "zhihu": "zhihu_content",
        "xhy": "xhs_note"  # 闲鱼暂时使用小红书表结构
    }

    table_name = table_map.get(platform, "xhs_note")

    # 检查表是否存在
    tables = get_available_tables()
    if table_name not in tables:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0
        }

    conn = _get_db_connection()
    cursor = conn.cursor()

    # 构建查询条件
    where_conditions = []
    params = []

    if keyword:
        if platform == "zhihu":
            where_conditions.append("(title LIKE ? OR desc LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        else:
            where_conditions.append("(title LIKE ? OR desc LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%"])

    where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""

    # 获取总数
    count_sql = f"SELECT COUNT(*) as count FROM {table_name} {where_clause}"
    cursor.execute(count_sql, params)
    total = cursor.fetchone()["count"]

    # 计算分页
    offset = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    # 获取数据
    if platform == "zhihu":
        # 知乎内容表
        data_sql = f"""
            SELECT
                content_id as note_id,
                title,
                desc,
                user_nickname as nickname,
                content_type as type,
                voteup_count as liked_count,
                comment_count,
                created_time as time,
                content_url as note_url
            FROM {table_name}
            {where_clause}
            ORDER BY created_time DESC
            LIMIT ? OFFSET ?
        """
    else:
        # 小红书/闲鱼笔记表
        data_sql = f"""
            SELECT
                note_id,
                title,
                desc,
                nickname,
                type,
                liked_count,
                collected_count,
                comment_count,
                share_count,
                time,
                note_url
            FROM {table_name}
            {where_clause}
            ORDER BY time DESC
            LIMIT ? OFFSET ?
        """

    cursor.execute(data_sql, params + [page_size, offset])
    rows = cursor.fetchall()

    items = []
    for row in rows:
        item = _row_to_dict(row)
        # 转换时间戳为可读格式
        if item.get("time"):
            try:
                timestamp = int(item["time"])
                # 处理毫秒级时间戳（13位）和秒级时间戳（10位）
                if timestamp > 1000000000000:  # 毫秒级
                    timestamp = timestamp / 1000
                item["time_formatted"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                item["time_formatted"] = str(item.get("time", ""))
        items.append(item)

    conn.close()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


def get_note_detail(platform: str, note_id: str) -> Optional[Dict[str, Any]]:
    """
    获取单个帖子详情

    Args:
        platform: 平台 (xhs/zhihu/xhy)
        note_id: 帖子ID

    Returns:
        帖子详情字典，不存在则返回 None
    """
    table_map = {
        "xhs": "xhs_note",
        "zhihu": "zhihu_content",
        "xhy": "xhs_note"
    }

    table_name = table_map.get(platform, "xhs_note")
    id_field = "content_id" if platform == "zhihu" else "note_id"

    conn = _get_db_connection()
    cursor = conn.cursor()

    sql = f"SELECT * FROM {table_name} WHERE {id_field} = ?"
    cursor.execute(sql, (note_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    item = _row_to_dict(row)

    # 转换时间戳
    if item.get("time") or item.get("created_time"):
        time_field = "created_time" if platform == "zhihu" else "time"
        try:
            timestamp = int(item[time_field])
            # 处理毫秒级时间戳（13位）和秒级时间戳（10位）
            if timestamp > 1000000000000:  # 毫秒级
                timestamp = timestamp / 1000
            item["time_formatted"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            item["time_formatted"] = str(item.get(time_field, ""))

    return item


def get_note_comments(
    platform: str,
    note_id: str,
    page: int = 1,
    page_size: int = 50
) -> Dict[str, Any]:
    """
    获取帖子评论列表

    Args:
        platform: 平台 (xhs/zhihu/xhy)
        note_id: 帖子ID
        page: 页码（从1开始）
        page_size: 每页数量

    Returns:
        {
            "items": [评论列表],
            "total": 总数量,
            "page": 当前页,
            "page_size": 每页数量,
            "total_pages": 总页数
        }
    """
    # 根据平台确定评论表名
    comment_table_map = {
        "xhs": "xhs_note_comment",
        "zhihu": "zhihu_comment",
        "xhy": "xhs_note_comment"
    }

    comment_table = comment_table_map.get(platform, "xhs_note_comment")

    # 检查表是否存在
    tables = get_available_tables()
    if comment_table not in tables:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0
        }

    conn = _get_db_connection()
    cursor = conn.cursor()

    # 获取总数
    count_sql = f"SELECT COUNT(*) as count FROM {comment_table} WHERE note_id = ?"
    if platform == "zhihu":
        count_sql = f"SELECT COUNT(*) as count FROM {comment_table} WHERE content_id = ?"

    cursor.execute(count_sql, (note_id,))
    total = cursor.fetchone()["count"]

    # 计算分页
    offset = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    # 获取评论数据
    if platform == "zhihu":
        data_sql = f"""
            SELECT
                comment_id,
                content,
                user_nickname as nickname,
                user_avatar as avatar,
                publish_time as create_time,
                like_count,
                sub_comment_count,
                ip_location
            FROM {comment_table}
            WHERE content_id = ?
            ORDER BY publish_time DESC
            LIMIT ? OFFSET ?
        """
    else:
        data_sql = f"""
            SELECT
                comment_id,
                content,
                nickname,
                avatar,
                create_time,
                like_count,
                sub_comment_count,
                ip_location,
                parent_comment_id
            FROM {comment_table}
            WHERE note_id = ?
            ORDER BY create_time DESC
            LIMIT ? OFFSET ?
        """

    cursor.execute(data_sql, (note_id, page_size, offset))
    rows = cursor.fetchall()

    items = []
    for row in rows:
        item = _row_to_dict(row)
        # 转换时间戳
        if item.get("create_time"):
            try:
                timestamp = int(item["create_time"])
                # 处理毫秒级时间戳（13位）和秒级时间戳（10位）
                if timestamp > 1000000000000:  # 毫秒级
                    timestamp = timestamp / 1000
                item["time_formatted"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                item["time_formatted"] = str(item.get("create_time", ""))
        items.append(item)

    conn.close()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


def get_data_stats() -> Dict[str, Any]:
    """
    获取数据统计信息

    Returns:
        {
            "platforms": {
                "xhs": {"notes": 笔记数, "comments": 评论数},
                "zhihu": {"contents": 内容数, "comments": 评论数}
            },
            "total_notes": 总笔记数,
            "total_comments": 总评论数
        }
    """
    tables = get_available_tables()
    stats = {
        "platforms": {},
        "total_notes": 0,
        "total_comments": 0
    }

    conn = _get_db_connection()
    cursor = conn.cursor()

    # 小红书统计
    if "xhs_note" in tables:
        cursor.execute("SELECT COUNT(*) as count FROM xhs_note")
        xhs_notes = cursor.fetchone()["count"]
        stats["platforms"]["xhs"] = {"notes": xhs_notes}
        stats["total_notes"] += xhs_notes

    if "xhs_note_comment" in tables:
        cursor.execute("SELECT COUNT(*) as count FROM xhs_note_comment")
        xhs_comments = cursor.fetchone()["count"]
        stats["platforms"]["xhs"]["comments"] = xhs_comments
        stats["total_comments"] += xhs_comments

    # 知乎统计
    if "zhihu_content" in tables:
        cursor.execute("SELECT COUNT(*) as count FROM zhihu_content")
        zhihu_contents = cursor.fetchone()["count"]
        stats["platforms"]["zhihu"] = {"contents": zhihu_contents}
        stats["total_notes"] += zhihu_contents

    if "zhihu_comment" in tables:
        cursor.execute("SELECT COUNT(*) as count FROM zhihu_comment")
        zhihu_comments = cursor.fetchone()["count"]
        stats["platforms"]["zhihu"]["comments"] = zhihu_comments
        stats["total_comments"] += zhihu_comments

    conn.close()

    return stats
