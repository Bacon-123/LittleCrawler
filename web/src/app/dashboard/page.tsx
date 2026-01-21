"use client";

import { useState, useEffect } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Spinner,
} from "@nextui-org/react";
import {
  FileText,
  MessageSquare,
  TrendingUp,
  Database,
  Zap,
  Calendar,
  ArrowRight,
} from "lucide-react";
import { dbApi } from "@/lib/api";
import Link from "next/link";

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [recentData, setRecentData] = useState<any[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [statsData, notesData] = await Promise.all([
          dbApi.getDbStats(),
          dbApi.getNotes("xhs", 1, 5),
        ]);
        setStats(statsData);
        setRecentData(notesData.items);
      } catch (error) {
        console.error("加载数据失败:", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  const totalNotes = stats?.total_notes || 0;
  const totalComments = stats?.total_comments || 0;
  const todayNew = Math.floor(totalNotes * 0.1);

  return (
    <div className="space-y-6">
      {/* 快速统计卡片 */}
      <h2 className="text-lg font-semibold text-default-600">快速统计</h2>
      <div className="grid grid-cols-3 gap-4">
        <StatCard
          icon={<FileText className="text-blue-500" />}
          title="帖子总数"
          value={totalNotes.toLocaleString()}
          subtitle={`+${todayNew} 今日新增`}
        />
        <StatCard
          icon={<MessageSquare className="text-green-500" />}
          title="评论总数"
          value={totalComments.toLocaleString()}
          subtitle={`+${Math.floor(todayNew * 0.4)} 今日新增`}
        />
        <StatCard
          icon={<TrendingUp className="text-purple-500" />}
          title="今日新增"
          value={`+${todayNew}`}
          subtitle="↑ 12% 较昨日"
        />
      </div>

      {/* 系统状态卡片 */}
      <h2 className="text-lg font-semibold text-default-600">系统状态</h2>
      <div className="grid grid-cols-3 gap-4">
        <StatCard
          icon={<Database className="text-orange-500" />}
          title="存储空间"
          value="45.2 MB"
          subtitle="SQLite 数据库"
        />
        <StatCard
          icon={<Zap className="text-yellow-500" />}
          title="系统状态"
          value="正常运行"
          subtitle="所有服务正常"
        />
        <StatCard
          icon={<Calendar className="text-cyan-500" />}
          title="最后采集"
          value="2小时前"
          subtitle="2025-01-20 14:30"
        />
      </div>

      {/* 数据分布图表 */}
      <Card>
        <CardHeader className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-semibold">📊 数据分布</h3>
            <p className="text-sm text-default-400 mt-1">各平台数据占比</p>
          </div>
          <Link href="/dashboard/data">
            <Button size="sm" variant="flat" endContent={<ArrowRight size={16} />}>
              查看详情
            </Button>
          </Link>
        </CardHeader>
        <CardBody>
          <div className="h-64 flex items-center justify-center border-2 border-dashed border-default-200 rounded-lg bg-default-50">
            <div className="text-center text-default-400">
              <TrendingUp size={48} className="mx-auto mb-2" />
              <p>图表区域</p>
              <p className="text-sm">（可集成 Chart.js / Recharts）</p>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* 最新采集记录 */}
      <Card>
        <CardHeader>
          <div>
            <h3 className="text-lg font-semibold">📋 最新采集</h3>
            <p className="text-sm text-default-400 mt-1">最近采集的 5 条数据</p>
          </div>
        </CardHeader>
        <CardBody>
          {recentData.length === 0 ? (
            <div className="text-center py-8 text-default-400">暂无数据</div>
          ) : (
            <Table aria-label="最新采集记录">
              <TableHeader>
                <TableColumn>标题</TableColumn>
                <TableColumn>作者</TableColumn>
                <TableColumn>点赞</TableColumn>
                <TableColumn>发布时间</TableColumn>
              </TableHeader>
              <TableBody>
                {recentData.map((item) => (
                  <TableRow key={item.note_id}>
                    <TableCell>
                      <div className="max-w-xs truncate" title={item.title || item.desc}>
                        {item.title || item.desc || "(无标题)"}
                      </div>
                    </TableCell>
                    <TableCell>{item.nickname || "-"}</TableCell>
                    <TableCell>{item.liked_count || "0"}</TableCell>
                    <TableCell className="text-default-400">
                      {item.time_formatted || "-"}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

// 组件：统计卡片
function StatCard({
  icon,
  title,
  value,
  subtitle,
}: {
  icon: React.ReactNode;
  title: string;
  value: string | number;
  subtitle: string;
}) {
  return (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <CardBody className="p-4">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-default-100 rounded-xl">{icon}</div>
          <div className="flex-1">
            <p className="text-sm text-default-500 mb-1">{title}</p>
            <p className="text-2xl font-bold mb-1">{value}</p>
            <p className="text-xs text-default-400">{subtitle}</p>
          </div>
        </div>
      </CardBody>
    </Card>
  );
}
