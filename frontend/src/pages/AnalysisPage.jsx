import { BarChart3, TrendingUp, Users, Award, Target, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import Notice from "../components/Notice";

const RANGE_LABELS = [
  { key: "range0_59", label: "不及格", color: "#ef4444" },
  { key: "range60_69", label: "60-69", color: "#f97316" },
  { key: "range70_79", label: "70-79", color: "#eab308" },
  { key: "range80_89", label: "80-89", color: "#22c55e" },
  { key: "range90_100", label: "90-100", color: "#1f7a6d" },
];

function DistributionBar({ distribution, total }) {
  const max = Math.max(...RANGE_LABELS.map((r) => distribution[r.key]), 1);

  return (
    <div className="dist-wrap">
      {RANGE_LABELS.map((range) => {
        const count = distribution[range.key] || 0;
        const width = (count / max) * 100;
        const percent = total ? ((count / total) * 100).toFixed(1) : 0;
        return (
          <div key={range.key} className="dist-row">
            <div className="dist-label">
              <span className="dist-dot" style={{ background: range.color }} />
              <span>{range.label}</span>
            </div>
            <div className="dist-bar-track">
              <div className="dist-bar-fill" style={{ width: `${width}%`, background: range.color }} />
            </div>
            <div className="dist-count">
              <strong>{count}</strong>
              <span>({percent}%)</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function CourseCard({ data }) {
  return (
    <div className="panel course-card">
      <div className="course-head">
        <div>
          <h2 className="course-title">{data.courseName}</h2>
          <p className="course-meta">
            {data.courseCode} · {data.semester} · {data.teacher} · {data.credit}学分
          </p>
        </div>
      </div>

      <div className="metric-grid analysis-metrics">
        <div className="metric">
          <span>
            <Users size={14} className="metric-icon" />
            学生人数
          </span>
          <strong>{data.studentCount}</strong>
        </div>
        <div className="metric">
          <span>
            <TrendingUp size={14} className="metric-icon" />
            平均分
          </span>
          <strong>{data.average}</strong>
        </div>
        <div className="metric">
          <span>
            <Target size={14} className="metric-icon" />
            及格率
          </span>
          <strong className={data.passRate < 60 ? "metric-warn" : ""}>{data.passRate}%</strong>
        </div>
        <div className="metric">
          <span>
            <Award size={14} className="metric-icon" />
            最高分
          </span>
          <strong>{data.maxScore}</strong>
        </div>
        <div className="metric">
          <span>
            <BarChart3 size={14} className="metric-icon" />
            最低分
          </span>
          <strong>{data.minScore}</strong>
        </div>
      </div>

      <div className="dist-section">
        <div className="dist-title">分数段分布</div>
        <DistributionBar distribution={data.distribution} total={data.studentCount} />
      </div>
    </div>
  );
}

export default function AnalysisPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState(null);
  const [semester, setSemester] = useState("");
  const [keyword, setKeyword] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const result = await api.analyzeGrades();
      setData(result);
    } catch (error) {
      setNotice({ type: "error", message: error.message });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => {});
  }, []);

  const semesters = useMemo(() => {
    const set = new Set(data.map((d) => d.semester));
    return Array.from(set);
  }, [data]);

  const filtered = useMemo(() => {
    return data.filter((item) => {
      if (semester && item.semester !== semester) return false;
      if (keyword) {
        const kw = keyword.toLowerCase();
        return (
          item.courseName.toLowerCase().includes(kw) ||
          item.courseCode.toLowerCase().includes(kw) ||
          item.teacher.toLowerCase().includes(kw)
        );
      }
      return true;
    });
  }, [data, semester, keyword]);

  const overall = useMemo(() => {
    if (!filtered.length) return null;
    const totalStudents = filtered.reduce((s, c) => s + c.studentCount, 0);
    const weightedSum = filtered.reduce((s, c) => s + c.average * c.studentCount, 0);
    const avgScore = totalStudents ? (weightedSum / totalStudents).toFixed(2) : 0;
    const passSum = filtered.reduce((s, c) => s + (c.passRate * c.studentCount) / 100, 0);
    const overallPass = totalStudents ? ((passSum / totalStudents) * 100).toFixed(2) : 0;
    const max = Math.max(...filtered.map((c) => c.maxScore));
    return {
      courseCount: filtered.length,
      totalStudents,
      avgScore,
      overallPass,
      max,
    };
  }, [filtered]);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <h1>班级成绩分析</h1>
          <p>按课程展示平均分、及格率、最高分与分数段分布。</p>
        </div>
        <button className="primary-action inline-btn" onClick={load} disabled={loading}>
          <RefreshCw size={16} className={loading ? "spinning" : ""} />
          刷新数据
        </button>
      </header>

      <Notice notice={notice} />

      <div className="panel">
        <div className="filter-bar">
          <div className="filter-item">
            <label>学期</label>
            <select value={semester} onChange={(e) => setSemester(e.target.value)}>
              <option value="">全部学期</option>
              {semesters.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <div className="filter-item filter-keyword">
            <label>搜索</label>
            <input
              placeholder="课程名称 / 代码 / 教师"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
          </div>
        </div>
      </div>

      {overall && (
        <div className="metric-grid summary-grid">
          <div className="metric">
            <span>课程数</span>
            <strong>{overall.courseCount}</strong>
          </div>
          <div className="metric">
            <span>总参与人次</span>
            <strong>{overall.totalStudents}</strong>
          </div>
          <div className="metric">
            <span>整体平均分</span>
            <strong>{overall.avgScore}</strong>
          </div>
          <div className="metric">
            <span>整体及格率</span>
            <strong>{overall.overallPass}%</strong>
          </div>
          <div className="metric">
            <span>全局最高分</span>
            <strong>{overall.max}</strong>
          </div>
        </div>
      )}

      {loading ? (
        <div className="empty">加载中...</div>
      ) : filtered.length === 0 ? (
        <div className="panel empty">暂无数据</div>
      ) : (
        <div className="course-list">
          {filtered.map((item, idx) => (
            <CourseCard key={`${item.courseCode}-${item.semester}-${idx}`} data={item} />
          ))}
        </div>
      )}
    </section>
  );
}
