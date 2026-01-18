# -*- coding: utf-8 -*-
"""
人工行为模拟工具类

提供多种延迟策略来模拟真实用户行为，避免被检测为机器人。
"""
import asyncio
import random
from typing import Optional

import config
from src.utils import utils


class HumanBehavior:
    """
    人工行为模拟类

    提供多种延迟策略来模拟真实用户行为，包括：
    - 随机延迟
    - 页面浏览延迟（模拟阅读时间）
    - 操作间隔延迟（模拟鼠标点击/滚动）
    - 会话休息延迟（长时间运行后的休息）
    """

    def __init__(self):
        """初始化人工行为模拟器"""
        self.enabled = getattr(config, 'ENABLE_HUMAN_BEHAVIOR', True)
        self.action_count = 0
        self.break_interval = getattr(config, 'SESSION_BREAK_INTERVAL', 30)

    async def random_delay(self, min_sec: float, max_sec: float) -> None:
        """
        随机延迟

        Args:
            min_sec: 最小延迟时间（秒）
            max_sec: 最大延迟时间（秒）
        """
        if not self.enabled:
            # 如果未启用人工行为模拟，使用固定延迟
            delay_time = getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2)
        else:
            delay_time = random.uniform(min_sec, max_sec)

        await asyncio.sleep(delay_time)
        utils.logger.info(f"[HumanBehavior] Random delay for {delay_time:.2f} seconds")

    async def page_view_delay(self, content_length: int = 0) -> None:
        """
        页面浏览延迟（模拟阅读时间）

        根据内容长度调整延迟时间，内容越长，阅读时间越长

        Args:
            content_length: 内容长度（字符数），用于调整阅读时间
        """
        if not self.enabled:
            delay_time = getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2)
        else:
            min_sec = getattr(config, 'PAGE_VIEW_MIN_SEC', 2.0)
            max_sec = getattr(config, 'PAGE_VIEW_MAX_SEC', 5.0)

            # 根据内容长度适当增加阅读时间
            # 每1000个字符增加约0.5秒
            extra_time = min(content_length / 2000, 2.0)  # 最多增加2秒

            delay_time = random.uniform(min_sec, max_sec) + extra_time

        await asyncio.sleep(delay_time)
        utils.logger.info(f"[HumanBehavior] Page view delay for {delay_time:.2f} seconds")

    async def action_delay(self) -> None:
        """
        操作间隔延迟（模拟鼠标点击/滚动间隔）

        用于模拟用户在页面上的操作间隔，如点击按钮、滚动等
        """
        if not self.enabled:
            delay_time = getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2)
        else:
            min_sec = getattr(config, 'ACTION_INTERVAL_MIN_SEC', 0.5)
            max_sec = getattr(config, 'ACTION_INTERVAL_MAX_SEC', 1.5)
            delay_time = random.uniform(min_sec, max_sec)

        await asyncio.sleep(delay_time)
        utils.logger.info(f"[HumanBehavior] Action delay for {delay_time:.2f} seconds")

    async def comment_crawl_delay(self) -> None:
        """
        评论爬取延迟

        评论通常需要更多时间来阅读，因此使用较长的延迟
        """
        if not self.enabled:
            delay_time = getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2)
        else:
            min_sec = getattr(config, 'COMMENT_CRAWL_MIN_SEC', 1.0)
            max_sec = getattr(config, 'COMMENT_CRAWL_MAX_SEC', 2.5)
            delay_time = random.uniform(min_sec, max_sec)

        await asyncio.sleep(delay_time)
        utils.logger.info(f"[HumanBehavior] Comment crawl delay for {delay_time:.2f} seconds")

    async def session_break_delay(self) -> None:
        """
        会话休息延迟（长时间运行后的休息）

        模拟用户在长时间使用后的休息行为
        """
        if not self.enabled:
            await asyncio.sleep(getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2))
            return

        min_sec = getattr(config, 'SESSION_BREAK_MIN_SEC', 10.0)
        max_sec = getattr(config, 'SESSION_BREAK_MAX_SEC', 30.0)
        delay_time = random.uniform(min_sec, max_sec)

        utils.logger.info(f"[HumanBehavior] Taking a session break for {delay_time:.2f} seconds...")
        await asyncio.sleep(delay_time)
        utils.logger.info("[HumanBehavior] Session break finished, resuming work")

    async def check_and_take_break(self) -> None:
        """
        检查是否需要会话休息

        每执行一定数量的操作后，自动进行休息
        """
        if not self.enabled:
            return

        self.action_count += 1

        if self.action_count >= self.break_interval:
            await self.session_break_delay()
            self.action_count = 0

    def get_random_delay(self, min_sec: float, max_sec: float) -> float:
        """
        获取随机延迟时间（不执行延迟，仅返回时间值）

        用于在需要传递延迟时间的场景

        Args:
            min_sec: 最小延迟时间（秒）
            max_sec: 最大延迟时间（秒）

        Returns:
            float: 随机延迟时间（秒）
        """
        if not self.enabled:
            return getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 2)
        return random.uniform(min_sec, max_sec)

    def get_delay_config(self, action_type: str) -> tuple:
        """
        获取指定操作类型的延迟配置

        Args:
            action_type: 操作类型，如 'page_view', 'action', 'comment', 'session_break'

        Returns:
            tuple: (min_sec, max_sec) 延迟时间区间
        """
        configs = {
            'page_view': (
                getattr(config, 'PAGE_VIEW_MIN_SEC', 2.0),
                getattr(config, 'PAGE_VIEW_MAX_SEC', 5.0)
            ),
            'action': (
                getattr(config, 'ACTION_INTERVAL_MIN_SEC', 0.5),
                getattr(config, 'ACTION_INTERVAL_MAX_SEC', 1.5)
            ),
            'comment': (
                getattr(config, 'COMMENT_CRAWL_MIN_SEC', 1.0),
                getattr(config, 'COMMENT_CRAWL_MAX_SEC', 2.5)
            ),
            'session_break': (
                getattr(config, 'SESSION_BREAK_MIN_SEC', 10.0),
                getattr(config, 'SESSION_BREAK_MAX_SEC', 30.0)
            ),
            'default': (
                getattr(config, 'CRAWLER_MIN_SLEEP_SEC', 1.5),
                getattr(config, 'CRAWLER_MAX_SLEEP_SEC', 3.0)
            )
        }

        return configs.get(action_type, configs['default'])
